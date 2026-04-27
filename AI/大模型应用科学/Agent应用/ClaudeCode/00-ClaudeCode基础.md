
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
- 