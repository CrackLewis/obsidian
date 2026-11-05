
## Mihomo Core配置

先安装二进制程序，参考实际情况修改：

```sh
sudo apt update
sudo apt install -y curl gzip ca-certificates

# 下载对应架构的最新稳定版本（具体版本要到GitHub查）
curl -fL \
  https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64-v1-$VERSION.gz \
  -o /tmp/mihomo.gz

# 解压
gzip -dc /tmp/mihomo.gz > /tmp/mihomo

# 安装
sudo install -m 755 /tmp/mihomo /usr/local/bin/mihomo

# 检查版本
mihomo -v

# 创建配置目录
mkdir -p /etc/mihomo

# 编写mihomo配置文件（略，假设保存到了/etc/mihomo/config.yaml）

# 验证配置
mihomo -t -d /etc/mihomo
```

配置文件参考格式（YAML）：

```yaml
mixed-port: 7890
allow-lan: false
bind-address: "127.0.0.1"
mode: rule
log-level: warning
ipv6: false

proxies:
  - name: "MyProxy"
    type: ss
    server: "example.com"
    port: 8388
    cipher: "aes-128-gcm"
    password: "your-password"

proxy-groups:
  - name: PROXY
    type: select
    proxies:
      - MyProxy
      - DIRECT

rules:
  - MATCH,PROXY
```

配置开机自启服务（`/etc/systemd/system/mihomo.service`）：

```ini
[Unit]
Description=Mihomo Proxy Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/mihomo -d /etc/mihomo
Restart=on-failure
RestartSec=5
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

启动并设置开机自启：

```sh
# 设置服务自启动
sudo systemctl daemon-reload
sudo systemctl enable --now mihomo

# 查日志
journalctl -u mihomo -f
```

测试（如果成功会输出代理节点的IP）：

```sh
curl -x http://127.0.0.1:7890 https://api.ipify.org
```

