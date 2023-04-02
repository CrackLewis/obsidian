
## 输出

- `window.alert(内容)`
- `console.log(内容)`
- `document.write(内容)`
- `ele.innerHTML = 内容`

## 语句

```js
var x, y, z;
x = 22;
y = 11;
z = x + y;
```

## 基本概念

值：
- 变量值：变量
- 混合值：字面量
	- 整型
	- 实型
	- 字符串

运算符

表达式：值、变量和运算符的组合

关键词：动作标识词

注释：解释作用的源码部分，对运行无影响，`//`或`/* */`形式均可。

标识符：命名变量的合法名称
- 由字母、数字、下划线、美元符号组成
- 首字符不能是数字
- 不能使用关键字
- 大小写敏感

函数：可调用对象。封装了一组语句。

## 变量

声明变量：
```js
var x, y = 8, z = y;
// x = undefined, y = 8, z = 8
```

通过`var`重复声明变量没有任何影响，但如果声明重新赋值，则赋值是有效的。
```js
var i = 7;
for (var i = 0; i < 10; ++i) {
	// some statements
}
// i = 10 here
```

`let`声明作用域严格变量，拥有比`var`变量更多的限制。

`const`声明常变量，必须声明时一次赋值。常量不能整体修改，但有一些特例：比如常量数组的元素值允许通过赋值修改。

不能通过`let`和`const`在同一作用域内重复声明变量。通过`let`和`const`声明的变量也不能通过`var`在同一作用域内重复声明。

### 变量的作用域

- 全局作用域：外部声明的变量可在全局被访问。
- 函数作用域：函数内声明的变量可在函数内被访问。
- 块作用域：通过`let`和`const`声明的变量拥有块作用域。

```js
var vglob = 1;
// vglob = 1

function demo() {
	// vglob = 1
	var vfunc = 2;
	// vfunc = 2
	{
		let vblock = 3;
		// vblock = 3
	}
	// vblock = undefined
}
```

### var声明提升

```js
// 可以使用x
var x;

// y = undefined
var y = 6;
// y = 6
```

`var`变量声明总是会被提升到函数顶端。

**注意：变量提升机制只会提升声明，不会提升赋值。**

## 运算符

