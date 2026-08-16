---
tags:
  - WSL
  - Linux
  - 网络
created: 2026-08-16
---
本文由Codex整理

# WSL2 网络配置（NAT / Mirrored 与代理）

> 本文结合 2026-08-16 本机实测整理的 WSL2 网络知识。实测环境：Windows 11 (Build 26200)、WSL 2.7.11、内核 6.18.33.2-2、Ubuntu-26.04、代理 mihomo (Clash Party)。

## 1. WSL2 网络架构概述

WSL2 本质是一台由 Hyper-V 承载的轻量虚拟机，拥有**独立的 Linux 网络栈**（独立的网卡、IP、路由、DNS）。它与 Windows 主机的网络关系由 `.wslconfig` 中的 `networkingMode` 决定，只有两种模式：

| 模式  | 配置值                         | 默认   | 一句话特点                              |
| --- | --------------------------- | ---- | ---------------------------------- |
| NAT | `networkingMode=NAT`（或省略该行） | ✅ 默认 | WSL 在私有子网内，通过主机 NAT 上网，与主机网络"隔开"   |
| 镜像  | `networkingMode=mirrored`   | ❌    | WSL 直接镜像主机网卡，与主机"共享"网络栈和 localhost |

两种模式的核心差异：

- **NAT**：WSL 有自己的私网 IP，对外流量由 Windows 做地址转换（SNAT），安全、隔离、稳定，但对"本机互访"不友好（localhost 单向）。
- **Mirrored**：WSL 直接借用主机的 IP 和网卡，localhost 双向互通、支持局域网直连 WSL，但对 VPN、虚拟网卡驱动等第三方网络组件很敏感。

## 2. NAT 模式（默认，本机当前使用）

### 2.1 网络构造

```
┌────────────────────────── Windows 主机 ──────────────────────────┐
│                                                                  │
│    WSL 虚拟机（eth0）                                             │
│    ┌─────────────────────┐                                       │
│    │ Ubuntu-26.04        │                                       │
│    │ eth0 = 172.21.20.41/20    默认路由 → 172.21.16.1             │
│    │ DNS  → 10.255.255.254      │                                │
│    └──────────┬──────────┘      │                                │
│               │ 虚拟交换机（Hyper-V）                              │
│   ┌───────────▼───────────────────┐                              │
│   │ vEthernet (WSL (Hyper-V       │ 宿主侧 = 172.21.16.1/20       │
│   │  firewall)) = NAT 网关         │                              │
│   └───────────┬───────────────────┘                              │
│               │ NAT（SNAT）                                       │
│   ┌───────────▼───────────────────┐                              │
│   │ 物理网卡 / VPN（本机：iSecSP）   │ 默认路由 10.7.0.1（VPN）      │
│   └────────────────────────────────┘                             │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 关键事实（本机实测）

- 宿主侧虚拟网卡：`vEthernet (WSL (Hyper-V firewall))`，IPv4 = `172.21.16.1/20`。这是 WSL 的 **NAT 网关**。
- WSL 侧：`eth0` 通过 DHCP 拿到 `172.21.20.41/20`，默认路由 `default via 172.21.16.1 dev eth0`。
- WSL 的 `/etc/resolv.conf` 指向 `10.255.255.254`——这是 **WSL 的 DNS 代理**（负责把 DNS 请求转发给 Windows 的 DNS），不是主机 IP。
- 出站：WSL → 外网，经 NAT 转换后从主机物理网卡出去，**可用**。
- 入站：外网/局域网 → WSL，默认**不可达**（没有端口映射）。
- localhost 转发：`localhostForwarding=true`（默认）只保证 **Windows → WSL 的 localhost 转发**（访问 `localhost:端口` 可到 WSL 里的服务）。
- **WSL → Windows 的 localhost 不通**：WSL 里的 `127.0.0.1` 是虚拟机自己的回环，不是主机的。访问主机服务必须用 NAT 网关地址 `172.21.16.1`（旧版本也可以用 `resolv.conf` 里的 nameserver，新版本已改为 DNS 代理地址，不再适用）。

### 2.3 可达性矩阵（NAT）

| 方向               | 方式               | 结果                        |
| ---------------- | ---------------- | ------------------------- |
| Windows → WSL 服务 | `localhost:端口`   | ✅（默认开启）                   |
| WSL → Windows 服务 | `172.21.16.1:端口` | ✅（服务需监听在主机可达的地址）          |
| WSL → Windows 服务 | `127.0.0.1:端口`   | ❌（回环隔离）                   |
| WSL → 外网         | 直接访问             | ✅（NAT）                    |
| 局域网 → WSL        | 直接访问             | ❌（需 portproxy 或 mirrored） |

### 2.4 相关 .wslconfig 参数

| 参数                        | 默认         | 作用                                           |
| ------------------------- | ---------- | -------------------------------------------- |
| `localhostForwarding`     | `true`     | 是否允许主机通过 localhost 访问 WSL 端口（仅 NAT 有效）       |
| `dnsTunneling`            | `true`（新版） | DNS 通过隧道转发到 Windows，Windows 的 DNS 后缀可镜像进 WSL |
| `dnsProxy`                | `true`     | 是否启用 NAT DNS 代理                              |
| `autoProxy`               | `true`     | 是否把 Windows 代理设置镜像进 WSL（见 5.4 的限制）           |
| `initialAutoProxyTimeout` | `1000`     | 启动时等待获取 Windows 代理信息的最长时间（毫秒）                |

## 3. Mirrored 模式（镜像）

### 3.1 网络构造

镜像模式下，WSL 不再使用独立私网，而是**直接镜像 Windows 主机的网络接口**：WSL 里的 `eth0` 拥有与主机相同的 IP 地址，与主机共享网卡、路由和 localhost（双向）。

### 3.2 优点

- `localhost` 双向互通：WSL 里直接用 `127.0.0.1:端口` 就能访问主机服务（例如代理 `http://127.0.0.1:7890`）。
- 支持局域网其他设备直接访问 WSL 服务（与主机同 IP、同端口）。
- 支持组播 / mDNS（`.local` 域名解析）。
- Windows 的系统代理（含 localhost 代理）可被 `autoProxy` 自动同步进 WSL。

