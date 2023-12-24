
简介：基于Python的Web服务框架之一

## 基本配置

```bash
$ conda create -n eflask
$ conda activate eflask
```

在环境下安装所有Flask有关的依赖。不是所有的依赖都有用，但配置一个通用的Flask环境还是比较有意义的。

[[01A-Flask有关的依赖列表]]

## 基本Flask应用

Flask应用一般做成一个程序包。这样，虚拟环境下的`flask`命令程序可以启动它，外部程序通过`import`和`app.run()`也可以启动它。

常规Flask应用必备的内容：
- 应用对象、扩展对象、蓝图的定义。
- 一组视窗函数。
- 数据库模型。
- 表单模型。
- HTML模板。
- 静态文件。

其他可选的功能，如数据库迁移、日志、邮件等，由第三方软件包提供。

常规Flask项目的文件结构：
```yaml
workspace:
	myapp: "Flask应用目录"
		__init__.py: "应用初始化声明文件"
		models.py: "数据库模型文件"
		extensions.py: "扩展文件"
		forms.py: "表单文件"
		settings.py: "应用配置文件"
		blueprints: "蓝图目录"
			__init__.py: 
			main.py: "默认蓝图"
			*.py: "其他蓝图"
		templates: "模板目录"
			*.html: "模板文件"
		static: "静态目录"
			*.*: "静态文件"
	.flaskenv: "Flask应用的环境配置"
	requirements.txt: "应用的pip依赖文件"
```

## 第一个Flask应用

实际上Flask项目的结构很灵活，不一定需要包来管理。比如下面的单文件也可以完成类似的功能。

```python
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def view_index():
	return "Hello, Flask!"

app.run(port=21080)
```

运行时，访问`127.0.0.1:21080`，即在浏览器中显示`Hello, Flask!`。

## 学习资源

[Flask Mega Tutorial](https://luhuisicnu.gitbook.io/the-flask-mega-tutorial-zh/)

[Hello Flask by GreyLi](https://tutorial.helloflask.com/)

