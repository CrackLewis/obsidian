
发送自定义HTTP请求

## demo：请求API示例

```python
import requests 
import sys
import os

PORT = 80
BASE_URL = f"http://127.0.0.1:{PORT}/v1/multiple_classification"

def option_init(args):
    resp = requests.request(
        method='POST',
        url=BASE_URL+"/init",
        json={'label_list': ['Q-1', 'Q0', 'Q1', 'Q2']}
    )
    print(resp.status_code, resp.json())

def option_load_predict(args):
    resp = requests.request(
        method='POST',
        url=BASE_URL+"/load_predict",
        json={'input_model_path': os.path.join(os.getcwd(), 'model.pickle')}
    )
    print(resp.status_code, resp.json())
```