import subprocess
import json
import os
import mimetypes
import argparse
from datetime import datetime

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
        help="增量模式：仅同步 git 历史中有变更的文件到 R2（首次运行自动全量）"
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


def sync_to_r2(incremental: bool = False):
    """将 tree.json 和仓库文件同步到 Cloudflare R2。"""
    config = read_r2_config()
    if not config:
        print("  ℹ️  未配置 r2.json，跳过 R2 同步（参考 r2.example.json）")
        return

    try:
        import boto3
    except ImportError:
        print("  ❌ 需要 boto3 库来同步 R2，请运行: pip install boto3")
        return

    print(f"📤 正在同步到 R2 存储桶 {config['bucket']} ...")

    client = boto3.client(
        "s3",
        endpoint_url=config["endpoint"],
        region_name=config.get("region", "us-east-1"),
        aws_access_key_id=config["access_key"],
        aws_secret_access_key=config["secret_key"],
    )

    bucket = config["bucket"]

    # --- 收集需要上传/删除的文件 ---
    files_to_upload: dict[str, str] = {}    # r2_key → local_path
    files_to_delete: list[str] = []         # r2_key

    if incremental:
        last_sync = get_last_sync_commit()
        if last_sync:
            changed = get_changed_files(last_sync)
            if changed is None:
                print("  ⚠️  上次同步记录不在 git 历史中，改为全量同步")
                last_sync = None
            elif not changed:
                print("  └─ 文件: 无变更（仅更新 tree.json）")
            else:
                additions = {p for p, s in changed.items() if s != "D"}
                deletions = [p for p, s in changed.items() if s == "D"]
                print(f"  └─ 文件（增量）: {len(additions)} 个新增/修改, {len(deletions)} 个删除")

                for path in additions:
                    local_path = os.path.join(local_repo_path, path)
                    if os.path.exists(local_path) and not os.path.isdir(local_path):
                        files_to_upload[path] = local_path
                files_to_delete = deletions

        if last_sync is None:
            incremental = False  # 回退到全量

    if not incremental:
        # 全量模式：使用 git ls-files 扫描所有未被忽略的文件
        print("  └─ 文件（全量）...")
        for path in get_non_ignored_files():
            files_to_upload[path] = os.path.join(local_repo_path, path)

    # --- 执行上传 ---
    uploaded = 0
    failed = 0

    if not files_to_upload and not files_to_delete:
        print("  └─ 文件: 无变更")
    else:
        progress_label = f"  └─ 文件 ({'增量' if incremental else '全量'}): "
        print(f"{progress_label}上传 {len(files_to_upload)}, 删除 {len(files_to_delete)}")

        for r2_key, local_path in files_to_upload.items():
            content_type, _ = mimetypes.guess_type(local_path)
            if not content_type:
                content_type = "application/octet-stream"

            try:
                # 使用 upload_file（有内置重试）替代 put_object 提升可靠性
                client.upload_file(local_path, bucket, r2_key,
                                   ExtraArgs={"ContentType": content_type})
                uploaded += 1
            except Exception as e:
                print(f"    ❌ {r2_key}: {e}")
                failed += 1

        for r2_key in files_to_delete:
            try:
                client.delete_object(Bucket=bucket, Key=r2_key)
            except Exception as e:
                print(f"    ❌ 删除失败 {r2_key}: {e}")
                failed += 1

    # --- 上传 tree.json ---
    print("  └─ tree.json ...")
    tree_path = os.path.join(local_repo_path, "tree.json")
    try:
        client.upload_file(tree_path, bucket, "tree.json", ExtraArgs={"ContentType": "application/json"})
        print("    ✅ tree.json 已上传")
    except Exception as e:
        print(f"    ❌ tree.json 上传失败: {e}")
        failed += 1

    # --- 记录本次同步的 commit hash（用于下次增量对比） ---
    current_head = git_run(["rev-parse", "HEAD"]).stdout.strip()
    if current_head:
        save_last_sync_commit(current_head)

    if failed:
        print(f"\n  ⚠️  完成: {uploaded} 个上传, {failed} 个失败")
    else:
        print(f"\n  ✅ R2 同步完成: {uploaded} 个文件已同步")


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
    sync_to_r2(incremental=args.increment)


if __name__ == "__main__":
    main()
    input("\n按 Enter 退出...")
