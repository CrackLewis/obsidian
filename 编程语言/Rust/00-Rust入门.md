
参考材料：
- [Runoob Rust](https://www.runoob.com/rust/rust-tutorial.html)
- 

相关网址：
- [Rust Playground](https://play.rust-lang.org/)：在线演示Rust

## 安装

略

## 例程

### HelloWorld

```rust
fn main() {  
    println!("Hello World!");  
}
```

### println Example

```rust
fn main() {
	let a = 12;
	let b = 7;
	// println!语句内的{}默认表示读取下一个元素并输出。
	println!("a is {}, a*2+3 is {}.", a, a * 2 + 3);
	// 想输出大括号，则需要通过两次大括号进行转义。
	println!("lbrace is {{, rbrace is }}.");
	// {k}表示输出第k个参数（下标为0）
	println!("a is {0}, a again is {0}, b is {1}, a yet another time again is {0}.", a, b);
}
```

## 基本语法

### 变量

Rust是强类型语言，但具有自动判断变量类型的能力，可根据变量声明的初始值推断变量类型。

Rust的广义变量（具名量）分常量、不可变变量和可变变量3类，区别如下：

| 项目     | 常量                  | 不可变变量        | 可变变量             |
| ------ | ------------------- | ------------ | ---------------- |
| 变量声明   | `const A: i32 = 1;` | `let x = 1;` | `let mut x = 1;` |
| 缺省初始值  | 不允许                 | 允许（必须指定类别）   | 允许（必须指定类别）       |
| 重新声明   | 不允许                 | 允许           | 允许               |
| 重新赋值   | 不允许                 | 不允许          | 允许               |
| 自修改运算符 | 不允许                 | 不允许          | 允许               |

由于Rust变量是强类型，所以可变变量不能赋为与初始值不同的类型，不可变变量和常量的初始值必须和声明类型相符。

例如：

```rust
let x = 10;
x = 11; // 错误：不能赋值给不可变变量
let x = 12; // 正确：重新绑定x=12

let mut y = 1;
y = 2; // 正确
y = "3"; // 错误：类型必须一致

let x = 10;
let x = x * 2; // 正确，x=20
let x = x * 2; // 正确，x=40

const A = 1; // 错误：常量必须指定类型
const A: i32 = 1; // 正确
const A: u64 = 2; // 正确
const a: i32 = 3; // 正确但警告：常量名建议大写
```

### 数据类型

类型：
- 基本类型：
	- 有符号整数、无符号整数
	- 浮点数
	- 布尔类型
	- 字符类型（Unicode标量）
- 复合类型：
	- 元组：类似Python元组
	- 数组：固定长度的同类型元素集合
	- 结构体：自定义数据类型，可以包含多种类型的字段
	- 枚举
- 寻址类型：
	- 引用
	- 指针
	- 智能指针
- 函数类型
- 切片类型
- 动态类型（`dyn Traits`）
- 空类型
- Never类型

#### 整数

整数细分为如下类型：
- 有符号：`i8`、`i16`、`i32`、`i64`、`i128`、`isize`
- 无符号：`u8`、`u16`、`u32`、`u64`、`u128`、`usize`

`isize`和`usize`的实际尺寸为主机的数据字长，32位主机为`i/u32`，64位主机为`i/u64`。

整数字面量：
- 十进制、十六进制与C/C++类似。
- 八进制采用`0o????`的格式：`114514=0o337522`。
- 二进制采用`0b????`的格式：`233=0b1110_1001`。
- 数位间允许用`_`隔断数位（`0x114_514`）。

#### 字符型

长度为4个字节，理论上可以存储Unicode和中文UTF-8字符。

不建议使用字符型存储UTF-8文本，建议使用字符串，否则容易出现编码问题。

#### 其他基本类型

布尔型只允许`true`、`false`。

浮点数分为`f64`、`f32`两种类型，字面量默认`f64`。

#### 复合类型简介

Rust复合类型包括元组、数组等。

元组是用一对`( )`包括的一组数据，可以包含不同种类的数据：

```rust
fn main() {
	let tup: (i32, f64, u8) = (500, 6.4, 1);
	// tup.0 等于 500
	// tup.1 等于 6.4
	// tup.2 等于 1
	let (x, y, z) = tup;
	// y 等于 6.4
}
```

数组是用一对`[ ]`包括的同类型数据：

```rust
let a = [1, 2, 3, 4, 5];
// a 是一个长度为 5 的整型数组

let b = ["January", "February", "March"];
// b 是一个长度为 3 的字符串数组

let c: [i32; 5] = [1, 2, 3, 4, 5];
// c 是一个长度为 5 的 i32 数组

let d = [3; 5];
// 等同于 let d = [3, 3, 3, 3, 3];

let first = a[0];
let second = a[1];
// 数组访问

a[0] = 123; // 错误：数组 a 不可变
let mut a = [1, 2, 3];
a[0] = 4; // 正确
```

### 注释

与C/C++不同的是，Rust支持三斜杠注释块。VSCode的Rust可以将这种注释块的内容以Markdown格式呈现为文档，Cargo doc也支持这种注解转换为文档。

```rust
/// Adds one to the number given. 
/// 
/// # Examples 
/// 
/// ``` 
/// let x = add(1, 2); 
/// 
/// ``` 

fn add(a: i32, b: i32) -> i32 { 
    return a + b; 
} 
    
fn main() { 
    println!("{}",add(2,3)); 
}
```

### 函数

Rust函数的常规定义为：

```rust
fn func_name(arg1: ty1, arg2: ty2, ...) -> ty_ret {
	func_body;
}
```

参数列表可有可无，但如果有参数，就一定要标明类型。

`-> ty_ret`表示函数的返回类型。原则上必须写返回类型，不过Rust也能自动推断。

函数示例：

```rust
fn prod(x: i32) -> i32 {
	let mut ret = 1;
	for i in 1..x:
		ret = ret * i;
	return ret; // 或者直接写ret
}
```

Rust有一种特殊语法叫*函数体表达式*，本质是大括号内一组语句，最后一句必为数值表达式：

```rust
let x = i32 { 5 };

let y = i32 {
	let mut ret = 1;
	for i in 1..11:
		ret = ret * i;
	ret
}; // 3628800
```

注意函数体和函数体表达式的区别：函数体表达式不能使用`return`语句；函数体既可以用`return`，也可以将最后一个语句的值作为函数返回值隐式返回。

### 条件语句

Rust条件语句分`if-else`和`match`语句。

`if-else`语句和C/C++中的`if-else`总体相似，有几处不同：
- 不强制要求条件表达式带括号（可带可不带）
- 分支子语句必须是组合语句（不能是单个语句）
- 语句本身是一个表达式，C/C++的对应语句则不是
- `if let`结构

例如：

```rust
let mut x = 2;
if x % 2 == 1 { // 条件表达式可不加括号
	x = 3 * x + 1;
}
else {
	x = x / 2;
}

if x > 1 x = 2; // 不合法，分支语句必须是组合语句

// 用if-else语句作为等号右端是合法的
// 类似C/C++的三目运算符
let y = if x % 2 == 1 { 3 * x + 1 } else { x / 2 };
```

`if let`是Rust中一种特殊结构，主要用于简化模式匹配语法。这里先不掰扯。

`match`语句类似于C/C++中的`switch-case`，但也有一些不同，同样留坑。

### 循环语句

循环语句分3种：
- `while`语句
- `for`语句
- `loop`语句

`while`语句与C/C++的`while`类似，区别在于条件表达式不必括起来，循环体必须为复合语句。

```rust
let mut x = 10;
let mut y = 0;
while x > 0 {
	y = y + x;
	x = x - 1;
}
println!("y = {}", y);
```

`for`语句则相当不同，只能在一个可迭代值内遍历，可以是数组迭代器或整数区间：

```rust
let a = [10, 20, 30, 40, 50];  
// [0,5)
for i in 0..5 {  
	println!("a[{}] = {}", i, a[i]);  
}  
// 遍历数组
for i in a.iter() {  
	println!("{}", i);  
}  
```

`loop`类似于`while(1)`，表示在跳出前一直循环：

```rust
let mut x = 1;
loop {
	if x >= 10 {
		break;
	}
	x += 1;
}
```

与`while`和`for`不同的是，`loop`语句可以充作赋值表达式的右端（尽管它实际不是表达式）：如果`loop`内的`return`语句通过加参数的形式带出一个值，它会作为表达式右端的值：

（感谢菜鸟教程让我薅羊毛）

```rust
fn main() { 
    let s = ['R', 'U', 'N', 'O', 'O', 'B']; 
    let mut i = 0; 
    let location = loop { 
        let ch = s[i];
        if ch == 'O' { 
            break i; 
        } 
        i += 1; 
    }; 
    println!(" \'O\' 的索引为 {}", location); 
}
```

### 迭代器

Rust迭代器的核心思想是：声明式访问数据容器，分离数据和处理数据的过程。

迭代器遵循的4原则：
- 惰性求值：只有必须求值时才求值。这样迭代器可处理不定长序列。
- 消费性：完成迭代的数据容器会被消费，不再可用。
- 不可变访问：迭代器默认不允许改变元素。
- 所有权：迭代器可以处理*拥有*（通过`into_iter`方法获取容器所有权）或*借用*（通过`iter`方法借用容器数据）

迭代器创造3方法：
- `iter_mut`：从容器借用数据，创建可变迭代器。（元素类型为可变引用）
- `iter`：从容器借用数据，创建不可变迭代器。（元素类型为引用）
- `into_iter`：创建获取所有权的迭代器。（元素类型为值）

例：

```rust
let a = vec![1, 2, 3, 4, 5];
for i in a.iter() {
	println!("element found: {}", i);
}

let mut b = vec![6, 7, 8];
for i in b.iter_mut() {
	println!("element found: {}", i);
}

let c: Vec<_> = a.into_iter().map(|x| x * x).collect();
for i in c.iter() {
	println!("element found: {}", i);
}
```

迭代器常用方法：
- `map()`：对每个元素应用给定的转换函数。
- `filter()`：根据给定的条件过滤集合中的元素。
- `fold()`：对集合中的元素进行累积处理。
- `skip()`：跳过指定数量的元素。
- `take()`：获取指定数量的元素。
- `enumerate()`：为每个元素提供索引。

## 留坑

- `if let`
- `match`