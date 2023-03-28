
第一段JS代码：
```js
document.write('Hello World!');
```

## 概念

JavaScript（JS）是：
- 轻量级解释性语言，也称脚本语言
- 可以运行在浏览器环境和其他的一些开发环境（Adobe、Node.js等）中

发展：
- 1995年网景公司设计：LiveScript，为啥叫JavaScript：因为发展中和Sun公司合作过，俗称蹭热度。。。
- 1996年，微软设计Jscript参与竞争
- 网景公司解散，ECMA接管JS
- 1999，ECMA统一Jscript和LiveScript，设计第三版JS（ECMAScript 3，简称ES3）
- 2009，ECMAScript 5，简称ES5，目前使用度最高。
- 2015，ECMAScript 2015，简称ES6，更新了一些新特性，放弃支持IE。
- 2015后每年一版，2022年为ES13。

## 核心组成

完整的JS语法：
- ECMA核心语法：I/O、变量、数据类型、控制结构、数组、函数
- 浏览器环境独有
	- BOM：浏览器对象模型
	- DOM：文档对象模型

## 运行环境

- Node.js：一套基于V8引擎的本地JS运行环境
	- 开发运行环境：VSCode（必选）、Code Runner插件（可选）
	- 特点：不支持BOM和DOM
- 浏览器：参见[[#站点引入JS的方式]]

## 站点引入JS的方式

- 内联JS：`<script>`标签内编写，建议放在`</body>`之前
- 引入JS：`<script src="源文件地址"></script>`。

## 输出

`document.write('内容')`
`console.log('内容')`
`alert('内容')`

## 变量

