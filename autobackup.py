import subprocess
from datetime import datetime

# 本地Git仓库路径
local_repo_path = "G:\\Desktop\\笔记"

# 远程仓库名称和URL
remote_name = "origin"
remote_url = "https://github.com/CrackLewis/obsidian.git"

# 切换到仓库目录
# subprocess.call(["cd", local_repo_path])

# 添加所有更改的文件到暂存区
subprocess.call(["git", "add", "."])

# 提交更改
commit_message = "\"AutoBackup: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\""
subprocess.call(["git", "commit", "-m", commit_message])

# 推送更改到远程仓库
subprocess.call(["git", "push", remote_name, "master"])