- 算术运算符：四则+取模、幂运算（`**`，ES2016新增）
- 自增或自减
- 赋值：`=`、四则和取模`=`
- [[#比较运算符]]
- 逻辑运算符：逻辑与、逻辑或、逻辑非
- 类型运算符：`typeof`、`instanceof`
- [[#位运算符]]：位与、位或、位非、异或、零填充左移、零填充右移、有符号右移

### 运算符优先级

[Mozilla提供的优先级说明和完整优先级表](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Operator_Precedence)

常见的优先级比较：后缀递增递减>前缀一元运算（逻辑非、位非、前缀增减）>乘除模>加减>位移>比较>位与位或和异或>逻辑与和逻辑或>赋值>逗号

### 比较运算符

除了常见的6种比较以外，JS特有两种：
- `===`：同类型且相等
- `!==`：不同类型或者不同值

数值间比较按照值的大小决定比较结果。

字符串间比较按照字典序返回结果。

两个对象之间比较将始终返回“不相等”，即使属性和值完全一致。

不同类型间运用6种经典比较运算符，会产生不可预料的结果，因此只能用`===`或`!==`比较。
```js
var b1 = false;
var b2 = new Boolean(false);

b1 == b2; // false
b1 === b2; // false
b1 !== b2; // true
```

### 位运算符

所有位运算都是32位。

## 数据类型

### 值类型
- 数值：64位浮点值
- 字符串值
- 布尔值
- 数组
- 对象
- 空值或未定义：空值等值于未定义，但不同类

### typeof类型名
- `number`：数值
- `string`：字符串值
- `boolean`
- `object`：对象值和数组在JS内部是一致的
- `undefined`：未定义
- `null`：空值
- `function`：函数

## 函数

```js
function 函数名(参数1, 参数2, ...) {
	语句组;
}

// 简写的箭头函数：没有名称，常用于函数传参
(arg1, arg2, ...) => {
	stmts;
};
```

## 对象

任意多个属性的组合体，每个属性有一个属性值。

定义：
```js
var obj = {
	attr1: 1,
	attr2: "attr2",
	attr3: function (a, b) {
		return a + b;
	}
};
```

访问某个属性：
```js
obj.attr1; // 1
obj["attr2"]; // "attr2"
obj.attr3(2, 3) // 5
obj.attr3 // function (a, b) { ... }
```

**注意：不要把数值、布尔值和字符串值声明为对象。否则有你好果子吃。**

### this关键词

`this`在函数定义中引用该函数的所有者。
- 对象方法：所有者对象
- 单独情形：全局对象
- 函数：全局对象
- 严格模式的函数：`undefined`
- 事件：接收事件的元素

尽管`this`可以绑定到所有者对象，但对象方法内的`this`是和方法而非对象绑定的。

```js
var person1 = {
  fullName: function() {
    return this.firstName + " " + this.lastName;
  }
}
var person2 = {
  firstName:"Bill",
  lastName: "Gates",
}
person1.fullName.call(person2);  // 会返回 "Bill Gates"
```

## 字符串

由一对单引号或双引号包裹的文本。

```js
"Johnson";
'Billy Wellington';
"Nested 'quotes'";
'Escape: \r\t\n\b\f\v'
```

字符串内换行：
- 用一个反斜杠。这种方法不是ES标准方法。
- 字符串加法。更安全，但有一点慢。

字符串可以被声明为对象。但尽量不要这么做。

[[002A-JavaScript字符串API]]

## 数值

数值统一使用64位浮点数：
- 符号位：1位
- 指数位：11位
- 系数位：52位，JS中整数可以精确到15位

十六进制数值用`0x`开头。不要单独使用前导零。

十进制科学计数法使用`AeB`的形式。

### 数值与字符串

**注意：尽量不要将数值与字符串直接相加。结果难于预测。**

一种可预见的情形是：数值加字符串将会产生拼接效果。

```js
20 + "30"; // "2030"
```

数值转字符串：
- `val.toString()`：通用方法
- `val.toExponential()`：转换为科学计数法
- `val.toFixed(digits)`：转换为小数点后`digits`位的字符串表示
- `val.toPrecision(digits)`：转换为小数点后`digits-1`位的字符串表示

非数值量转数值：
- `Number(val)`：通用方法
- `parseInt(str)`：解析第一个整数，失败返回`NaN`
- `parseFloat(str)`：解析第一个数值，失败返回`NaN`

### 保留值

`NaN`：表示一个非法数值。与任何非`NaN`数值比较都会返回`false`，`NaN`参与大部分运算都会产生`NaN`的结果。

判断是否为`NaN`可以使用全局函数`isNaN(val)`。

`Infinity`：表示一个无限大数值。任何有限数值都小于`Infinity`，都大于`-Infinity`。

一些保留数值属性：
- `Number.MAX_VALUE`：最大的有限数值
- `Number.MIN_VALUE`：最小的有限数值
- `Number.NEGATIVE_INFINITY`：负无穷
- `Number.POSITIVE_INFINITY`：正无穷

## 数组

数组是一系列元素的线性组合，是一种特殊对象。

数组的声明可以用列表形式或对象形式。但尽量避免用第二种。
```js
var arr1 = ["Saab", "Volvo", "BMW"];
var arr2 = new Array("Saab", "Volvo", "BMW");
```

访问元素用下标方法：
```js
var arr = ["Saab", "Volvo", "BMW"];
arr[0]; // "Saab"
```

因为数组是特殊类型的对象，所以：
- 元素类型可以不同。
- 可以扩容或缩小容量。
- 支持其他和对象相关的特性。

用`const`声明的数组：
- 声明时必须赋值，且不能整体重新赋值。
- **不是常量。**`const`数组语义是对数组的常量引用，所以修改内部元素的操作仍是允许的。
- 元素可以重新赋值。
- 具有块作用域。

更多详细内容，参见[[002B-JavaScript数组API]] 。

## 日期

```js
var d = new Date();
```

请参考 [[002C-JavaScript日期API]] 。

## 数学

请参考[[002D-JavaScript数学API]] 。

## 逻辑结构

### 条件逻辑：if-else语句

```js
if (cond1) {
	stmt1;
} else if (cond2) {
	stmt2;
} else if (cond3) {
	stmt3;
} else {
	stmt4;
}
```

### 条件逻辑：switch语句

```js
switch (cond) {
	case value1: {
		stmt1;
		break;
	}
	case value2: {
		stmt2;
		break;
	}
	...
	default: {
		stmtn;
		break;
	}
}
```

### 循环逻辑：for、for-in、for-of

普通`for`语句最简单，常见于各类高级编程语言：

```js
var x = 0;
for (var i = 1; i <= 100; ++i) {
	x += i;
}
x; // 5050
```

`for-in`、`for-of`用于对象内或数组内遍历元素：

```js
const person = {fname:"Bill", lname:"Gates", age:25};

let text = "";
for (let x in person) {
  text += person[x];
}
```

### 循环语句：while、do-while

`while`：先判断后执行
`do-while`：先执行后判断

```js
var cars = ["BMW", "Volvo", "Saab", "Ford"];
var i = 0;
var text = "";
 
while (cars[i]) {
    text += cars[i] + "<br>";
    i++;
}
```

### 跳转语句：break、continue

跳转语句用于改变程序的运行路径。

`break`可用于跳出循环语句或`switch`语句。

`continue`可用于**跳过一次**循环语句的执行阶段。

## 类型转换

转换到字符串：
- 万能：`toString()`。
- 类构造，不建议用：`String()`。
- 其他方法。

转换到数字：`parseInt()`、`parseFloat()`。

下面是一些特殊值的转换用例。**加粗的值**表示一般不希望出现的转换结果。

| 原始值           | 转换为数字 | 转换为字符串      | 转换为逻辑 |
| :--------------- | :--------- | :---------------- | :--------- |
| false            | 0          | "false"           | false      |
| true             | 1          | "true"            | true       |
| 0                | 0          | "0"               | false      |
| 1                | 1          | "1"               | true       |
| "0"              | 0          | "0"               | **true**     |
| "000"            | 0          | "000"             | **true**     |
| "1"              | 1          | "1"               | true       |
| NaN              | NaN        | "NaN"             | false      |
| Infinity         | Infinity   | "Infinity"        | true       |
| -Infinity        | -Infinity  | "-Infinity"       | true       |
| ""               | **0**        | ""                | **false**    |
| "20"             | 20         | "20"              | true       |
| "twenty"         | NaN        | "twenty"          | true       |
| \[ \]              | **0**        | ""                | true       |
| \[20\]             | **20**       | "20"              | true       |
| \[10,20\]          | NaN        | "10,20"           | true       |
| \["twenty"\]       | NaN        | "twenty"          | true       |
| \["ten","twenty"\] | NaN        | "ten,twenty"      | true       |
| function(){}     | NaN        | "function(){}"    | true       |
| { }              | NaN        | "\[object Object\]" | true       |
| null             | **0**        | "null"            | false      |
| undefined        | NaN        | "undefined"       | false      |

## 正则表达式

[[003-JavaScript正则表达式]]

## 异常

```js
try {
	statementWhichMightThrowExceptions();
	throw "I AM AN EXCEPTION";
} catch (ex) {
	statementDealingWithExceptions(ex);
} finally {
	afterwardStatements();
}
```

`throw`可以抛出大部分值作为异常，包括但不限于字符串、数组、对象、数值等。

### 内置Error对象

属性：
- `name`： 错误名
	- `EvalError`：历史遗留，旧版JS中`eval()`函数出错会抛出它。
	- `RangeError`：越界错误。
	- `ReferenceError`：非法引用。
	- `SyntaxError`：语法错误。
	- `TypeError`：类型错误。
	- `URIError`：在`encodeURI()`中发生的错误
	- 其他类型：部分浏览器或平台自行定义。慎用。
- `message`：错误信息

## 严格模式

```js
"use strict";
```

严格模式不允许的事项：
- 使用未声明的变量
- 使用`delete`删除变量或函数
- 函数的参数名重复
- 八进制数值
- 转义字符
- 写入只读属性或只能获取的属性
- 删除不可删除的属性
- 将`eval`、`arguments`用作变量名
- `with`语句
- `eval`语句内创建变量

其他事项：[Mozilla Strict Mode](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Strict_mode) 。

