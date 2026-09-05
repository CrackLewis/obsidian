
## 版本变种、安装、使用

变种：
- Desktop：官方开发的桌面端，但很多功能疑似不全
- *TUI*：最常见，终端伪图形界面
- CLI：命令行接口，不需要打开任何界面便可执行Agent会话
- WebUI：Web图形化界面

TUI+CLI安装：

```sh
npm install -g opencode-ai
```

输入`opencode`启动一个新会话

## 核心概念

Agent：有自主感知、推理、决策和执行能力的智能体

会话：Agent的工作单元，所有输入输出、工具调用、推理、文件读取结果都存储在会话中

模型：即LLM，提供推理决策能力

tools：工具，可供Agent调用执行。OC内置一部分tools，MCP server也提供外部工具

skills：一套预先编写好的、可加载的能力单元，为模型提供一或多种任务能力（如：科学调试、头脑风暴、TDD、前端设计等）

MCPs：全称MCP servers，第三方提供的外接工具服务器，可以是本地服务也可以是远程服务

## TUI命令速查

- 会话管理：
	- `/new`：退出当前会话，开启一个新会话
	- `/compact`：将当前会话做摘要压缩，从压缩后的会话继续工作
	- `/export`：导出会话历史
	- `/sessions`：切换会话
	- `/copy`：复制会话历史
	- `/fork`：拷贝当前会话的所有内容
	- `/rename`：重命名会话
	- `/share`：分享会话（效果未知）
	- `/undo`：撤销上一轮会话
- 资源管理：
	- `/models`：切换模型
	- `/agents`：切换Agent模式
	- `/skills`：管理已安装的skills
	- `/mcps`：管理已配置的MCP服务器
	- `/variants`：切换模型变体
- 其他：
	- `/exit`：退出当前会话并关闭OpenCode程序

## CLI命令速查

- 会话管理：
	- `opencode session`：管理当前工作区内的所有会话
		- `list/delete`：列出所有工作区内会话/删除某个会话
	- `opencode run <prompt>`：非交互式处理一个文本请求
		- `--format`：指定会话输出格式，默认文本，可选`json/xml`等
	- `opencode export`：导出一个会话的全部上下文为外部文件
	- `opencode import`：从外部文件导入一个会话
- 资源管理：
	- `opencode acp`：管理ACP（agent client protocol）servers
	- `opencode mcp`：管理MCP servers
	- `opencode providers`：管理模型提供商/凭据
	- `opencode agent`：管理Agent
	- `opencode models`
	- `opencode stats`
	- `opencode github`
	- `opencode plugin`
- 远程服务连接：
	- `opencode serve`：开启一个OpenCode服务器
	- `opencode attach`：连接到一个OpenCode服务器
	- `opencode web`
- 工具：
	- `opencode completion`
	- `opencode upgrade`
	- `opencode uninstall`
	- `opencode debug`：调试用
	- `opencode pr`
	- `opencode db`

