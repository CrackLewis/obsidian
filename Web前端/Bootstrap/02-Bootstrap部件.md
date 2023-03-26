
## 按钮

![[Pasted image 20230326100042.png]]

```html
<button type="button" class="btn btn-primary">Primary</button>
<button type="button" class="btn btn-secondary">Secondary</button>
<button type="button" class="btn btn-success">Success</button>
<button type="button" class="btn btn-danger">Danger</button>
<button type="button" class="btn btn-warning">Warning</button>
<button type="button" class="btn btn-info">Info</button>
<button type="button" class="btn btn-light">Light</button>
<button type="button" class="btn btn-dark">Dark</button>

<button type="button" class="btn btn-link">Link</button>
```

- 重要级别：重要蓝，次要灰
- 事态级别：成功绿，危险红，警告黄，信息青
- 其他样式：明亮白，暗淡黑，链接透明

按钮组：一组

## 面包屑导航

```html
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="#">Home</a></li>
    <li class="breadcrumb-item"><a href="#">Library</a></li>
    <li class="breadcrumb-item active" aria-current="page">Data</li>
  </ol>
</nav>
```

![[Pasted image 20230326100518.png]]

`active`表示当前活跃页面，没有活跃链接。

**修改样式的原则在于：尽量避免自己创建标签。因为自己创建的样式的优先级往往不如Bootstrap的优先级高，所以可能无法覆盖。**

## 卡片

一种图片和文字的组合元素。

```html
<?--- width: 18rem; 属性是针对移动端的 ---?>
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```

结构：
- `.card`：卡片元素
	- `.card-img-top`：卡片顶部图片。
	- `.card-body`：卡片的下部内容。内部内容是可选的。
		- `.card-title`：卡片标题。`.card-subtitle`为卡片副标题。
		- `.card-text`：卡片内容。
		- `.card-link`：卡片链接。

## 轮播

幻灯片式部件。[官方文档介绍](https://v4.bootcss.com/docs/components/carousel/) 

```html
<div id="carouselExampleSlidesOnly" class="carousel slide" data-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
        <img src="..." class="d-block w-100" alt="...">
    </div>
    <div class="carousel-item">
      <img src="..." class="d-block w-100" alt="...">
    </div>
    <div class="carousel-item">
      <img src="..." class="d-block w-100" alt="...">
    </div>
  </div>
</div>
```

凭记忆做一个轮播属实有亿点难。这里贴出参考地址：
- [官方V4文档](https://v4.bootcss.com/docs/components/carousel/)
- [w3cschool](https://www.w3school.com.cn/bootstrap5/bootstrap_carousel.asp)

## 表单

WIP

## 模态框

一个悬浮于整个页面之前的元素。[官方文档](https://v4.bootcss.com/docs/components/modal/)

