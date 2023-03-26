
<h1>SASS = Syntactically Awesome StyleSheets</h1>

功能：简化CSS的编写工作

VSCODE插件Easy Sass
- 安装
- 修改`Target Dir`到工作区的`css`子目录下，或者存放CSS文件的站点目录下

SASS文件：后缀`*.scss`，注意不是sass后缀。

## 基本用法

### 嵌套使用

```scss
.hyperbox {
	background-color: pink;
	.superbox {
		background-color: violet;
		.box {
			background-color: blue;
			.minibox {
				background-color: aqua;
			}
		}
	}
}
```

编译生成的CSS会将上述SCSS展开，成为正常的CSS样式。

### SASS变量

SASS支持自定义变量，以`$`开头，被引用时写作`$变量名`，被镶嵌入字符串时写作`#{$变量名}`。

```scss
$dark: #000;
$side: left;
.box {
	color: $dark;
}

.box2 {
	background: $dark;
	border-#{$side}-radius: 5px;
}
```

### 伪类/伪元素嵌套

格式：`&:伪类选择器`、`&::伪元素选择器`

```scss
.box {
	a {
		&:hover {
			color: red;
			font-style: underline;
		}
	}
}
```

### SASS mixin

定义一组复用度较高的样式，在任何需要使用该样式时，可以直接引入。

样式的定义可以带参，也可以不带。

```scss
@mixin mix_without_args {
	width: 200px;
	height: 200px;
}

@mixin mix_with_args ($width, $height) {
	width: $width;
	height: $height;
}

$arg-width: 50px;
.box {
	@include mix_without_args;
	.minibox {
		@include mix_with_args($arg-width, 50px);
		background-color: blue;
	}
}
```

### SASS extend

直接继承指定选择器名对应的样式。

**注意：继承操作会同时继承子选择器。所以慎重使用。**

```scss
.box1 {
	width: 200px;
	height: 200px;
	div {
		width: 100px;
	}
}

.box2 {
	/*会继承width/height和div子选择器*/
	@extend .box1;
}
```

### SASS import

可以导入其他的SASS文件。

如果同级目录下有`box1.scss`，则可以直接：
`@import "box1"`

### SASS 注释

SASS支持行内注释`//`，但在生成的任何形式的CSS中都不会保留

普通块状注释在压缩CSS中也不会保留

只有强制注释`/* ! */`才会被压缩CSS保留

### SASS 数学运算

支持四则运算。

**注意：除号会被CSS认为是合法的，所以需要加括号。**

```scss
.box {
	width: 50px + 50px;
	height: 100px - 50px;
	// 这里不能两个都带单位，否则是100px*px这种不合法的值
	margin-top: 10px * 10; 
	// css会将/认为是合法的，所以需要加括号
	padding-top: (100px / 2) ;
}
```

### SASS 行为逻辑

#### SASS if

通过条件判断给出特定的样式

```scss
.box {
	@if 1+1 == 2 {
		color: red;
	} @else if 1+1 == 3 {
		color: blue;
	} @else {
		color: pink;
	}
}
```

#### SASS for

```scss
@for $i from 1 through 5 { // [1,5]
	.col-#{$i} {
		width: 50px * $i;
	}
}

@for $i from 1 to 5 { // [1,5)
	.colw-#{$i} {
		width: 50px * $i;
	}
}

```

#### SASS each

```scss
$icons: success fail warning;
@each $i in $icons {
	.icon-#{$i} {
		background-image: url(../images/icons/#{$icon}.png);
	}
}
```

#### SASS while

```scss
$index: 6;
@while $index> 0 {
    .box-#{$index} {
        width: 5px * $index;
    }

    $index: $index - 2;
}
```

### SASS 自定义函数

```scss
$index: 6;
@function get-color($key) {
	@if $key > 5 {
		@return #000;
	} @else {
		@return #fff;
	}
}

body {
	background: get-color($index);
}
```