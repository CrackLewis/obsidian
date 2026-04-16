
特点：
- 响应式布局。会随着浏览器视窗大小变换大小，可以兼容移动端。
- 全局划分为12列。可以通过`col-<响应级别>-<列数>`规定一个元素占用的列数。

## 布局方式对比

### 传统布局方式

| 布局方式 | 静态布局 | 流式布局 |
| --- | --- | --- |
| 概念 | 一般以固定宽度配合margin: auto来居中布局页面。一般只适用于PC端。 | 全部以百分比来设置宽度 |
| 优点 | 布局简单 | 有一定的适应性 |
| 缺点 | 不适配移动设备，浏览器缩小会出现横向滚动条 | 屏幕过小，会导致内容无法查看 |

### 响应式布局

概念：利用了[[03-Bootstrap布局#CSS媒体查询]] 的技术，来适配各种屏幕大小和设备的情况，采用不同的CSS代码来编写样式。一套HTML代码采用多套不同的CSS代码来使用，让不同的屏幕尺寸，达到不同的效果。

好处：完全适配所有的屏幕大小，用户有更好的体验感。

坏处：增加了一些开发成本。

## CSS媒体查询

媒体查询是Bootstrap获取媒体属性的方式。

[菜鸟教程 - CSS3多媒体查询](https://www.runoob.com/css3/css3-mediaqueries.html)

功能：在符合指定条件的设备上使用对应的样式替代原有样式。

栗子：（在宽度低于480px的显示器上设置淡绿背景）
```css
@media screen and (max-width: 480px) {
	body {
		background-color: lightgreen;
	}
}
```

Bootstrap的响应式容器源码：
```css
.container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

@media (min-width: 576px) {
  .container {
    max-width: 540px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 720px;
  }
}

@media (min-width: 992px) {
  .container {
    max-width: 960px;
  }
}

@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}
```

## 使用响应式容器|栅格系统

`.container`：响应式容器。

`.container-fluid`：全宽容器。

`.row`：行容器。行容器内包含若干列。

`.col`：列容器。可以指定占几列，最高12列，也可以指定在何种设备宽度下应用何种布局。

![[Pasted image 20230326143550.png]]

示例一：站点在992px以上宽度时分6栏，在768px以上时分4栏，在576px以上时分3栏，否则分两栏。
```html
<div class="container">
	<div class="row">
		<div class="col-12 col-sm-6 col-md-3 col-lg-2 demobox">col1</div>
		<div class="col-12 col-sm-6 col-md-3 col-lg-2 demobox">col2</div>
		<div class="col-12 col-sm-6 col-md-3 col-lg-2 demobox">col3</div>
		<div class="col-12 col-sm-6 col-md-3 col-lg-2 demobox">col4</div>
		<div class="col-12 col-sm-6 col-md-3 col-lg-2 demobox">col5</div>
		<div class="col-12 col-sm-6 col-md-3 col-lg-2 demobox">col6</div>
	</div>
</div>
```