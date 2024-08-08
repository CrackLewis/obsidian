
## 文件系统指令

- 基础：ls、cp、mv、rm、mkdir、rmdir、touch、pwd
- 链接：ln
- 更改文件信息：chmod、chown、chgrp、umask
- 查找定位：find、locate
- 打包和解包：tar、zip、unzip、gzip、gunzip
- 远程同步：rsync

## 存储系统指令

- 文件系统的磁盘使用：df
- 磁盘空间用量：du
- 磁盘分区：fdisk

### df

`df <options> [<directory>]`：
- `directory`：挂载点。表示查询挂载点对应文件系统的数据
- 选项：
	- `-h`、`-H`：人性化显示。区别是前者单位为GiB（$2^{30} B$），后者单位为GB（$10^9 B$）。
	- `-k`：用量以KB单位显示，而非字节单位。
	- `-T`：显示文件系统类型（如：ntfs、ext4等）。

`df -h`可以查看所有文件系统的用量和挂载点：

```
lewislee@CrackLewis:/mnt/g/Desktop$ df -h
Filesystem      Size  Used Avail Use% Mounted on
none            3.9G  4.0K  3.9G   1% /mnt/wsl
drivers         251G  216G   35G  87% /usr/lib/wsl/drivers
none            3.9G     0  3.9G   0% /usr/lib/modules
none            3.9G     0  3.9G   0% /usr/lib/modules/5.15.153.1-microsoft-standard-WSL2
/dev/sdc       1007G   63G  894G   7% /
none            3.9G   96K  3.9G   1% /mnt/wslg
none            3.9G     0  3.9G   0% /usr/lib/wsl/lib
rootfs          3.9G  2.1M  3.9G   1% /init
none            3.9G     0  3.9G   0% /run
none            3.9G     0  3.9G   0% /run/lock
none            3.9G     0  3.9G   0% /run/shm
none            3.9G     0  3.9G   0% /run/user
tmpfs           3.9G     0  3.9G   0% /sys/fs/cgroup
none            3.9G   76K  3.9G   1% /mnt/wslg/versions.txt
none            3.9G   76K  3.9G   1% /mnt/wslg/doc
C:\             251G  216G   35G  87% /mnt/c
D:\             206G  150G   56G  73% /mnt/d
G:\             805G  479G  327G  60% /mnt/g
```

### du

