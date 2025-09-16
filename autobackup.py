import subprocess
from datetime import datetime
from threading import Thread
import time
import os

local_repo_path = "C:\\Users\\DELL\\Desktop\\Workbench\\obsidian"
remote_name = "origin"
remote_url = "https://github.com/CrackLewis/obsidian.git"

def main():
	os.chdir(local_repo_path)

	# 添加所有更改的文件到暂存区
	subprocess.run(["git", "add", "."])
	# 提交更改
	commit_message = "AutoBackup: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	commit_result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True)
	commit_result_txt = commit_result.stdout.decode('utf8')
	print(commit_result_txt)
	
	# 拉取远程仓库
	while True:
		fetch_result = subprocess.run(["git", "pull", "--rebase", remote_name, "master"], capture_output=True)
		if fetch_result.returncode != 0:
			fetch_result_txt = fetch_result.stdout.decode('utf8')
			print(fetch_result_txt)
			# 网络原因拉取失败
			if "resolve" in fetch_result_txt or "Connection" in fetch_result_txt:
				print("Remote fetching failed. Please update the proxy config or check the network status. ")
				if 'r' in input('Input R to retry.').lower():
					continue
				else:
					break
			# 本地仓库与远程仓库冲突
			elif "CONFLICT" in fetch_result_txt:
				print("Remote fetching failed due to a conflict. Please resolve the conflict manually. ")
				print("Type 'Y' if you have resolved the conflict, or 'N' if you want to fix it later.")
				if 'y' in input().lower():
					subprocess.run(["git", "add", "."])
					subprocess.run(["git", "rebase", "--continue"])
					break
				elif 'n' in input().lower():
					with open(".CONFLICT", "w") as f:
						f.write(fetch_result_txt)
						print("Conflict information has been saved to .CONFLICT. ")
					return
				else:
					continue
			# 其他错误
			else:
				print("Remote fetching failed due to unknown reasons. ")
				break
		else:
			print("Remote fetching complete. ")
			break

	# 如果本地没有更改，则不进行推送
	if "nothing to commit" in commit_result_txt:
		return
	# 推送更改到远程仓库
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

if __name__ == "__main__":
	main()
input("Press Enter to exit. ")