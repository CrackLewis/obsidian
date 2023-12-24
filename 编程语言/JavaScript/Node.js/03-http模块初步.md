
`const http = require("http");`

http是一个提供网络服务的内置模块，使JS有充当服务端的最低能力。与ASP.NET或者PHP不同，它不需要使用IIS或者Apache等第三方的Web服务器软件，而是可以自行提供Web服务。

> phpStudy：一个后端服务软件的演示小程序

## 服务器相关的概念

IP地址：互联网上每台计算机的唯一地址

域名：唯一对应一个IP地址，是IP的自然语言化描述

域名服务器：提供IP和域名之间转换服务的服务器

端口号：对应主机上的一个Web服务，每个服务占有一个或多个端口
- 80端口实际上可省略

## 案例：最基本的Web服务器

- 调用`http.createServer()`创建Web服务器实例
- 为服务器实例绑定`request`事件，监听客户端发送的网络请求
- 在指定的端口上启动Web服务器

```js
const http = require("http");
const server = http.createServer();

server.on("request", (req, res) => {
  const url = req.url;
  const method = req.method;
  const str = `Your request url is ${url}, and request method is ${method}`;
  console.log(str);
});

server.listen(15080, () => {
  console.log("server running at http://127.0.0.1:15080");
});
```

效果：浏览器访问本机15080端口，会一直加载中，但服务终端会显示有人访问。

`server.on`中的回调函数参数`req`：
- `req`：请求对象，包含一些与客户端相关的数据和属性
	- `req.url`：客户端请求的URL地址
	- `req.method`：客户端的method请求类型

上面的例子从本机浏览器访问，会一直显示url为/，method为GET。

> 如果需要演示POST请求，则需要Postman工具。

服务端若想正常响应客户端，则需要操作`res`参数。最简单的方法是执行一次`res.end(响应内容)`方法，以回复客户端。

如果响应内容有中文，则需要手动设置内容编码为`utf8`。具体操作：
```js
server.on("request", (req, res) => {
  const str = `問天地好在！`;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.end(str);
});
```

## 根据不同的请求地址响应不同内容

核心步骤：
- 获取请求的URL地址
- 设置默认的响应内容为404 Not Found
- 判断用户的请求是否为`/`或者`/index.html`（首页）或者`/about.html`（关于页面）
- 设置响应头，防止中文乱码
- 使用`res.end(content)`将内容响应给客户端

```js
server.on("request", (req, res) => {
	const url = req.url;
	let content = "<h1>404 Not Found</h1>";
	if (url === "/" || url === "/index.html") {
		content = "<h1>首页</h1>";
	} else if (url === "/about.html") {
		content = "<h1>关于</h1>";
	}
	res.setHeader("Content-Type", "text/html; charset=utf-8");
	res.end(content);
});
```

## 案例：实现一个极简Web服务器

核心思路图：
![[Pasted image 20230328180512.png]]

实现步骤：
- 创建基本的Web服务器
- 将资源的请求URL地址映射为文件的存放路径
- 读取文件内容并响应给客户端
- 优化资源的请求路径

```js
server.on("request", (req, res) => {
  const url = req.url;
  const fpath = path.join(__dirname, url);
  
  console.log(
    `Your request url is ${url}, and request method is ${req.method}.`
  );

  fs.readFile(fpath, "utf8", (err, data) => {
    if (err) return res.end("404 Not Found");
    res.end(data);
  });
});
```

<h1>大道至简</h1>
