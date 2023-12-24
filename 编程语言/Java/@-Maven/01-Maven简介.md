
## Why Maven?

管理项目的构建、报告和文档等步骤。

Maven不一定管理Java项目，还可以管理一些其他语言的项目。

功能：
- 构建、发布、分发
- 报告
- 依赖
- SCMs
- 文档生成
- 邮件列表

## Maven约定的项目配置

```yaml
- basedir: "存放pom.xml和所有子目录"
	- src:
		- main:
			- java: "项目的java源码"
			- resources: "项目的资源，比如property文件，springmvc.xml"
			- webapp:
				- WEB-INF: "web应用文件目录，web项目的信息"
		- test:
			- java: "项目的测试类"
			- resources: "测试用的资源"
	- target: "打包输出目录"
		- classes: "编译输出目录"
		- test-classes: "测试编译输出目录"
```

默认本地仓库目录为：`~/.m2/repository`

## Maven特点

- 项目设置统一
- 任意工程中共享
- 依赖管理包括自动更新
- 一个庞大且不断增长的库
- 可扩展，能够轻松编写插件
- 访问新功能需要极少配置
- 基于模型构建
- 项目信息的一致性站点
- 发布管理和发布单独的输出
- 向后兼容性
- 子项目可继承父项目依赖
- 并行构建
- 更好的错误报告

## 环境配置

要求：JDK版本不能太旧。。。

配置教程：[Maven 环境配置](https://www.runoob.com/maven/maven-setup.html)

