import subprocess
import json
import os
import mimetypes
import argparse
from datetime import datetime, timezone

local_repo_path = "C:\\Users\\DELL\\Desktop\\Workbench\\obsidian"
remote_name = "origin"
remote_branch = "master"
LAST_SYNC_FILE = os.path.join(local_repo_path, ".last-sync-r2")
# 上传到 R2 时显式忽略的文件（安全措施，防止凭证泄露）
R2_EXCLUDED_FILES = {"r2.json", ".last-sync-r2", ".gitignore"}


def get_non_ignored_files() -> list[str]:
    """使用 git ls-files 获取仓库中所有未被 .gitignore 忽略的文件
    （排除 .obsidian/、.git/ 及显式安全规则）"""
    result = git_run(["-c", "core.quotepath=false", "ls-files",
                      "--cached", "--others", "--exclude-standard"])
    files = []
    for line in result.stdout.strip().split("\n"):
        path = line.strip().replace("\\", "/")
        if not path:
            continue
        # 排除 .obsidian、.git 目录和显式排除的文件
        if path.startswith((".obsidian/", ".git/")) or path in (".obsidian", ".git"):
            continue
        if path in R2_EXCLUDED_FILES:
            continue
        files.append(path)
    files.sort()
    return files


def generate_tree_json() -> list:
    """从 git ls-files 输出构建完整的文件目录树（所有文件类型，不限于 .md）"""
    print("📁 扫描文件结构...")
    all_files = get_non_ignored_files()

    # 构建前缀树
    tree: dict = {}
    for file_path in all_files:
        parts = file_path.split("/")
        node = tree
        for i, part in enumerate(parts):
            if part not in node:
                node[part] = {} if i < len(parts) - 1 else None
            node = node[part]

    # 递归转换为输出格式
    def build(prefix: str, node: dict) -> list:
        entries = []
        names = sorted(node.keys(), key=lambda n: (0 if isinstance(node[n], dict) else 1, n.lower()))
        for name in names:
            child = node[name]
            path = f"{prefix}/{name}" if prefix else name
            if child is None:  # 文件
                entries.append({"name": name, "path": path, "type": "blob"})
            else:  # 目录
                children = build(path, child)
                if children:
                    entries.append({"name": name, "path": path, "type": "tree", "children": children})
        return entries

    return build("", tree)


def count_entries(nodes: list) -> int:
    """递归统计节点总数"""
    count = 0
    for node in nodes:
        count += 1
        if "children" in node:
            count += count_entries(node["children"])
    return count


def git_run(args: list, check: bool = False):
    """运行 git 命令并返回结果"""
    return subprocess.run(
        ["git"] + args,
        capture_output=True, text=True,
        encoding='utf-8', errors='replace'
    )


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="自动备份笔记并同步到 GitHub + R2")
    parser.add_argument(
        "--increment", action="store_true",
        help="增量模式：根据 git diff 对 R2 做同样增删改"
    )
    parser.add_argument(
        "--zero-trust", action="store_true",
        help="零信任模式：无条件重传所有文件，删除 R2 多余文件，更新 tree.json"
    )
    return parser.parse_args()


def get_last_sync_commit() -> str | None:
    """读取上次同步到的 commit hash"""
    try:
        with open(LAST_SYNC_FILE, "r") as f:
            return f.read().strip()
    except (FileNotFoundError, OSError):
        return None


def save_last_sync_commit(commit_hash: str):
    """记录本次同步到的 commit hash"""
    with open(LAST_SYNC_FILE, "w") as f:
        f.write(commit_hash)


def get_changed_files(since_hash: str) -> dict | None:
    """获取 since_hash..HEAD 之间变更的未忽略文件: {path: status}"""
    check = git_run(["cat-file", "-e", since_hash])
    if check.returncode != 0:
        return None

    result = git_run(["-c", "core.quotepath=false", "diff",
                      "--name-status", f"{since_hash}..HEAD"])
    changed = {}
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t") if "\t" in line else line.split(None, 1)
        if len(parts) < 2:
            continue
        status = parts[0]
        path = parts[-1].strip()
        # 跳过被排除的目录和文件
        if path.startswith((".obsidian/", ".git/")) or path in (".obsidian", ".git"):
            continue
        if path in R2_EXCLUDED_FILES:
            continue
        changed[path] = status
    return changed


