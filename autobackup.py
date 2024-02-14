import subprocess
from datetime import datetime
from threading import Thread
import time
import os

local_repo_path = "G:\\Desktop\\笔记"
remote_name = "origin"
remote_url = "https://github.com/CrackLewis/obsidian.git"
trojan_path = "D:\\Program Files (x86)\\trojan"

# 启动trojan
# os.chdir(trojan_path)
# trojan_process = subprocess.Popen(["trojan.exe"])

# time.sleep(2)
os.chdir(local_repo_path)

# 添加所有更改的文件到暂存区
subprocess.call(["git", "add", "."])
# 提交更改
commit_message = "AutoBackup: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
commit_result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True)
commit_result_txt = commit_result.stdout.decode('utf8')
print(commit_result_txt)
if "nothing to commit" in commit_result_txt:
	pass
# 推送更改到远程仓库
else:
	while True:
		if subprocess.call(["git", "push", remote_name, "master"]) != 0:
			print("Remote pushing failed. Please update the proxy config or check the network status. ")		
			if 'r' in input('Input R to retry.').lower():
				continue
			else:
				break
		else:
			print("Remote pushing complete. ")
			break


input("Press Enter to exit. ")