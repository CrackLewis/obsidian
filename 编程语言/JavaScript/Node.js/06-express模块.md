
```bash
// 建议指定版本号，黑马教程用的是4.17.1
$ npm install express
```

```js
const express = require("express");
```

## 简介

express是基于Node.js平台，快速、开放、极简的Web开发框架。

相比之下，原生的http模块更贴近于底层，在Web开发方面效率较低。基于http封装的Express模块的开发效率更高。

## 基本使用

```js
const express = require("express");

const app = express();

app.listen(80, () => {
	console.log("express server running at http://127.0.0.1");
});
```

### 监听GET请求

```js
app.get("/", (req, res) => {
	res.send({ url: req.url, page: "index" });
});
```

### 监听POST请求

```js
app.post("/", (req, res) => {
	res.send("success: " + req.query);
});
```

### 获取更详细的请求信息

`req.query`：URL查询信息

例如：`localhost/name=john&age=20`访问时，产生的`req`的`query`为`{ name: "john", age: 20 }`。

### 动态参数

```js
app.get("/user/:id", (req, res) => {
	console.log(req.params);
	res.send(req.params);
});
```

访问`/user/john`，返回`"john"`。

### 托管静态资源

对外开放`public-path`目录下的文件访问：
```js
app.use(express.static("./public-path"));
```
访问`localhost/index.html`，即相当于`./public-path/index.html`。

如果托管多个目录，则多次调用`express.static`方法即可。如果文件在第一个目录找到，就不会在第二个目录找。

挂载路径前缀：
```js
app.use("/public", express.static("./__public"));
```
访问`localhost/public/index.html`，相当于访问`./__public/index.html`。

## nodemon

目的：监听项目文件变动，如果变动则立刻重启项目，方便调试。
```bash
$ npm i -g nodemon
// 使用nodemon而不是node启动项目，可以实现修改即重启的功能。
$ nodemon index.js
```

## Express路由

路由本质上是一组映射关系。

在Express中，它特指**客户端请求**和**服务器处理函数**之间的映射关系。
```js
app.请求方法(请求路径, 处理函数);
```

路由匹配：请求到达服务器后，依次和各声明的路由比对匹配，如匹配成功，则将该请求转交给处理函数。

### 路由的模块化

路由模块化步骤：
- 创建路由模块对应的JS文件
- 调用`express.Router`方法创建路由对象
- 向路由对象挂载具体路由
- 使用`module.exports`共享路由对象
- 使用`app.use`注册路由模块

路由模块实例：
```js
var express = require("express");
var router = express.Router();

router.get("/user/list", (req, res) => {
	res.send("get");
});
router.post("/user/add", (req, res) => {
	res.send("post");
});

module.exports = router;
```

主模块实例：
```js
var express = require("express");
const user_router = require("./router/user.js");

app.use(user_router);

app.listen(80, () => {
	console.log("q(≧▽≦q)");
});
```

### 路由模块统一添加前缀

```js
app.use("/user", user_router);
```

## Express中间件

中间件（Middleware）：