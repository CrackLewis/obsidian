
refs：
- 面试鸭

## toc

- 推理范式：
	- Plan-and-Execute
	- [[#ReAct推理范式|ReAct]]
	- [[#Reflexion推理范式|Reflexion]]

## 什么是AI Agent，和直接调模型API的区别

AI Agent是一类可以感知环境、拆解任务、调用工具、读取结果并根据环境进行决策的自主系统。

调API是一问一答/多问多答：
- 模型不能感知用户的工作环境
- 模型没有工具可用，不能帮助用户解决实际问题
- 除非是从官网或者Harness调，否则一般也没有主动决策的能力

AI Agent的核心差异：
- 循环执行能力：思考-行动-观察
- 外部工具调用能力：读文档、搜索、代码执行、数据库取数等
- 记忆：建立、检索、维护、完善、管理知识库/记忆库

演进路线：
- 2023-2024：prompt engineering
- 2023-2025：RAG
- 2023：雏形agent -- AutoGPT
	- OpenAI发布function calling格式
- 2024-now：agent技术成熟
	- 框架搭建工具：LangChain/LangGraph、CrewAI、AutoGen等
	- MCP：模型上下文协议，统一工具接入标准
	- Agent产品：
		- Coding Agent：Claude Code、Codex、OpenCode等
		- Claw类Agent：OpenClaw、Hermes等

## AI Agent核心组件

**4核心组件**：感知、决策、执行、记忆

感知：接收和理解外部信息

决策：一般接入LLM，理解和分析已有信息，制定执行计划/决策

执行：将决策转化为实际行动，如工具调用、代码执行、取数、调API等

记忆：让系统记住历史信息，以便未来复用

协作循环：
- 感知、记忆为决策提供依据
- 执行能够落实决策的细节，过程会积累记忆，并有可能影响感知

*决策能力*决定了Agent系统能力的上限，一般和依赖的LLM能力正相关

短期记忆、工作记忆、长期记忆：
- 短期记忆：不会跨会话生效的记忆，如中间结果、工具调用记录、会话上下文等
- 工作记忆：任务的结构化状态（待办列表、任务进度、中间变量等）
- 长期记忆：本地存档的知识库、记忆库等
	- 向量知识库、文档库等格式
- 各记忆间的调度：
	- 短期记忆中比较深刻/高价值的沉入长期记忆，长期记忆检索后变为短期记忆
	- 工作记忆一般限定于某个任务，承接短期和长期记忆的交接

感知模块的多模态扩展：读图片、看电脑屏幕或视频等

细节：
- 短期记忆满：上下文压缩、滑动窗口（保留近K轮）、检索式记忆
- 决策模块选错工具/调用失败：Agent错误恢复机制（K轮重新规划）
- 多Agent记忆共享：共享黑板模式、Agent间消息传递

## AI Agent的工具调用及其流程

负责Agent的执行层

工具调用基本流程：
- 向模型提供一个工具清单，包含每个工具的作用、参数、调用格式
- 模型会根据工具清单，在合适的时机输出调用工具的结构化JSON
- Agent解析JSON并执行调用
- Agent收集工具调用结果，并回传模型，等待模型进一步的决策

![[Drawing 2026-08-16 18.09.55.excalidraw]]

工具需要在desc中写明适合/不适合什么场景，避免LLM误调用：

```json
{
  "name": "search_web",
  "description": "搜索互联网上的最新信息，适合查询实时新闻、天气、股价等时效性内容。不适合查询稳定的知识性问题。",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "搜索关键词，尽量具体，包含时间和地点等限定信息"
      }
    },
    "required": ["query"]
  }
}
```

*工具调用实现方式*：
- 原生function calling：API层面提供tools数组定义工具列表
- prompt注入：system prompt内提供tool list
- MCP协议：统一调用格式

*工具调用的安全性*：安全网关（防注入/频率限制/操作审计）、沙箱等

细节：
- 工具调用参数格式不对：解析容错（JSON宽松解析/修复器）、有限次数重试
- 工具输出过长：应用层截断或摘要
- MCP vs function calling：前者解决工具怎么接入agent，后者解决模型怎么调工具
- 工具调用 vs RAG：RAG可理解为一种具备记忆/索引的特殊工具

## AI Agent的上下文窗口

*上下文窗口*（context window）是模型一次能处理的文本长度上限

上下文窗口的有关问题：
- agent是多轮执行的，会不断积累内容（system prompt、工具定义、对话历史、工具调用结果等），轻易达到窗口规模
- 窗口大不等于好用，一般1M上下文到达300-400k就开始流口水，具体表现为对大部分token不敏感，只对头尾部敏感
- 上下文长度越长，token越多，费用越高

上下文窗口的工程应对策略：
- *对话历史压缩*：调用模型总结上下文，将会话压缩为数百至数千token的摘要
- *工具结果截断*：在工具调用结果过长时，只提取关键信息
- *动态工具加载*：只加载和会话有关的tools

Agent级应对：滑动窗口、分层记忆（选择性沉入长期记忆）

## 如何处理超大的工具调用结果

三个阶段：
- 事前控制：在调用工具前限死返回规模
- 事中截断：拿到工具返回结果后，送入模型前，做结构化截断+数据统计处理，让模型知道结果全貌
- 事后摘要：另开一个空会话，让LLM总结调用结果

*分页加载策略*：对于文件系统/数据库等天然支持分页的数据源，设计工具时添加offset/limit参数，避免全量操作结果

*结构化截断技巧*：假如有5000条结构化行，取前5条让Agent理解格式，然后算所有字段的分位数/标准差/均值/最值

*引用机制与按需读取*：调用结果存入临时存储，只向模型提供ID，让模型按需读取

*多级压缩策略*：
- 第一级：工具层控制（设limit）
- 第二级：返回后结构化截断（只保留前10条+stats）
- 第三级：如果截断后仍超出上下文，做LLM语义压缩

*流式处理与提前终止*：不一次性返回全部结果，让Agent边看边判断（streaming模式），一旦遇到问题数据立刻停止

## Agent Loop

思考-行动-观察循环：
- 接收输入：用户请求+上一轮观察结果
- 推理决策：基于上下文思考并推断该做什么
- 执行行动：执行决策指定的工具调用并收集结果
- 观察和判断：将工具调用结果添加到上下文

细节：
- *最大迭代次数*：给agent一定的思考和决策空间，同时规避其走错误推理路径钻牛角尖
- Agent Loop vs Chain：chain是写死的固定流程，而loop是由LLM主导决策
- 常见的坑：
	- 上下文膨胀：
	- 工具调用失败处理：有限次数重试、错误恢复、策略回退等
	- 死循环检测：在循环层外检测，发现连续N轮相同便强制打断
	- token成本爆炸：压缩、滑动窗口、分层存储
	- 循环中一直做错误决策：循环加一个反思阶段

并发Loop：一次执行多个tool call，所有结果拼接后进入下一轮推理

## ReAct推理范式

ReAct = Reasoning + Acting

意义：将推理和行动结合

核心思想：
- 让模型每做一步之前，都想一想为什么
- 做完之后，想下一步怎么办

早期形式：

```
Thought: 用户想知道北京明天的天气，我需要调用天气查询工具
Action: get_weather(city="北京", date="202x-06-23")
Observation: 晴，最高气温 28°C，最低气温 15°C，东南风 2-3 级
Thought: 已经拿到了天气信息，可以给用户一个完整的回答了
Answer: 北京明天天气晴好，气温 15-28°C，东南风 2-3 级，适合户外活动。
```

现代agent的改进：
- 用tool call代替action
- 用模型内部的推理过程代替thoughts（如extended thinking、reasoning tokens等）

*ReAct局限性*：
- 正确性风险：本质是顺序推理，不会回顾整个执行过程，因此可能会累积错误
- 效率问题：简单操作不需要思考，过度思考会浪费token/污染上下文

*ReAct vs Plan-and-Execute*：
- 决策时机：P&E开头一次性规划完毕；ReAct边做边规划
- 灵活性：ReAct更灵活一些，能调整方向
- Token消耗：ReAct更高
- 适合场景：ReAct适合不确定环境，P&E适合确定环境
- 典型应用：ReAct适合问题排查/信息检索等；P&E适合批量数据处理/代码重构等

*Reflexion范式*：ReAct的改进
- 增加一个反思步骤，回顾整个过程并总结经验教训

细节：
- 如何防止thought越写越长：system prompt限制推理长度；拼接上下文时只保留action/observation，摘要或略过thoughts；利用模型自身的thinking/reasoning能力控制推理强度/模式
- 验证ReAct结果：给observation附加元信息用于校验；更激进地，引入validator agent审查结果
- ReAct vs function-calling：前者是推理范式，后者是action环节的一种实现

## Reflexion推理范式

ReAct + reflection

典型流程：执行-评估-生成反思-存储反思-重试

*Reflexion关键组件*：
- Actor：负责执行任务，本质上是一个ReAct Agent
- Evaluator：负责判断任务完成的效果，可以是自动化测试或者evaluator agent
- *Self-Reflection*：核心组件，根据执行过程+评估结果，生成一段自然语言的反思总结，指出“错在哪+咋错了+怎么改”
	- 决定整个推理范式的质量

*Reflexion vs ReAct*：
- 执行模式：ReAct单次执行，Reflexion多次尝试
- 有无记忆：Reflexion有长+短，ReAct只有短期
- 纠错方式：ReAct即时调整，Reflexion事后反思
- Token消耗：ReAct相对省token，Reflexion有额外的重试/反思开销（3-5x）
- 适用场景：ReAct简单-中等复杂度，Reflexion中高复杂度

应用：
- 失败重试时的经验注入：第一次尝试失败后，不是无脑重试，而是先分析失败原因，再把结论塞进上下文再重试
- 代码修复场景：代码测试不通后，将错误堆栈+源码一并发给模型反思
- 多轮优化场景：写文案、数据分析等，先做初版再自我评估+反思改进

提升纠错能力：
- 给一个明确的反思模板（尝试的目标+结果差在哪+为什么+怎么做）
- 外部验证机制：尽量不依赖agent自评，而是由第三方给评估结果
- 渐进式难度：先做简单子任务，攒够经验再做复杂任务

细节：
- 经验能够跨会话复用吗：可以
- 如果自评模型本身是LLM，如何避免自评偏差：使用不同模型；使用不同system prompt；要求给出失败/扣分理由，结合LLM+确定性检查（如静态程序等）
- 控制成本：用轻量级模型反思；简单任务用ReAct；限制反思轮数

## 设计终止条件

*优雅的终止条件*一般有三层：
- 自然终止：agent自行判断任务结束
- 硬性上限：设置最大迭代次数/token预算
- 模式检测：识别并中断异常行为（重复调用/若干轮无进展）

Agent陷入死循环的几种经典模式：
- 重复调用：agent反复调用同一个工具，参数一致，结果也一样，但agent不知道怎么往下走
- 乒乓型：在2-3个操作之间循环跳。本质是对任务全局理解不够
- 过度完善型：agent不断打磨已经够好的结果，反复改细节

*行动历史摘要机制*：每轮循环结束后，用几句话概括这一轮干了啥、结果咋样，是否存在异常模式/行为

细节：
- token预算管理：需要在agent内实现，对当前任务设置token预算，要求在预算内产出结果
- 多agent场景下的终止协调：
	- 背景：一个agent陷入异常，不能拖垮全局运行
	- 做法：设置orchestrator监控其他agent，观察到异常后可决定是否重试/换agent/降级返回
- 如果agent在即将满预算时，发现了突破性进展：适度增加预算/延长最大轮数
- 如何判断agent是否真的在推理：判断行动多样性+输出增量
- token预算快用完时，输出质量下降：在达到70%-80%预算时，便采用渐进式收敛，逐步减少每轮的系统提示长度，关闭非必要工具

## MCP协议是什么、解决什么问题

MCP = Model Context Protocol

由A畜在2024年底提出

核心目标：统一AI模型和外部工具/数据源间的连接方式

解决问题：工具和agent之间的集成困境
- MCP协议下，每个应用实现一个MCP server便可互相通信

细节：
- MCP server提供哪些能力：
	- tools：提供在线服务的接入能力，可被client主动调用，有名称、描述和参数结构
	- resources：提供只读上下文数据给模型
	- prompts：预定义的提示词模板
- why MCP：
	- 门槛低（JSON-RPC 2.0）：任何语言都能实现
	- 支持本地进程通信+远程Streamable HTTP
	- 生态推动力强：A/自己牵头做官方server，主流服务也有MCP server
- MCP vs function calling：后者只规定工具调用格式，前者额外处理了调用请求传输+服务发现+传输处理等，是端到端的协议
- server异常/超时怎么处理：返回错误信息，client/LLM决定有限重试/换工具/降级备用server/报告用户
- 本地stdio vs 远程HTTP：前者适合本地使用，如接入本地MCP server时直接和对应进程通信，不走套接字；后者适合团队共享/云端部署，如公司内部统一数据库

*MCP通信流程*：
- client启动时initialize握手，交换协议版本+能力列表
- client调用tools/list拿到server暴露的工具定义，包括：名称、描述、参数的JSON schema
- 用户提问后，模型根据工具描述决定具体的调用+参数
- client发送tools/call到server，server执行具体操作后返回结果
- client把结果喂回模型，模型继续后续工作

![[Drawing 2026-08-18 15.44.00.excalidraw]]

*MCP安全性设计*：
- 人机交互确认机制：敏感工具会要求弹窗确认，避免模型自作主张执行危险操作
- server能力边界由server自行声明，client可以选择性暴露哪些工具给模型
- 远程模式下支持OAuth 2.0鉴权，一个server服务多个用户，权限相互隔离

## MCP架构

客户端-服务端模型：
- Host：面向用户的AI应用，如CC/Codex/OpenCode/Hermes等
- Client：运行在Host内部，负责与server沟通的角色
- Server：提供能力的本地/远程MCP服务端

*MCP两种通信方式*：
- stdio：适用于在本地的MCP server，将MCP server作为子进程启动，通过pipe通信，延迟低
- Streamable HTTP：适用于远程共享的MCP server，通过HTTP请求/响应交互

细节：
- 能力协商机制：双方互相告知具备的能力，不会调用不存在的能力
- 安全模型与认证：互不信任
	- Host在调用工具前必须得到用户确认，如写/删除等敏感操作
	- 远程MCP server使用OAuth 2.0认证，只有授权client才能调用
	- server端对每个工具做细粒度权限控制，不因为认证过，便特许任何操作
- stdio和HTTP是否可以混用：可以

## A2A协议是什么

A2A = Agent-to-Agent

一种解决AI Agent间通信协作问题的开放协议标准，由Google于2025年发布

*A2A核心概念*：
- Agent Card：Agent名片，描述能力范围/交互模式/访问方式
- Task：Agent的工作单元，由一个Agent给另一个创建
- Message、Artifact：信息交换。前者用于消息传递，后者用于产物交付

A2A的取舍：选择不透明设计，Agent不对外暴露内部细节（模型/工具链/推理策略等）

A2A如何处理长任务：使用异步模式，调用方边推进边轮询进度，不需要阻塞等待

## A2A Agent Card

解决A2A Agents之间的发现、识别问题

主要包含内容：
- Agent名称和描述
- Agent擅长处理的任务类型
- Agent支持的输入输出格式、认证方式、通信端点地址

三阶段作用：
- 发现阶段：外部通过agent card了解可用agent
- 选择阶段：根据card描述选用合适agent
- 调用阶段：根据card声明的通信方式和认证要求发起请求

一个简化的Agent Card示例：
- skills是能力声明的核心
- capabilities是通信能力

```json
{
  "name": "数据分析 Agent",
  "description": "擅长数据清洗、统计分析和可视化，支持 CSV、Excel 和 SQL 数据源",
  "url": "https://data-agent.example.com",
  "version": "1.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "data-analysis",
      "name": "数据分析",
      "description": "对结构化数据进行统计分析并生成报告",
      "inputModes": ["text", "file"],
      "outputModes": ["text", "file"]
    }
  ],
  "authentication": {
    "schemes": ["OAuth2"]
  }
}
```

细节：
- A2A vs MCP：前者是agent对agent，后者是agent对tool/skill
- agent能力变化怎么处理：更新卡片，其他agent通过轮询/事件触发
- agent card中skills描述是自然语言，如何保证准确性：加标签体系；写得具体一些
- A2A安全性设计：在authentication字段声明认证方式；加上agent身份验证/请求签名/权限范围限制

## 上下文压缩策略

四种主流策略：
- 滑动窗口截断：只保留最近K轮对话
- 摘要压缩：在上下文容量将满时，调LLM压缩会话的早期阶段，替代完整历史。在保留关键信息的情况下，将token数降至20%，但会多一次LLM调用和数秒延迟，且会引入不稳定性
- 递进式摘要：每5轮做一次局部摘要
- 选择性保留：