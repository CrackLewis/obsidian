
ref's:
- [github-repo](https://github.com/evilbinary/catclaw)

## outline

目录结构：

```
catclaw/src/
+ main.c            # 程序入口：初始化各模块、命令行交互循环
  
+ agent/            # Agent核心逻辑
  + agent.{c,h}     # Agent主模块：状态管理、消息队列、工具注册、多步执行等
  + command.{c,h}   # 命令及其解析
  + context.{c,h}   # 上下文管理

+ common/
  + cJSON.{c,h}       # (第三方编写的)JSON解析逻辑
  + config.{c,h}      # 本地配置文件加载和管理
  + http_client.{c,h} # HTTP客户端逻辑
  + log.{c,h}         # 日志逻辑
  + platform.{c,h}    # 平台兼容处理
  + plugin.{c,h}      # 插件加载和管理逻辑
  + queue.{c,h}       # 线程安全的消息队列
  + thread_pool.{c,h} # 线程池
  + utils.{c,h}       # 杂项工具函数
  + workspace.{c,h}   # 工作空间管理
  + ws_client.{c,h}   # WebSocket客户端

+ gateway/               # 网关层：多平台消息接入
  + gateway.{c,h}        # 网关核心（WS/飞书/HTTP）
  + channels.{c,h}       # 频道管理：多平台统一分发消息
  + discord.{c,h}
  + feishu.{c,h}
  + feishu_ws.{c,h}
  + http_api.{c,h}
  + http_server.{c,h}
  + telegram.{c,h}
  + websocket.{c,h}
  + weixin.{c,h}

+ memory/            # 长期记忆系统
  + memory.{c,h}     # KV-pairs持久化记忆（存文件）
    
+ model/                      # AI模型接入层
  + ai_model.{c,h}            # 模型管理
  + ai_provider.h             # Provider接口抽象（流式回调、响应结构）
  + ai_provider_factory.{c,h} # Provider工厂
  + provider_anthropic.c      # Claude
  + provider_gemini.c         # Gemini
  + provider_ollama.c         # Ollama
  + provider_openai.c         # OpenAI

+ session/            # 会话管理
  + session.{c,h}     # 会话生命周期、磁盘持久化、压缩
  + message.{c,h}     # 消息结构（角色、内容、附件、工具调用）

+ tool/                # 工具系统（AI可调用的函数）
  + tool.{c,h}         # 工具注册/执行框架+内置工具
  + skill.{c,h}        # 技能系统
  + skill_weather.c    # 一个内置技能示例（天气查询）
```

层次结构：
- 自顶向下：`(IM平台) -> 消息入口层 -> Agent应用 -> 工具层/会话层/记忆层 -> 基础设施<JSON/客户端/多线程/消息队列等> -> 模型适配层 -> (模型接口)` 
- 消息入口层：对接IM平台（飞书/微信/TG/DC等）转化为内部消息
- Agent应用层：接收消息后调用AI模型，处理工具调用，管理多步执行流程
- 会话层：维护Agent与用户的一次沟通过程，支持持久化/自动压缩
- 长期记忆层：键值存储，会话间有效
- 模型适配层：适配Anthropic/OpenAI或其它格式API

## src/agent

