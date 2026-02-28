
域名需要买，腾讯云/阿里云/GoDaddy都可买

*DNS记录*控制全球范围内对该域名的解析行为：
- CNAME记录：
- A记录：

## 基于Cloudflared的内网映射

具有公网IP的境内服务器不能在无备案的情形下直接映射80端口，否则会被封。笔者摸索出了一种通过Cloudflare Tunnel映射的方案：
- 首先需要注册Cloudflare账户，把域名的解析服务器挂到Cloudflare上。否则Cloudflare无法更改DNS记录
- 注册ZeroTrust账户，在仪表盘内选`Access -> Tunnel`，新建一个隧道。隧道会要求指定被映射的域名，安全起见使用二级域（如：`app.abc.xyz`），地址指定为服务器的公网IP（如果服务器在内网，看后面的内网穿透）。内网服务器需要对应地安装cloudflared并登录
- 如果IP为公网，应该不需要额外操作

内网穿透：假设你持有一个域名`abc.xyz`，一台本地主机
- 首先在本地主机上安装cloudflared
- 然后登录`Cloudflare -> Zero Trust -> 网络 -> 连接器`
- 点【创建隧道】，然后遵照其后续步骤。其应该需要你指定一个域名的子域（用于与你的本机资源连接）、一个可选路由和你本机的开放路径（一般是`http://localhost`+自定义端口），然后你应该需要在本机执行类似`sudo cloudflared service install xxxxxx`之类的命令。
- 正确执行上述步骤后，Cloudflare平台上应该显示连接器已建立。此时应该可以通过在自定义端口提供网络服务的方式，使本机资源对外可见（而且不用被请喝茶）

