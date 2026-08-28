
ref's:
- [runoob](https://www.runoob.com/ai-agent/openclaw-feishu.html)

openclaw可以飞书机器人的形式参与办公

步骤：
- 登录[飞书开放平台](https://open.feishu.com) - 开发者后台，创建一个企业自建应用，名称和头像自拟
- 在应用后台 - 凭证与基础信息中，记录AppID/AppSecret
- 执行`openclaw channels add`：
	- channel选Feishu/Lark
	- app secret provide选Enter App Secret，输入Secret和ID
	- 连接模式选WebSocket，域视情形选择（一般国内）
	- 消息回复策略暂时选`Open`，后续可以进一步调整
- 配置机器人能力：
	- 之前创建的应用 - 配置 - 添加应用能力 - 机器人
	- 权限管理 - 批量导入权限，添加[[#appendix：机器人默认权限|机器人的默认权限]]
	- 事件与回调配置：
		- 事件订阅方式：长连接
		- 添加订阅事件：
			- `im.message.receive_v1` - 接收消息
			- `im.message.message_read_v1` - 消息已读回执
			- `im.chat.member.bot.added_v1` - 机器人进群
			- `im.chat.member.bot.deleted_v1` - 机器人被移出群
	- 发布应用并重启OpenClaw，将应用加入需要其服务的群组

## appendix：机器人默认权限

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "cardkit:card:read",
      "cardkit:card:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
  }
}
```