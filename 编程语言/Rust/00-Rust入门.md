
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
| 缺省初始值  | 不允许                 | 允许           | ？                |
| 重新赋值   | 不允许                 | 允许（重新绑定）     | 允许               |
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

基本类型：
- 有符号整数、无符号整数
- 浮点数
- 布尔类型
- 字符类型（Unicode标量）
- 