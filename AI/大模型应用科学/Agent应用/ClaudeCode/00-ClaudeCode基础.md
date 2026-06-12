
refs:
- [claude-code-docs](https://code.claude.com/docs/zh-CN/overview)
- [marketplaces](https://claudemarketplaces.com/marketplaces)

## VSCode集成

steps：
- 安装扩展
- 二选一：
	- 取消登录界面，在设置中配置国内模型
	- 启用代理，设置Claude API

## 基本命令

- `/init`：在当前工作目录创建/更新`CLAUDE.md`，描述目录内结构、技术细节和注意事项等
- `/compact`：手动压缩上下文，节省思考空间
- `/plugin`：插件/marketplace管理
	- `/plugin marketplace add xxx`：在marketplace中添加xxx；添加后可检索到对应插件
	- `/plugin install yyy`：安装yyy插件

## 安装

目前推荐使用脚本方式安装：

```sh
# macOS/Linux
$ source <(curl -fsSL https://claude-zh.cn/scripts/install.sh)
```

```powershell
# Windows
& ([scriptblock]::Create((New-Object Net.WebClient).DownloadString("https://claude-zh.cn/scripts/install.ps1")))
```

不太推荐使用npm：

```sh
$ npm install -g @anthropic-ai/claude-code
```

如果不使用Claude API，则需要修改`~/.claude/settings.json`，改用第三方API：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "<第三方服务提供的token>",
    "ANTHROPIC_API_KEY": "", // 留空，表示强制不使用Claude
    "ANTHROPIC_BASE_URL": "<第三方Anthropic-like接入点>",
    "ANTHROPIC_MODEL": "<第三方模型名>",
    "ANTHROPIC_REASONING_MODEL": "<第三方模型名>"
  },
  "includeCoAuthoredBy": false,
  "enabledPlugins": {
    // 允许的插件
  }
}
```

## 添加、管理plugins

此小节基于CC v2.1.174

Claude Code的plugins存储在本地`~/.claude/plugins`中，其目录结构：

```
~/.claude/plugins/
├── blocklist.json                 # 插件黑名单
├── known_marketplaces.json        # 已注册的插件市场
├── installed_plugins.json         # 已安装插件清单
├── plugin-catalog-cache.json      # 所有可安装插件的在线目录缓存
├── .last_inuse_sweep              # 使用状态清理标记
├── cache/                         # 已安装插件的本体（源码缓存）
│   └── <插件市场名>/<插件名>/<版本号>/...
├── data/                          # 插件的运行时数据/状态
└── marketplaces/                  # 插件市场的 git 克隆
    └── claude-plugins-official/   # 官方市场仓库
```

