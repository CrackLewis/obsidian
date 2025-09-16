
这破玩意调了一天。

总体思路：
- 安装CentOS的服务器（称为A机）安装Samba服务，准备一个用于共享的目录，调整好SELinux和防火墙的设置
- 客户机（称为B机）需要确保出站规则正常
- 如果服务器运营商封锁了139、445端口，则A、B机都需要调整端口

## 服务端配置

以Ubuntu为例。

安装samba：

```sh
sudo apt install samba
```

修改配置文件：

```sh
sudo vim /etc/samba/smb.conf
```

假设Samba用户名（稍后会创建）为`smbuser`，共享目录为`/shared`，共享名为`myshared`，则添加如下设置组：

```conf
[myshared]
	comment = My shared folder
	path = /shared
	create mask = 0755
	browseable = Yes
	writable = Yes
	valid users = smbuser
```

另外添加一个名为`smbuser`的用户。（在root用户下执行）

```sh
useradd -m smbuser
passwd smbuser
smbpasswd -a smbuser
```

确保共享目录存在：

```sh
sudo mkdir -p /shared
sudo chmod -R 0755 /shared
sudo chown -R smbuser:smbuser /shared
```

重启服务以使得配置生效：

```sh
sudo service smb restart
```

注意：如果配置文件中的配置名为`myshared`，本地目录为`/shared`，则外部连接到samba服务器需要使用`myshared`名称，而非`shared`。

## Linux客户端连接

mount方式（通过修改`/etc/fstab`可修改为永久挂载）：

```sh
sudo apt install cifs-utils -y
sudo mount -t cifs -o rw,vers=3.0,username=$SMB_USERNAME,password=$SMB_PASSWORD //$SMB_IP/myshared /mnt/myshared
```

samba-client方式：

```sh
sudo smbclient -L $SMB_IP -U $SMB_USERNAME%$SMB_PASSWORD
```

## 本机端口转发

对于部分安全策略十分严苛的发行版（说的就是你，CentOS），有可能139和445端口甚至无法使用。此时需要进行端口转发配置。

此部分基于Windows 10/11系统。

本机的`445`端口转发到`a.b.c.d:yyyy`：

```
netsh interface portproxy add v4tov4 listenport=445 listenaddress=127.0.0.1 connectport=yyyy connectaddress=a.b.c.d
```

查看当前活动的转发：

```
netsh interface portproxy show all
```

如果需要移除转发：

```
netsh interface portproxy delete v4tov4 listenport=445 listenaddress=127.0.0.1
```