### 3.3 要求与限制

- 需要 Windows 11 22H2+ 与 WSL 2.0+。
- **已知与部分 VPN / NDIS 过滤驱动不兼容**（Microsoft 官方排障文档列出了这类问题，如 Cisco AnyConnect 等）。
- 某些场景下虚拟网卡初始化失败，导致 `eth0` 处于 DOWN、无 IP、无路由——**本机正是这个故障**，详见第 4 节。

### 3.4 相关 .wslconfig 参数

| 参数                        | 说明                                                                             |
| ------------------------- | ------------------------------------------------------------------------------ |
| `networkingMode=mirrored` | 开启镜像模式                                                                         |
| `firewall`                | 是否启用 Hyper-V/WSL 防火墙（默认 true）                                                  |
| `ignoredPorts`            | 镜像模式下不镜像的端口列表（避开端口冲突）                                                          |
| `hostAddressLoopback`     | 实验性；**仅 mirrored 模式生效**，允许通过"分配给主机的 IP"在主机与 WSL/容器之间互访（注意：不是 127.0.0.1 回环的替代品） |

## 4. 本机实战案例（2026-08-16）

### 4.1 故障现象

WSL 能正常启动，但完全不能联网：

```text
eth0: <BROADCAST,MULTICAST> state DOWN   # 无 IP、无 UP 标志
ip route：空                               # 无默认路由
ping / curl：Network is unreachable
```

Windows 主机上网正常（curl 百度 200），但 ping 8.8.8.8 超时。

### 4.2 根因

`.wslconfig` 中配置了 `networkingMode=Mirrored`。本机装有 **Array Networks SSL VPN（iSecSP）**，其 TAP/NDIS 过滤驱动与 WSL 镜像模式冲突，导致 WSL 虚拟网卡初始化失败（eth0 DOWN、无 IP、无路由）。重启 WSL 无法解决，确认是配置层面的稳定冲突。

### 4.3 修复

把 `.wslconfig` 中的 `networkingMode=Mirrored` 删除（回到默认 NAT），然后 `wsl --shutdown` 重启：

```ini
# C:\Users\CrackLewis\.wslconfig（当前生效）
[wsl2]
processors=12

[experimental]
hostAddressLoopback=true
```

修复后 `eth0` 正常拿到 IP、默认路由出现，baidu / github / archive.ubuntu.com / pypi 全部 200。

> 注意：`hostAddressLoopback` 是实验项且仅 mirrored 模式生效，当前 NAT 模式下它实际不起作用（这解释了 127.0.0.1:7890 在 WSL 里依然不通）。

### 4.4 本机环境快照

