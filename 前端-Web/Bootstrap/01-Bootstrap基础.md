
Bootstrap：最流行的HTML/CSS/JS框架，用于创建响应式、移动优先的网站

[Bootstrap中文网](https://www.bootcss.com/)

一堆花里胡哨的东西（bushi

本地开箱：
- 下载V4/V5生产文件：[V4](https://v4.bootcss.com/docs/getting-started/download/) 、[V5](https://v5.bootcss.com/docs/getting-started/download/)
- 将CSS中的`bootstrap.min.css`和`bootstrap.css`加入项目的css子目录下
- 将JS中的`bootstrap.bundle.js`和`bootstrap.bundle.min.js`加入项目的js子目录下
- 下载jQuery：[国内下载](https://www.jq22.com/jquery-info122) 
- 将`jquery-<版本号>.js`和`jquery-<版本号>.min.js`放到项目的js子目录下

HTML使用：
```html
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Document</title>
	<script src="./js/jquery-3.5.1.min.js"></script>
	<script src="./js/bootstrap.bundle.min.js"></script>
	<link rel="stylesheet" href="./css/bootstrap.min.css">
</head>
```
**注意：jQuery JS必须在Bootstrap JS前被引入。**

**注意：因为不同版本的Bootstrap功能差别迥异，请特别留意自己本地下载并使用的Bootstrap框架版本，以避免兼容性问题的产生。**
