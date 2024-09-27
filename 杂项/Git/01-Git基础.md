
迁移自考研复试资料

## 基本概念

- 工作区、暂存区、版本库
- 版本、修改：
	- 相对版本：`~N`表示上N个版本。例如`HEAD~3`。
	- 绝对版本：版本ID的某个前缀、分支名
- 分支、`HEAD`指针
- 远程仓库、远程分支

![[Pasted image 20240305195259.png]]

## 基本操作

- 创建版本库：`git init`
- 暂存一或数个文件修改：`git add <file1> [<file2> ...]`
- 暂存所有文件修改：`git add .`
- 提交暂存更改到版本库：`git commit`
	- 附带备注信息：`-m <message>`
	- 同时提交未暂存更改：`-a`
- 查看工作区与仓库的差异：`git status`
	- 信息简短版：`git status -s`
- 查看工作区的修改：`git diff`
	- 尚未缓存的修改：`git diff`
	- 已缓存的修改：`git diff --cached`
	- 已缓存和尚未缓存的修改：`git diff HEAD`
	- 摘要：`git diff --stat`
- 将工作区重置到某个仓库版本：`git reset`
	- 默认重置（切换仓库版本，重置暂存区）：`git reset [--mixed] <target>`
	- 软重置（只切换仓库版本）：`git reset --soft <target>`
	- 硬重置（切换仓库版本，重置暂存区和工作区，抹消现存更改）：`git reset --hard <target>`
- 查看提交历史：
	- 查看分支上的提交历史：`git log [--oneline] [--graph] [--decorate] [--author=<author>] [--since=<time>] [--until=<time>] [--grep=<pattern>] [--stat]`。
	- 查看单个文件的历史：`git blame <file>`。
- 管理标签：
	- 对当前提交打标签：`git tag [-a] <tag_name> [-m <msg>]`。
	- 显示所有标签：`git tag`。

## 扩展操作

- `git config`：管理Git配置
- `git revert <commit1> [<commit2> ...]`：创建一个新提交，该提交对指定的提交作逆修改
- `git rebase <commit_name>`：将当前结点所有不存在于指定结点前的提交都复制到该结点后，并将当前分支指向最新提交
- `git rebase -i <commit_name>`：交互式rebase，可用特定顺序复制特定提交
- `git cherry-pick <commit1> [<commit2> ...]`：复制指定提交到当前分支下
- `git rm [--cached] <file>`：从暂存区（和工作区，除非有`--cached`选项）移除文件
- `git mv [-f] <file> <new_file>`：移动或重命名文件，`-f`表示强制
- `git restore [--staged] [--source=<commit>] [<file>|.]`：还原仓库或文件至指定提交（默认为最新提交）
- `git restore -i`：交互式还原

## 分支管理

- `git branch`：
	- 查看所有分支：`git branch [--list]`
	- 创建新分支：`git branch <branch_name>`
	- 复制分支：`git branch -c [<old_branch>] <new_branch>`
	- 重命名分支：`git branch -m [<old_branch>] <new_branch>`
	- 删除分支：`git branch -d <branch_name>`
- `git checkout`：
	- 切换到分支：`git checkout <branch_name>`
	- 创建并切换到分支：`git checkout -b <branch_name>`
	- 放弃工作区未暂存更改：`git checkout .`
	- 放弃某个文件未暂存的更改：`git checkout -- <file_name>`
	- 将HEAD切换到某更改：`git checkout <target>`
- `git merge`：
	- 合并当前分支和另一个分支：`git merge <branch_name>`
	- 合并冲突时，中止合并操作：`git merge --abort`
	- 合并冲突时，再次尝试合并：`git merge --continue`
- `git switch`：Git 2.23引入，是`git checkout`的简化版
	- 创建并切换到分支：`git switch -c <branch_name>`
	- 切换到分支：`git switch <branch_name>`
	- 切换到前一个访问的分支：`git switch -`
	- 切换到某个标签：`git switch tags/<tag_name>`

## 远程操作

- 克隆远程仓库到本地：`git clone <url>`
- 管理远程仓库：
	- 列出远程仓库：`git remote`
	- 列出远程仓库并显示URL：`git remote -v`
	- 添加远程仓库：`git remote add <remote_name> <remote_url>`
	- 重命名远程仓库：`git remote rename <old_name> <new_name>`
	- 移除远程仓库：`git remote remove <remote_name>`
	- 修改远程仓库URL：`git remote set-url <remote_name> <new_url>`
	- 显示远程仓库详细信息：`git remote show <remote_name>`
- 拉取远程仓库：`git fetch <remote_name> [<branch_name>]`
	- 查看远程仓库的最新提交：`git log -p FETCH_HEAD`
- 拉取并更新：
	- 拉取远程仓库：`git pull <remote_name>`
	- 拉取远程分支并合并：`git pull <remote> <rem_branch>[:<loc_branch>]`
- 上传到远程并合并：`git push <remote> [<loc_branch>:]<rem_branch>`

以本笔记所在的仓库举例：
- 修改后提交：`git commit -am 'ManualBackup'`
- 上传：`git push origin master`