def read_r2_config() -> dict | None:
    """读取 r2.json 中的 R2 凭证配置"""
    config_path = os.path.join(local_repo_path, "r2.json")
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        required = ("endpoint", "access_key", "secret_key", "bucket")
        missing = [k for k in required if k not in cfg]
        if missing:
            print(f"⚠️  r2.json 缺少字段: {', '.join(missing)}")
            return None
        return cfg
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️  r2.json 读取失败: {e}")
        return None


def list_r2_objects(client, bucket) -> dict:
    """列出 R2 存储桶中所有对象及其元数据 {key: {Size, LastModified, ...}}"""
    objects = {}
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get("Contents", []):
            objects[obj["Key"]] = obj
    return objects


def get_tree_file_paths(tree: list) -> set:
    """从 tree.json 嵌套结构中提取所有文件路径"""
    paths = set()
    for node in tree:
        if node["type"] == "blob":
            paths.add(node["path"])
        elif "children" in node:
            paths.update(get_tree_file_paths(node["children"]))
    return paths


def _guess_content_type(path: str) -> str:
    ct, _ = mimetypes.guess_type(path)
    return ct or "application/octet-stream"


def _update_tree_json(client, bucket) -> bool:
    """重新生成 tree.json 并上传到 R2，返回是否成功"""
    print("  └─ 更新 tree.json ...")
    tree = generate_tree_json()
    tree_path = os.path.join(local_repo_path, "tree.json")
    with open(tree_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)
    try:
        client.upload_file(tree_path, bucket, "tree.json",
                           ExtraArgs={"ContentType": "application/json"})
        print("    ✅ tree.json 已上传")
        return True
    except Exception as e:
        print(f"    ❌ tree.json 上传失败: {e}")
        return False