| 项目              | 值                                                  |
| --------------- | -------------------------------------------------- |
| WSL 版本          | 2.7.11.0（内核 6.18.33.2-2）                           |
| 发行版             | Ubuntu-26.04（WSL2）                                 |
| NAT 宿主网关        | 172.21.16.1/20（vEthernet (WSL (Hyper-V firewall))） |
| WSL eth0        | 172.21.20.41/20                                    |
| WSL DNS         | 10.255.255.254（WSL DNS 代理）                         |
| 主机物理网卡          | MediaTek Wi-Fi 6E MT7922（被 VPN 改名为 iSecSP）         |
| 主机默认路由          | 0.0.0.0/0 via 10.7.0.1（VPN 网关，metric 0）            |
| 主机 DNS          | 127.0.0.1 + 162.105.129.27（北大 DNS）                 |
| ICMP            | 被 VPN 屏蔽：ping 不通，但 TCP/HTTPS 正常                    |
| Hyper-V/WSL 防火墙 | 入站默认 Block，出站默认 Allow                              |
| 代理软件            | mihomo (Clash Party)，allow-lan=true                |

## 5. 代理连接方法

### 5.1 核心原理

要让 WSL 使用 Windows 上的代理，本质是让 WSL 能访问到代理监听的地址。NAT 模式下：

- 代理监听 `127.0.0.1:7890` → **只有 Windows 自己能访问**，WSL 访问不到（回环隔离）。
- 代理监听 `0.0.0.0:7890`（即开启"允许局域网连接"）→ WSL 通过网关 `172.21.16.1:7890` 访问 ✅。

实测对比（allow-lan 开启后）：

| 测试                                    | 结果                  |
| ------------------------------------- | ------------------- |
| Windows 访问 `127.0.0.1:7890`           | ✅ HTTP 400（正常裸请求响应） |
| WSL 访问 `127.0.0.1:7890`               | ❌ 连接被拒              |
| WSL 访问 `172.21.16.1:7890`             | ✅                   |
| WSL 用 `172.21.16.1:7890` 当代理访问 Google | ✅ 302               |

### 5.2 Windows 侧：开启局域网监听

代理软件（Clash / mihomo / v2ray 等）默认只监听 `127.0.0.1`，需要在 GUI 中开启 **"允许局域网连接"（Allow LAN）**，或直接改配置：

```yaml
# C:\Users\CrackLewis\AppData\Roaming\mihomo-party\work\config.yaml
allow-lan: true
```

改完重新加载配置。开启后监听地址变为 `::` / `0.0.0.0`。

若 Windows 防火墙拦截 WSL 访问，只放行 WSL 网段（推荐，不要对整个局域网开放）：

```powershell
New-NetFirewallRule -DisplayName "Mihomo Allow WSL" -Direction Inbound `
  -LocalPort 7890,7891,7892 -Protocol TCP -Action Allow -RemoteAddress 172.21.16.0/20
```

本机 mihomo 端口约定：`7890` = mixed（HTTP+SOCKS5）、`7891` = SOCKS5、`7892` = HTTP。

### 5.3 WSL 侧：proxy_on / proxy_off 开关（已安装）

> 方案选定：**默认不代理**，需要时手动开、用完关，避免所有场景都被代理接管。

已写入 `~/.bashrc`（标记 `# === WSL_HOST_PROXY`），内容：

```bash
proxy_on() {
  local host_ip
  host_ip=$(ip route show default | awk '{print $3}')   # 动态取 NAT 网关 = 主机地址
  export http_proxy="http://${host_ip}:7890"
  export https_proxy="http://${host_ip}:7890"
  export all_proxy="socks5://${host_ip}:7891"
  export no_proxy="localhost,127.0.0.1,::1"
  export NO_PROXY="$no_proxy"
  echo "proxy ON -> ${http_proxy}"
}

proxy_off() {
  unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY no_proxy NO_PROXY
  echo "proxy OFF"
}
```

用法：

```bash
proxy_on      # 当前终端会话开启代理（curl/git/npm/pip/apt 等自动生效）
proxy_off     # 关闭并清空环境变量
```

特点：

- 主机地址**动态获取**（默认路由的网关），WSL 重启、NAT 网段变化后依然有效，无需改代码。
- 只影响当前终端会话；重开终端即恢复默认直连。
- 网关 IP 指到的是主机，不是代理端口本身；端口 7890/7891 需与代理软件一致。

### 5.4 autoProxy（WSL 自动同步 Windows 代理）

