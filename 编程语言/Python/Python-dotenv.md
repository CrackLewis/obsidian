
```sh
$ pip install python-dotenv
```

不通过命令行环境，将存储于本地文件内的环境变量设置加载到Python程序中，程序可通过`os.getenv(var, default?)`访问

## demo：用例1

假如需要从`.env`加载如下环境变量：

```
LLM_MODEL_ID="qwen-plus"
LLM_API_KEY="sk-xxx"
LLM_BASE_URL=""
```

在当前路径执行下列代码：

```python
from dotenv import load_dotenv
import os

load_dotenv()

# 输出：LLM_MODEL_ID=qwen-plus
print("LLM_MODEL_ID=", os.getenv("LLM_MODEL_ID", "unknown-model"))
```

