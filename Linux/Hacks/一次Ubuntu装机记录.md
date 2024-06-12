
## 获取并安装镜像

从清华镜像站获取并下载[Ubuntu 22.04 LTS镜像](https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/22.04/ubuntu-22.04.4-desktop-amd64.iso)。

从VMWare中创建一个新虚拟机，NAT方式入网，100GB外存，4GB内存，2个处理器核心。

启动虚拟机，完成安装流程。我个人选择英文系统和GMT+8时区。

## 第一次启动：配置网络

为啥要先配置网络：我的NAT适配器是手动分配IP，如果不配置就上不了网，也无法进行后续的软件包安装。

这是我的NAT网络配置：

![[Pasted image 20240612104736.png]]

本来还想配一下apt库，后来发现现在`cn.archive.ubuntu.com`自动重定向到清华源。。。NB了。

## 必要软件安装

首先要更新一下apt源：

```bash
$ sudo apt update
```

然后是必要软件：（什么发行版，连GCC都不给装）

```bash
$ sudo apt install open-vm-tools git openssh-server vim net-tools
```

Git要配一下用户名和密码：

```bash
$ git config --global --add user.name CrackLewis
$ git config --global --add user.email cracklewis@fbi.gov
```

SSH的有关配置：[[SSH相关]]