WSL 2.0+ 默认 `autoProxy=true`，会尝试把 Windows 系统代理镜像为 Linux 环境变量（`HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY` 等，均同时设置大小写；PAC 代理则通过 `WSL_PAC_URL` 配置）。

**重要限制（本机实测）**：若 Windows 系统代理是 `127.0.0.1:端口` 这类 localhost 地址，NAT 模式下 WSL **不会**镜像，并提示：

```text
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
```

结论：`autoProxy` 在 **mirrored 模式**下对 localhost 代理可用；在 **NAT 模式**下不可用，需要手动方案（5.3）。

### 5.5 单条命令临时走代理

不改任何状态，仅本次命令生效：

```bash
curl -x http://172.21.16.1:7890 https://www.google.com
https_proxy=http://172.21.16.1:7890 git push
```

### 5.6 按工具固定配置（可选）

适合"某个工具永远走代理"的场景（注意：这类配置是持久的、按工具生效）：

```bash
# git（全局）
git config --global http.proxy http://172.21.16.1:7890
git config --global https.proxy http://172.21.16.1:7890

# apt（需要 sudo）
# 写入 /etc/apt/apt.conf.d/95proxy：
#   Acquire::http::Proxy "http://172.21.16.1:7890";
#   Acquire::https::Proxy "http://172.21.16.1:7890";

# npm
npm config set proxy http://172.21.16.1:7890
npm config set https-proxy http://172.21.16.1:7890

# pip
pip config set global.proxy http://172.21.16.1:7890
```

注意：`sudo apt` 默认不继承用户环境变量，所以 apt 要么用上面的配置文件，要么把静态代理写入 `/etc/environment`。

### 5.7 验证方法

```bash
# 1) 代理链路是否通（返回 200/302 即通）
curl -sS -m 8 -o /dev/null -w '%{http_code}\n' -x http://172.21.16.1:7890 https://www.google.com

# 2) 开关是否生效
proxy_on && env | grep -i proxy
proxy_off && env | grep -i proxy || echo clean

# 3) 直连 vs 代理出口 IP（国内站点可能被 Clash 规则直连，属正常）
curl -sS https://api.ipify.org          # 直连出口（本机直连该站超时，被网络屏蔽）
curl -sS -x http://172.21.16.1:7890 https://api.ipify.org   # 代理出口
```

## 6. 排障速查表

| 现象                    | 可能原因                              | 处理                                                                   |
| --------------------- | --------------------------------- | -------------------------------------------------------------------- |
| `eth0` DOWN、无 IP、无路由  | WSL 网络栈未初始化；mirrored 模式与 VPN/驱动冲突 | `wsl --shutdown` 重启；检查 `.wslconfig` 的 `networkingMode`；有 VPN 时优先 NAT |
| ping 不通但网页/HTTPS 正常   | ICMP 被 VPN 或防火墙屏蔽                 | 正常现象，用 curl/TCP 验证                                                   |
| WSL 访问主机 localhost 失败 | NAT 模式回环隔离                        | 用网关 `172.21.16.1` 代替 `127.0.0.1`                                     |
| 代理连不上                 | allow-lan 未开 / 防火墙拦截 / 端口不对       | 开 Allow LAN；放行 WSL 网段；核对端口（本机 7890/7891/7892）                        |
| `autoProxy` 不生效       | NAT 模式 + localhost 代理             | 手动 `proxy_on`；或改用 mirrored（需评估 VPN 兼容性）                              |
| DNS 解析异常              | resolv.conf 被改坏 / DNS 隧道关闭        | 恢复自动生成：`[network] generateResolvConf=true`；检查 `dnsTunneling`         |
| WSL 里能解析但连不上外网        | 路由缺失                              | `ip route` 应有 `default via 172.21.16.1`；无则重启 WSL                     |

## 7. 参考链接

- Microsoft Learn：WSL 高级配置（.wslconfig / wsl.conf）：<https://learn.microsoft.com/en-us/windows/wsl/wsl-config>
- Microsoft Learn：WSL 网络访问应用（含 autoProxy 说明）：<https://learn.microsoft.com/en-us/windows/wsl/networking>
- Microsoft Learn：WSL 排障（VPN 兼容性、代理镜像注意事项）：<https://learn.microsoft.com/en-us/windows/wsl/troubleshooting>
- WSL 2.0 更新公告（mirrored 网络、autoProxy 引入）：<https://devblogs.microsoft.com/commandline/windows-subsystem-for-linux-september-2023-update/>

