
## 包

包：第三方个人或团队开发的模块或模块集合

为什么需要包：基于内置模块封装的包可以提供更高级、更方便的API，极大提高开发效率。包和内置模块的关系类似于jQuery和浏览器内置API之间的关系。

从哪里下载：[npm](https://www.npmjs.com/) 官网，抑或是npm包管理器。

```bash
$ npm -v
```

## “调包侠”的一般玩法

- 使用npm安装需要的包
- 使用`require(包名)`引入第三方包
- 参考第三方文档完成自己的工作

安装包：
```bash
$ npm install moment
```

导入包：注意，安装时的名称就是导入时的名称。
```js
const moment = require("moment");
```

然后上官网读文档，用包，调程序。。。

## npm与包

初次装包后，目录下会多出：
- `node_modules`：第三方包的存放目录
- `package-lock.json`：配置文件，记录每个第三方包的下载信息

### 安装指定版本的包

```bash
$ npm i moment@2.22.2
```

版本号：点分十进制：`Major.Minor.Patch`
- `Major`：大版本号
- `Minor`：功能版本号
- `Patch`：Bug修复版本号

## 包管理配置文件

配置文件：`package.json`，该文件记录与项目有关的一些配置信息：
- 项目的名称、版本号、描述
- 项目的包依赖
- 哪些包只用于开发，哪些包用于开发和部署

多人协作管理包时，不需要一同管理第三方包。

### 快速创建配置文件

```bash
$ npm init -y
```

**注意：只有英文目录名才可以正确初始化配置文件。**

### dependencies节点

在首次安装第三方包时，会添加该节点，记录第三方包的依赖信息。

特别地：`devDependencies`节点下的包只会在开发阶段使用，正式上线后不会使用。

```bash
// 安装到devDependencies中
$ npm i package-name -D
$ npm i package-name --save-dev
```

### 根据配置文件安装所有依赖

拿到一个删除了`node_modules`的项目之后，需要先下载所有依赖。

直接执行`npm install`命令即可。

### 卸载包

```bash
$ npm uninstall package-name
```

### 解决下包速度慢的问题

npm默认使用国外源，国外源限制了下载速度。

备选国内源：
- 淘宝npm镜像服务器
- 。。。

切换npm下载镜像源：
```bash
// 查看当前的下包镜像源
$ npm config get registry
// 将下包镜像源设置为淘宝镜像源
$ npm config set registry=https://registry.npm.taobao.org/
// 检查镜像源是否下载成功
$ npm config get registry
```

**nrm**：下包镜像源切换工具

```bash
$ npm i nrm -g
// 切换到淘宝镜像
$ nrm use taobao
// 切换到官方镜像
$ nrm use npm
```

**注意：个人实测nrm时遇到过依赖问题。慎用。**

## 包的分类

- 核心依赖包：开发期间和上线期间都会使用
- 开发依赖包：只在开发期间被使用

### 全局包

```bash
$ npm install global-package-name -g
```

可被本机命令行直接访问调用的包称为全局包。全局包一般都是工具性质。

### 全局包示例：i5ting_toc

一个将Markdown转换为HTML页面的小工具。

```bash
// 安装为全局包
$ npm install -g i5ting_toc
// 调用以转换文件
$ i5ting_toc -f src.md -o
```

## 规范的包结构

- 必须以单独的目录存在
- 顶级目录必须包含配置文件`package.json`
- 配置文件必须有`name`、`version`、`main`属性，表示名称、版本、包的入口

## 编写和维护包

### 初始化包的基本结构

在包目录下，初始化如下文件：
- `package.json`：包配置文件
- `index.js`：包的入口文件
- `README.md`：包的说明文档

`package.json`应遵循如下格式：
```json
{
	"name": "mytoolkit",
	"version": "1.0.0",
	"main": "index.js",
	"description": "A series of useful tool functions.",
	"keywords": [ "utility", "toolkit" ],
	"license": "ISC"
}
```

### 不同的功能进行模块化拆分

考虑将具有不同功能的方法放到不同的模块中。例如下面的`index.js`：
```js
const feat1 = require("./src/feat1.js");
const feat2 = require("./src/feat2.js");

module.exports = {
	feat1.func11,
	feat2.func21,
	feat2.func22
};
```

### 编写包的说明文档

安装方式、导入方式、格式化时间、功能描述、开源协议

### 发布包

注册npm账号并邮箱验证激活

终端内登录npm账号：`npm login`

发布包：`npm publish`

删除已发布的包：`npm unpublish package-name --force`
- 只能在发布72h以内删除，且删除后24h内不能重复发布

## 模块的加载机制

模块首次加载后会存到缓存中，之后会优先从缓存加载此模块。

同名情形下，内置模块的优先级最高。

加载自定义模块时，必须使用相对路径，开头必须用`./`或`../`的形式，否则会被当做内置模块或第三方模块。

使用`require()`加载自定义模块时，如果省略扩展名，会按如下顺序尝试加载：
- 确切的文件名
- 补全`.js`
- 补全`.json`
- 补全`.node`

如果模块名不是相对路径，则按照如下顺序尝试加载：
- 查找同名内置模块
- 从当前模块父目录的`/node_modules`加载模块
- 移动到上一级目录查找，直到文件系统的根目录