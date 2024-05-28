
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

Rust是强类型语言，但具有自动判断变量类型的能力。