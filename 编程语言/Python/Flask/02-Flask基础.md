
Flask基础：

## 路由、视窗函数

Web路由是Web应用的一种响应机制，当客户端对特定的地址发出特定类型的请求时，调用对应视窗函数进行响应。

一个路由对应一个视窗函数，一个视窗函数对应一或多个路由。

路由基于一个Flask应用或Flask蓝图。

```python
app = Flask(__name__)

@app.route("/", methods=["GET"])
@app.route("/root", methods=["GET"])
def view_root():
	return "ROOT"
```

视窗函数是一个响应用户请求的逻辑单位。该单位返回的值将作为响应返回给用户。

### 动态路由

路由允许带路径参数。

```python
@app.route("/<string:profile>", methods=["GET"])
def view_profile(profile: str):
	return "Profile: {}".format(profile)
```

## 请求

在视窗函数内可通过访问`request`对象访问当前请求。

请求有以下成员：

![[Pasted image 20230429221854.png]]
![[Pasted image 20230429221910.png]]

## 响应

常见的几种搭建响应的方式：
- 返回裸字符串
- 通过`render_template`方法渲染模板
- 通过`make_response`方法搭建响应