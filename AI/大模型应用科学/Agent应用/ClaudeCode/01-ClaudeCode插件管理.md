
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

官方预装了一系列plugins，位于`marketplaces/claude-plugins-official`下；第三方的plugins则在`cache/<插件市场名>`内

插件（plugin）的结构形如下面目录：

```
<插件名>
├── .claude-plugin/                 # Claude Code插件信息
│   ├── plugin.json
│   └── marketplace.json
├── commands/
├── skills/
├── agents/
├── hooks/
├── .mcp.json
├── .lsp.json
├── settings.json
```