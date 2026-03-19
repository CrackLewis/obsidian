
refs:
- [blog](https://blog.csdn.net/weixin_45735355/article/details/149448484)

## 基本概念

高性能的HTTP和反向代理web服务器

*正向代理*：客户端配置代理服务器，通过代理服务器访问服务端资源

*反向代理*：
- 客户端无需配置即可访问服务端
- 服务端配置*反向代理服务器*，将客户端请求转发到真实的目标服务器，由目标服务器处理后返回

Nginx负载均衡算法：多个目标服务器，由代理服务器决定向哪个转发
- 轮询（round robin）
- 加权轮询（weighted round robin）
- IP哈希：相同IP只会映射到一台服务器上
- 最少连接、加权最少连接：优先转发到负载低的服务器上
- 自定义哈希（generic hash）
- 随机转发
- 粘性会话：通过Cookie维护连接

## 安装

步骤：
- 源码编译或包管理器安装
- 检查防火墙状态，开放HTTP端口（80容易被封）
- 启动nginx服务

## 架构、配置

实时日志： `/var/log/nginx/access.log`

服务PID：`/var/run/nginx.pid`

配置文件路径（默认）：`/etc/nginx/nginx.conf`