def sync_to_r2(mode: str = "full"):
    """同步仓库文件到 Cloudflare R2。

    三种模式:
      "incremental" — 基于 git diff 对 R2 做同样增删改
      "full"        — 以 tree.json 为清单核对 R2，上传缺失/不一致，删除多余
      "zero-trust"  — 无条件重传所有文件，删除 R2 多余文件
    """
    config = read_r2_config()
    if not config:
        print("  ℹ️  未配置 r2.json，跳过 R2 同步（参考 r2.example.json）")
        return

    try:
        import boto3
    except ImportError:
        print("  ❌ 需要 boto3 库来同步 R2，请运行: pip install boto3")
        return

    # tqdm 可选支持
    try:
        from tqdm import tqdm
    except ImportError:
        def tqdm(iterable, **kwargs):
            items = list(iterable)
            desc = kwargs.get("desc", "")
            n = len(items)
            for item in items:
                yield item
            if n:
                print(f"    {desc}: {n} 完成")

    print(f"📤 正在同步到 R2 存储桶 {config['bucket']}（模式: {mode}）...")

    client = boto3.client(
        "s3",
        endpoint_url=config["endpoint"],
        region_name=config.get("region", "us-east-1"),
        aws_access_key_id=config["access_key"],
        aws_secret_access_key=config["secret_key"],
    )
    bucket = config["bucket"]

    # ── increment: 根据 git diff 增删改 ──
    if mode == "incremental":
        last_sync = get_last_sync_commit()
        if not last_sync:
            print("  ⚠️  没有上次同步记录，改用全量模式")
            mode = "full"
        else:
            changed = get_changed_files(last_sync)
            if changed is None:
                print("  ⚠️  上次 sync hash 不在 git 历史中，改用全量模式")
                mode = "full"
            elif not changed:
                print("  └─ 文件: 无变更")
            else:
                additions = {p for p, s in changed.items() if s != "D"}
                deletions = [p for p, s in changed.items() if s == "D"]
                print(f"  └─ 增量: {len(additions)} 新增/修改, {len(deletions)} 删除")

                if additions:
                    for p in tqdm(sorted(additions), desc="上传"):
                        local_path = os.path.join(local_repo_path, p)
                        if os.path.exists(local_path) and not os.path.isdir(local_path):
                            client.upload_file(
                                local_path, bucket, p,
                                ExtraArgs={"ContentType": _guess_content_type(p)}
                            )

                if deletions:
                    for p in tqdm(deletions, desc="删除"):
                        client.delete_object(Bucket=bucket, Key=p)

    # ── full: 以 tree.json 为清单核对 R2 ──
    if mode == "full":
        tree_path = os.path.join(local_repo_path, "tree.json")
        if os.path.exists(tree_path):
            with open(tree_path, "r", encoding="utf-8") as f:
                tree = json.load(f)
        else:
            print("  📋 tree.json 不存在，正在生成...")
            tree = generate_tree_json()
            with open(tree_path, "w", encoding="utf-8") as f:
                json.dump(tree, f, ensure_ascii=False, indent=2)

        tree_files = get_tree_file_paths(tree)

        print("  📋 查询 R2 对象列表...")
        r2_objects = list_r2_objects(client, bucket)

        # (a) 上传缺失或本地更新的文件
        need_upload = []
        for path in sorted(tree_files):
            local_path = os.path.join(local_repo_path, path)
            if not os.path.exists(local_path):
                continue
            st = os.stat(local_path)
            r2_obj = r2_objects.get(path)
            if r2_obj:
                # 大小一致 → 再检查时间戳
                if r2_obj["Size"] == st.st_size:
                    local_utc = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                    if local_utc <= r2_obj["LastModified"]:
                        continue  # 文件一致，跳过
            need_upload.append(path)

        if need_upload:
            print(f"  📤 上传 {len(need_upload)} 个文件...")
            for p in tqdm(need_upload, desc="上传"):
                client.upload_file(
                    os.path.join(local_repo_path, p), bucket, p,
                    ExtraArgs={"ContentType": _guess_content_type(p)}
                )
        else:
            print("  └─ 文件: 均与 R2 一致")

        # (b) 删除 R2 上 tree.json 未追踪的文件
        exclude_prefixes = (".obsidian/", ".git/")
        exclude_set = R2_EXCLUDED_FILES | {"tree.json"}
        to_delete = [
            k for k in r2_objects
            if not k.startswith(exclude_prefixes)
            and k not in exclude_set
            and k not in tree_files
        ]
        if to_delete:
            print(f"  🗑️  删除 {len(to_delete)} 个 R2 多余文件...")
            for p in tqdm(to_delete, desc="删除"):
                client.delete_object(Bucket=bucket, Key=p)

    # ── zero-trust: 无条件重传 ──
    if mode == "zero-trust":
        all_files = get_non_ignored_files()
        print(f"  📤 无条件重传 {len(all_files)} 个文件...")
        for p in tqdm(all_files, desc="上传"):
            client.upload_file(
                os.path.join(local_repo_path, p), bucket, p,
                ExtraArgs={"ContentType": _guess_content_type(p)}
            )

        # 清理 R2 多余文件
        file_set = set(all_files)
        exclude_prefixes = (".obsidian/", ".git/")
        exclude_set = R2_EXCLUDED_FILES | {"tree.json"}
        r2_objects = list_r2_objects(client, bucket)
        to_delete = [
            k for k in r2_objects
            if not k.startswith(exclude_prefixes)
            and k not in exclude_set
            and k not in file_set
        ]
        if to_delete:
            print(f"  🗑️  删除 {len(to_delete)} 个 R2 多余文件...")
            for p in tqdm(to_delete, desc="删除"):
                client.delete_object(Bucket=bucket, Key=p)

    # ── 统一收尾：更新 tree.json + 保存 sync hash ──
    _update_tree_json(client, bucket)

    current_head = git_run(["rev-parse", "HEAD"]).stdout.strip()
    if current_head:
        save_last_sync_commit(current_head)

    print(f"\n  ✅ R2 同步完成（模式: {mode}）")


