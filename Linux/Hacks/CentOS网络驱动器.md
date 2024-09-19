
这破玩意调了一天。

总体思路：
- 安装CentOS的服务器（称为A机）安装Samba服务，准备一个用于共享的目录，调整好SELinux和防火墙的设置
- 客户机（称为B机）需要确保出站规则正常
- 如果服务器运营商封锁了139、445端口，则A、B机都需要调整端口

## 本机端口转发

本机的`445`端口转发到`a.b.c.d:yyyy`：

```
netsh interface portproxy add v4tov4 listenport=445 listenaddress=127.0.0.1 connectport=yyyy connectaddress=a.b.c.d
```

查看当前活动的转发：

```
netsh interface portproxy show all
```

移除转发：

```
netsh interface portproxy delete v4tov4 listenport=445 listenaddress=127.0.0.1
```

