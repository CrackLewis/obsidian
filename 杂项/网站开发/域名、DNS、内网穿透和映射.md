
域名需要买，腾讯云/阿里云/GoDaddy都可买

*DNS记录*控制全球范围内对该域名的解析行为：
- CNAME记录：
- A记录：

具有公网IP的境内服务器不能在无备案的情形下直接映射80端口，否则会被封。笔者摸索出了一种通过Cloudflare Tunnel映射的方案：
- 首先需要注册Cloudflare账户，把域名的解析服务器挂到Cloudflare上。否则Cloudflare无法更改DNS记录
- 注册ZeroTrust账户，在仪表盘内选`Access -> Tunnel`，新建一个隧道。隧道会要求指定被映射的域名，安全起见使用二级域（如：`app.cracklewis.site`），地址指定为服务器的公网IP（如果服务器在内网，看后面的内网穿透）。内网服务器需要对应地安装cloudflared并登录
- 如果IP为公网，应该不需要额外操作

内网穿透：（没具体实践过，仅供参考）
- 