def main():
    args = parse_args()
    os.chdir(local_repo_path)

    # ============================================================
    # Step 1: 获取远程仓库状态
    # ============================================================
    print("=" * 50)
    print("步骤 1/5: 获取远程仓库状态...")
    print("-" * 50)

    fetch_result = git_run(["fetch", remote_name])
    if fetch_result.returncode != 0:
        output = fetch_result.stderr
        print(fetch_result.stdout, end="")
        print(fetch_result.stderr, end="")

        while True:
            if "resolve" in output or "Connection" in output:
                print("\n⚠️  网络连接异常，请检查代理或网络设置")
                choice = input("输入 R 重试，其他键退出: ").lower()
                if choice == 'r':
                    fetch_result = git_run(["fetch", remote_name])
                    output = fetch_result.stderr
                    if fetch_result.returncode == 0:
                        print("✅ 远程获取成功")
                        break
                    continue
                else:
                    print("已退出")
                    return
            else:
                print("❌ 获取远程失败，请检查仓库配置")
                return

    print("✅ 远程获取成功")

    # ============================================================
    # Step 2: 检查远程更新，有冲突则提示人工介入
    # ============================================================
    print("\n步骤 2/5: 检查远程更新...")
    print("-" * 50)

    # 检查本地是否落后于远程
    behind_result = git_run(["rev-list", "--count", f"HEAD..{remote_name}/{remote_branch}"])
    behind = int(behind_result.stdout.strip() or 0)

    # 检查本地是否领先于远程
    ahead_result = git_run(["rev-list", "--count", f"{remote_name}/{remote_branch}..HEAD"])
    ahead = int(ahead_result.stdout.strip() or 0)

    if behind > 0:
        print(f"📥 远程有 {behind} 个新提交，正在拉取...")

        while True:
            pull_result = git_run(["pull", "--rebase", remote_name, remote_branch])
            if pull_result.returncode != 0:
                output = pull_result.stdout + pull_result.stderr
                print(output)

                if "CONFLICT" in output:
                    print("\n" + "⚠️ " * 15)
                    print("⚠️  合并冲突！需要人工介入")
                    print("⚠️ " * 15)
                    print("\n请手动解决冲突后，输入 Y 继续")
                    print("输入 N 中止操作（冲突信息将保存到 .CONFLICT）")
                    choice = input().lower()

                    if choice == 'y':
                        git_run(["add", "."])
                        continue_result = git_run(["rebase", "--continue"])
                        if continue_result.returncode != 0:
                            print(f"❌ rebase 继续失败: {continue_result.stderr}")
                            print("请手动完成 rebase 后重新运行脚本")
                            return
                        print("✅ 冲突已解决，rebase 继续")
                        break
                    elif choice == 'n':
                        git_run(["rebase", "--abort"])
                        with open(".CONFLICT", "w", encoding="utf-8") as f:
                            f.write(output)
                        print("⚠️  已中止，冲突信息保存到 .CONFLICT")
                        print("   请手动处理冲突后重新运行脚本")
                        return
                    else:
                        continue

                elif "resolve" in output or "Connection" in output:
                    print("⚠️  网络异常")
                    if input("输入 R 重试: ").lower() == 'r':
                        continue
                    else:
                        return
                else:
                    print(f"❌ 拉取失败: {output}")
                    return
            else:
                print("✅ 拉取完成")
                break

    elif ahead > 0:
        print(f"📤 本地领先远程 {ahead} 个提交，准备推送")
    else:
        print("✅ 本地仓库已是最新")

    # ============================================================
    # Step 3: 根据最新仓库状态生成 tree.json
    # ============================================================
    print("\n步骤 3/5: 根据仓库状态生成 tree.json...")
    print("-" * 50)

    tree = generate_tree_json()
    tree_path = os.path.join(local_repo_path, "tree.json")
    with open(tree_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)

    total = count_entries(tree)
    print(f"\n✅ tree.json 已生成（{total} 条记录）")
    print(f"   输出: tree.json")

    # ============================================================
    # Step 4: 提交本地改动并推送到远程
    # ============================================================
    print("\n步骤 4/5: 提交并推送...")
    print("-" * 50)

    # Stage 所有文件（包括 tree.json）
    git_run(["add", "."])

    # 检查是否有改动需要提交
    status_result = git_run(["-c", "core.quotepath=false", "status", "--porcelain"])
    if status_result.stdout.strip():
        # 提交
        commit_msg = f"AutoBackup-R2: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        commit_result = git_run(["commit", "-m", commit_msg])
        print(commit_result.stdout, end="")

        if commit_result.returncode == 0:
            print(f"📦 提交信息: {commit_msg}")

            # 推送
            print("\n正在推送到远程...")
            while True:
                push_result = git_run(["push", remote_name, remote_branch])
                if push_result.returncode != 0:
                    output = push_result.stdout + push_result.stderr
                    if "resolve" in output or "Connection" in output:
                        print("⚠️  网络异常")
                        if input("输入 R 重试: ").lower() == 'r':
                            continue
                        else:
                            break
                    else:
                        print(f"❌ 推送失败: {output}")
                        break
                else:
                    print("✅ 推送完成")
                    break
        else:
            print(f"⚠️  提交跳过: {commit_result.stderr.strip() or commit_result.stdout.strip()}")
    else:
        print("ℹ️  没有需要提交的更改")

    # ============================================================
    # Step 5: 同步到 Cloudflare R2（始终执行，不依赖 Git 提交结果）
    # ============================================================
    print("\n步骤 5/5: 同步到 Cloudflare R2...")
    print("-" * 50)
    if args.zero_trust:
        mode = "zero-trust"
    elif args.increment:
        mode = "incremental"
    else:
        mode = "full"
    sync_to_r2(mode=mode)


if __name__ == "__main__":
    main()
    input("\n按 Enter 退出...")
