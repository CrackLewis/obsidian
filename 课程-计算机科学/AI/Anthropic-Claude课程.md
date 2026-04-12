
ref: [Anthropic Skilljar](https://anthropic.skilljar.com/claude-with-the-anthropic-api)

outline:
- accessing Claude with Anthropic API
- prompt evaluation
- prompt engineering techniques
- tool use with Claude
- RAG and agentic search
- Claude features
- model context protocol (MCP)
- Anthropic apps
- agents and workflows

## 调用Anthropic API

### 一次完整的API调用流程

一次完整的调用流程：
- 发起API请求：
	- api\_key：
	- model：选用的模型
	- messages：对话历史
	- max\_tokens：模型的最大输出长度
- 服务器对API进行处理
	- tokenization
	- embedding：将token转换为向量，包含单词的语义信息
	- contextualization：根据每个token前后其他token，推断出每个token最有可能的含义，并对其embedding调整
	- generation：基于输入embedding序列，生成输出
- 返回请求：
	- message：输出文本
	- usage：API tokens用量
	- stop\_reason：停止原因（输出超限，自然停止，出现了预定义的终止序列）

### 手动API调用

```sh
$ pip install anthropic python-dotenv
```

将api\_key保存在`.env`中（此文件需要被VCS手动忽略）：

```sh
ANTHROPIC_API_KEY=xxx
```

然后编写请求代码：

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-0"

message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What is quantum computing? Answer in one sentence"
        }
    ]
)

# 提取API回复文本
message.content[0].text
```

由于Anthropic API不保存历史对话消息，所以**多轮对话**需要将完整对话历史（包括用户请求和回复）传入messages中：

```python
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text
    
# Start with an empty message list
messages = []

# Add the initial user question
add_user_message(messages, "Define quantum computing in one sentence")

# Get Claude's response
answer = chat(messages)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)

# Add a follow-up question
add_user_message(messages, "Write another sentence")

# Get the follow-up response with full context
final_answer = chat(messages)
```

### system prompt

system prompt定义了此次API调用中，模型会以何种方式、语调、角度回复请求

```python
system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""

client.messages.create(
    model=model,
    messages=messages,
    max_tokens=1000,
    system=system_prompt
)
```

将前文的chat函数和system prompt结合：

```python
def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }
    
    if system:
        params["system"] = system
    
    message = client.messages.create(**params)
    return message.content[0].text
```

### temperature

是一个`[0.0, 1.0]`内输入参数，控制输出的多样化程度：
- 低温度：文本处理、事实校验、coding支持
- 中等温度：摘要、解决问题
- 高温度：创作型任务、头脑风暴等

![[Pasted image 20260411154318.png]]

将温度作为参数传入请求：

```python
def chat(messages, system=None, temperature=1.0):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    
    if system:
        params["system"] = system
    
    message = client.messages.create(**params)
    return message.content[0].text
```

### 流式响应（response streaming）

逐步生成输出，而非让API一次性全部返回

流式响应时序：
- `MessageStart`：即将返回一个新消息
- `ContentBlockStart`：一个文本段的开始
	- `ContentBlockDelta`：实际生成文本的片段
- `ContentBlockStop`：
- `MessageDelta`：当前message已经发送完毕
- `MessageStop`：新消息结束

![[Pasted image 20260411155754.png]]

通过`client.messages.create`函数创建流式API调用：

```python
messages = []
add_user_message(messages, "Write a 1 sentence description of a fake database")

stream = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    stream=True
)

for event in stream:
    print(event)
```

或者使用`client.messages.stream`方法：

```python
with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages
) as stream:
    for text in stream.text_stream:
        print(text, end="")
        
    # 在所有text返回完毕后，可通过get_final_message方法获取完整文本
    full_msg = stream.get_final_message()
```

### 结构化生成

有时大模型需要处理结构化生成任务：只生成JSON/XML而不输出其他信息
- 尽管好的prompt+模型可以达成目标，但仍有概率输出无关内容

解决方案：
- 在`user`请求后构建一个`assistant`响应头，要求模型从该响应头开始补全
- 指定\`\`\`为终止序列，这样模型可以补全一个完整JSON

```python
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])

import json

# Clean up and parse the JSON
clean_json = json.loads(text.strip())
```

## prompt evaluation

*提示词评估*（prompt evaluation）是提示词工程的一个关键环节，用于帮助用户迭代提升提示词的效果
- 如果不对提示词进行“评估-加强”循环，可能会在实际上线时遇到问题

提示词评估pipeline：
- 