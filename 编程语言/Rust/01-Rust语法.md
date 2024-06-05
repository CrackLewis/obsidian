
探讨一些更复杂的Rust语法。

## 组织管理

Cargo是Rust的包管理器，管理Rust项目的文件结构、构建过程等。

一个Rust包是一个或一系列Rust源程序的集合，生成一或多个可执行文件或库。包目录下有一个`Cargo.toml`记录包的详细信息。

Rust包下有两层结构：
- 箱（crate）：一个二进制程序文件或库文件。
- 模块（module）：一系列Rust语法单元组成的高阶单元，可以实现封装、层次组织和模块引入。

一个Rust包下可定义数个Rust箱，其中至多一个可以是库crate。程序crate对应一个目标可执行文件，可以是除了`src/lib.rs`外的任何文件；库crate对应一个可被其他Rust程序重用的库文件，只能是`src/lib.rs`。

下面是一个例子：假设某项目有一个目标程序（`main.rs`）、一个目标库（`lib.rs`），两者使用一些公共源码（`utils.rs`）。则源码可以这么组织：

```rust
my_project
├── Cargo.toml
└── src
    ├── main.rs   // 主crate的入口文件
    ├── lib.rs    // 另一个库crate的入口文件
    └── utils.rs  // 第三个库crate的入口文件
```

`Cargo.toml`内容如下：

```toml
[package]
name = "my_project"
version = "0.1.0"
edition = "2024"

[lib]
path = "src/lib.rs"

[[bin]]
name = "my_project"
path = "src/main.rs"

[dependencies]
utils = { path = "src/utils.rs" }
```

### 模块语法

Rust模块可以定义在源码文件的最外层或其他模块内部：

```rust
mod nation {
    mod government {
        fn govern() {}
    }
    mod congress {
        fn legislate() {}
    }
    mod court {
        fn judicial() {}
    }
}
```

### 访问模块

Rust模块的成员默认不可从外部访问，除非通过加`pub`关键字声明其为公开成员。

`pub`关键字修饰不同成员有不同的含义：
- `pub mod`：公开子模块，子模块对模块外部可见。模块成员仍然默认不可见。
- `pub struct`、`pub impl`：公开的结构体定义和实现，该定义对外可见。结构体成员仍然默认不可见。
- `pub enum`：公开枚举类，定义对外可见，但枚举成员默认不可见。

```rust
mod nation {
	// 公开模块：最外层可通过crate::nation::government访问
    pub mod government {
        pub fn govern() {}
    }

	// 私有模块：最外层不可见，模块内可见
    mod congress {
	    // 私有模块公开方法：模块内可见
        pub fn legislate() {}
    }
    
    mod court {
	    // 私有模块私有方法：模块内不可见
        fn judicial() {
	        // 合法
            super::congress::legislate();
        }
    }
}

fn main() {
	// 合法
    nation::government::govern();
    // 不合法
    nation::congress::legislate();
    // 不合法
    nation::court::judicial();
}
```

定位方式：
- 绝对定位：`crate::aaa::bbb::...`
- 相对定位：`super`访问上级模块，`::`向下定位。

```rust
mod back_of_house {
    pub struct Breakfast {
	    // 结构体的公开成员对外可见
        pub toast: String,
        // 非公开成员对back_of_house内部可见，对外不可见
        seasonal_fruit: String,
    }

    impl Breakfast {
        pub fn summer(toast: &str) -> Breakfast {
            Breakfast {
                toast: String::from(toast),
                seasonal_fruit: String::from("peaches"),
            }
        }
    }
}
pub fn eat_at_restaurant() {
	// 访问back_of_house模块的结构体方法
    let mut meal = back_of_house::Breakfast::summer("Rye");
    meal.toast = String::from("Wheat");
    println!("I'd like {} toast please", meal.toast);
}
fn main() {
    eat_at_restaurant()
}
```

### use声明

`use`声明用于简化模块访问，将一串名称简化为成员名：

```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting;
// 此情形下与use front_of_house::hosting同义

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

`pub use`声明可以*重导出*（re-export）`use`声明，使得模块外可以通过该声明简化访问：

```rust
mod external {
    mod front_of_house {
        pub mod hosting {
            pub fn add_to_waitlist() {
                println!("added!");
            }
        }
    }

    pub use front_of_house::hosting;
}

fn main() {
    external::hosting::add_to_waitlist();
}
```

为了避免别名冲突，`use...as...`可以为`use`声明的对象起一个别名：

```rust
#![allow(unused)]
fn main() {
	use std::fmt::Result; // 此处的use声明占用了Result，不能重复声明
	use std::io::Result as IoResult;
	
	fn function1() -> Result {
	    println!("func1");
	}
	
	fn function2() -> IoResult<()> {
	    println!("func2");
	}
}
```

### 模块分拆为不同源码文件

有时单个模块过于复杂，用单个源码文件很难表述其所有的定义与实现细节，此时需要将其分拆为数个源码文件。

源码文件的设置有两种方案：方案一是在`src`下创建一个模块目录和一个模块同名的`.rs`文件：

```
my_project
+ src
	+ main.rs
	+ my_module.rs
	+ my_module
		+ impl1.rs
		+ impl2.rs
```

方案二是`src`下只设置模块目录，目录内通过`mod.rs`文件描述模块结构。

```
my_project
+ src
	+ main.rs
	+ my_module
		+ mod.rs
		+ impl1.rs
		+ impl2.rs
```

`src/my_module/impl1.rs`有如下内容：

```rust
pub fn func1() {
	println!("called func1");
}
```

`src/my_module/impl2.rs`有如下内容：

```rust
pub fn func2() {
	println!("called func2");
}
```

`src/main.rs`有如下内容：

```rust
mod my_module;
pub use crate::my_module;

fn main() {
	my_module::switch(1);
	my_module::switch(2);
}
```

假如采用方案一，则需要编辑`src/my_module.rs`文件，对于方案二则需要编辑`src/my_module/mod.rs`文件。但这两个文件的内容是一致的：

```rust
// 目录下的所有子模块放这里。
// 如果模块需要开放外部访问，则加上pub关键字。
mod impl1;
mod impl2;

// 这里放模块的一级定义，即my_module的直接成员

pub fn switch(x: i32) {
	if x % 2 == 0 {
		impl1::func1();
	} else {
		impl2::func2();
	}
}
```

## 错误处理

### 不可恢复错误

Rust中不可恢复的错误非常简单粗暴，类似于C/C++中的`assert`宏。Rust中用`panic!`宏报告一个不可恢复的错误，同时强制退出程序：

```rust
fn main() {
	panic!("panic_test: {}", 1);
	println!("after_panic");
}
```

上述示例中，`after_panic`不会显示。

如果需要在报告这类错误时提供调用栈信息，则需要设置环境变量`RUST_BACKTRACE`为`1`。

### 可恢复错误

Rust内没有C++、Java、Python中所有的异常捕捉，取而代之的是一个`Result<T, E>`枚举：

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

该枚举常用于表示一个*可能失败的方法*的返回值。如果方法成功，则返回值为`Ok<T>`类型，否则为`Err<E>`类型。

例如，Rust标准库的`std::fs::File::open`函数便返回`Result<>`类型：

```rust
use std::fs::File;

fn main() {
    let f = File::open("hello.txt");
    if let Ok(file) = f {
        println!("File opened successfully.");
    } else {
        println!("Failed to open the file.");
    }
}
```

将一个可恢复错误*按不可恢复错误处理*，可以使用`Result<T,E>`的`unwrap`或`expect`方法。两者区别在于后者可以添加一段报错信息：

```rust
let f1 = File::open("hello.txt").unwrap();  
let f2 = File::open("hello.txt").expect("Failed to open.");
```

一个可能返回失败结果的函数，可根据执行是否成功决定返回`Ok`或`Err`：

```rust
fn f(i: i32) -> Result<i32, i32> {
	if i >= 0 { Ok(i) }
	else { Err(-i) }
}

fn main() {
	let x = -8;
	let x_abs = match f(x) {
		Ok(v) => v,
		Err(v) => v
	};
}
```

返回`Result`的函数还可以通过在`Result`中间值后加`?`。该写法表示：如果该中间值为`Err`类型，则直接返回该`Err`：

```rust
fn f(i: i32) -> Result<i32, bool> {  
    if i >= 0 { Ok(i) }  
    else { Err(false) }  
}  
  
fn g(i: i32) -> Result<i32, bool> {  
    let t = f(i)?;  
    Ok(t) // 因为确定 t 不是 Err, t 在这里已经是 i32 类型  
}
```

标准库内大部分使用到`Result`的场合，其`Err`类型都会提供一个`kind`方法说明*错误类型*，以免调用方不知道如何处理错误：

```rust
use std::io;
use std::io::Read;
use std::fs::File;

fn read_text_from_file(path: &str) -> Result<String, io::Error> {
    let mut f = File::open(path)?;
    let mut s = String::new();
    f.read_to_string(&mut s)?;
    Ok(s)
}

fn main() {
    let str_file = read_text_from_file("hello.txt");
    match str_file {
        Ok(s) => println!("{}", s),
        Err(e) => {
            match e.kind() {
                io::ErrorKind::NotFound => {
                    println!("No such file");
                },
                _ => {
                    println!("Cannot read the file");
                }
            }
        }
    }
}
```

## 泛型

Rust泛型类似于C++的模板系统和Java的泛型系统。

下面是一个函数泛型格式示例。参数`&[T]`表示以`T`为元素类型的数组，返回值为数组元素的最大值。

```rust
fn max<T>(array: &[T]) -> T {
    let mut max_index = 0;
    let mut i = 1;
    while i < array.len() {
        if array[i] > array[max_index] {
            max_index = i;
        }
        i += 1;
    }
    array[max_index]
}
```

结构体泛型：

```rust
struct Point<T1, T2> {
    x: T1,
    y: T2
}
```

枚举类泛型：

```rust
enum Option<T> {
    Some(T),
    None,
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

注意，如果结构体有`impl`块，则`impl`也必须用泛型修饰：

```rust
impl<T, U> Point<T, U> {
    fn mixup<V, W>(self, other: Point<V, W>) -> Point<T, W> {
        Point {
            x: self.x,
            y: other.y,
        }
    }
}
```

但*结构体实现特化*时则可以不用写（这个规定有点诡异。。）：

```rust
impl Point<f64> {
    fn x(&self) -> f64 {
        self.x
    }
}
```

## 特性（trait）

Rust特性类似于Java的接口，规定了符合这一特性的类型必须实现哪些成员方法，符合哪些规范。

特性的定义包括：
- 特性声明。格式为`trait my_trait`。
- 特性要求实现的方法定义或默认实现。参数列表必须为`(&self)`。

### 特性的定义

特性的定义示例：

```rust
trait Descriptive {
	// 提供默认实现
	fn desc_str(&self) -> String {
		String::from("<descriptive_object>")
	}

	// 不提供默认实现，则只提供定义
	fn desc_int(&self) -> isize;
}
```

结构体如需实现一个特性，则需要提供对应的`impl`块，格式为`impl...for...`：

```rust
struct Person {
	name: String
	age: u8
}

impl Descriptive for Person {
	fn desc_str(&self) -> String {
		format!("Person(name={}, age={})", self.name, self.age)
	}

	fn desc_int(&self) -> isize {
		self.age as isize
	}
}
```

### 特性作为函数参数

函数参数可以要求传入*实现了指定特性的结构体*，类型表示为`impl <trait_name>`：

```rust
fn output(object: impl Descriptive) {
    println!("{}", object.desc_str());
}
```

这种语法和泛型写法是等价的：

```rust
fn output<T: Descriptive>(object: T) {
	println!("{}"), object.desc_str();
}
```

如果要求对象*实现数个特性*，可以用`+`连接：

```rust
fn some_function<T: Display + Clone, U: Clone + Debug>(t: T, u: U) {
}
```

也可以通过`where`关键字将泛型的*限定后置*：

```rust
fn some_function<T, U>(t: T, u: U)
	where T: Display + Clone, U: Clone + Debug {
}
```

### 特性作为返回值

特性作为函数返回值的语法为`fn <func_name>(<arglist>) -> impl <impl_name>`。尽管写法上，特性看似允许返回任意符合该特性的对象，但实际上只能返回一种实现了该特性的对象：

```rust
fn person() -> impl Descriptive {  
    Person {  
        name: String::from("Cali"),  
        age: 24  
    }  
}
```

比如这种写法就是错误的：

```rust
fn some_function(bool bl) -> impl Descriptive {
    if bl {
        return A {};
    } else {
        return B {}; // 类型错误，只能返回一个实现Descriptive的类型
    }
}
```

### 特性的有条件实现

特性可以与泛型结合，表示泛型必须实现某些特性才能提供对应的特性实现：

```rust
struct A<T> {}

// 只有T类型实现了特性B和C，A<T>类型才有对应的方法实现。
impl<T: B + C> A<T> {
    fn d(&self) {}
}
```

### 示例：求数组元素最大值

下面是求数组元素最大值的完整实现。

```rust
// 特性Comparable，要求符合特性的类型实现compare方法
trait Comparable {
    fn compare(&self, object: &Self) -> i8;
}

fn max<T: Comparable>(array: &[T]) -> &T {
    let mut max_index = 0;
    let mut i = 1;
    // 遍历数组，维护max_index
    while i < array.len() {
        if array[i].compare(&array[max_index]) > 0 {
            max_index = i;
        }
        i += 1;
    }
    // 返回最大值的引用
    &array[max_index]
}

impl Comparable for f64 {
    fn compare(&self, object: &f64) -> i8 {
        if &self > &object { 1 }
        else if &self == &object { 0 }
        else { -1 }
    }
}

fn main() {
    let arr = [1.0, 3.0, 5.0, 4.0, 2.0];
    println!("maximum of arr is {}", max(&arr));
}
```

## 所有权、生命周期

参考[[00-Rust入门#所有权|所有权]]章节。

所有权描述变量对值的持有关系。一个值在生命周期内只能被一个变量持有。值可以复制和移动，值的所有权也会随之复制和移动。

对于一个值而言，除了该值持有者以外，其他变量只能通过借用的方式使用变量。引用是一种典型方式，但需要考虑引用失效问题和悬垂引用问题：

```rust
{
    let r;
    {
        let x = 5;
        r = &x;
    } // x被删除，r悬空
    println!("r: {}", r);
}
```

还有之前遗留的一个问题，为什么这种引用不行？因为编译器不能判断返回的引用是否在使用时仍然有效，所以编译器的*借用检查器*（borrow checker）阻止它通过编译：

```rust
fn longer(s1: &str, s2: &str) -> &str {
    if s2.len() > s1.len() {
        s2
    } else {
        s1
    }
}
```

例如下面这个情形，等到访问结果的时候，引用必然已经失效了：

```rust
fn main() {
    let r;
    {
        let s1 = "rust";
        let s2 = "ecmascript";
        r = longer(s1, s2);
    } // s1,s2被删除，r悬垂

	// r为无效引用，不能被访问
    println!("{} is longer", r);
}
```

### 函数生命周期标注

**注意**：新版本的Rust可以自动推断一些涉及引用参数的声明周期情形（例如单参数，单返回值），所以不是每个涉及引用参数的函数都必须标注生命周期。

为了解决返回引用可能无效的问题，Rust允许在函数声明部分添加*生命周期标注*，确保返回值的有效期不会长于引用参数的有效期。参数的标注称为*输入生命周期*，返回值的标注称为*输出生命周期*。

生命周期标注的语法为`'<label>`，一般对应一个引用参数的生命周期。下面这个示例要求，`max`函数的返回值生命期不超过任一参数的生命期。

```rust
fn max<'a, T: std::cmp::PartialOrd>(a: &'a T, b: &'a T) -> &'a T {
    if *a > *b { a }
    else { b }
}

fn main() {
    let a = 5;
    let b = 7;
    {
	    // 函数调用要求返回值不超过a,b的生命期
        let t = max(&a, &b);
        println!("{}", t);
    }
}
```

假如不同的引用参数对应不同生命周期，函数声明也支持*标注多个生命周期*，但要求必须通过`'<l1>: '<l2>`的方式描述不同周期的层次关系，表示`<l1>`的生存期不短于`<l2>`。

注意，这种层次关系只用于限定返回值生命期，不能检查各引用参数的生命期长短关系。

```rust
fn max<'a, 'b : 'a, T: std::cmp::PartialOrd>(va: &'a T, vb: &'b T) -> &'a T {
	// 形式上规定'b>='a，要求参数为最短的'a
    if *va > *vb { va }
    else { vb }
}

fn main() {
    let b = 5;
    {
        let a = 7;
        let t = max(&a, &b);
        {
            println!("{}", t);
        }
    }
}
```

如果函数标注了生命周期，就一定要使用，否则报错。

### 结构体生命周期标注

结构体定义也可以携带生命周期标注，表示结构体生命期不会超过标注对应的引用成员：

```rust
fn main() {
    struct Str<'a> {
        content: &'a str
    }
    let s = Str {
        content: "string_slice"
    };
    println!("s.content = {}", s.content);
}
```

带生命周期标注的结构体的实现也需要标注：

```rust
#![allow(unused)]
fn main() {
	struct ImportantExcerpt<'a> {
	    part: &'a str,
	}
	
	impl<'a> ImportantExcerpt<'a> {
	    fn announce_and_return_part(&self, announcement: &str) -> &str {
	        println!("Attention please: {}", announcement);
	        self.part
	    }
	}
}
```

### 静态生命周期

静态生命周期（`'static`）用于修饰一类引用，这类引用指向的值存活于整个Rust程序生命周期，程序初始化时，从静态数据区创建，程序退出时销毁。

所有的字符串字面量都是`'static`的。

```rust
let s: &'static str = "I have a static lifetime.";
```

## 迭代器、闭包

参考[[00-Rust入门#迭代器]]、[[00-Rust入门#闭包]]章节。

迭代器回顾：
- 四原则：惰性求值、消费性、不可变访问、所有权
- 三方法：`iter`、`iter_mut`、`into_iter`
- 通过迭代器处理数据：`map`、`filter`、`skip`、`take`、`enumerate`、`collect`、`fold`
- 复制容器数据：`cloned`

闭包回顾：
- 是一种特殊的函数
- 特点：性能高，生命期
- 捕获外界变量（`move`）
- 类别：`Fn`、`FnMut`、`FnOnce`
- 闭包作为参数和返回值

## 智能指针

智能指针指*独有或共有*数据的一类数据结构。与引用不同，引用只是借用数据。

智能指针都实现了`Deref`和`Drop`两个特性，规定了它们在被解引用和被删除时的行为。

最常用的智能指针：
- `Box<T>`：在堆内存创建一个值。
- `Rc<T>`：带引用计数器的指针。
- `Ref<T>`、`RefMut<T>`：通过`RefCell<T>`访问。

### Box\<T\>

`Box<T>`允许在堆上存储一个值。它尤其适合以下3个情形：
- 在需要确切大小的上下文中，使用一个编译时未知大小的值
- 希望数据移动时不变更所有权
- 只关心值的类型是否实现了特定特性，而非值的具体类型

堆上储存数据：

```rust
let b = Box::new(5); // Box<i32>
println!("{}", b); // 5
```

定义递归类型，如链表：

```rust
enum ListNode<T> {
	Cons(T, Box<ListNode<T>>),
	Nil
}

use crate::ListNode::{Cons, Nil};

fn main() {
	let list = Cons(
		1, Box::new(Cons(
		2, Box::new(Cons(
		3, Box::new(Cons(
		4, Box::new(Cons(
		5, Box::new(Nil
	)))))))))); // 什么Lisp
	
	let mut curr = list;
	// 遍历链表
	loop {
	    match curr {
	        Cons(v, nxt) => {
	            println!("Value: {}", v);
	            curr = *nxt;
	        },
	        Nil => {
	            break;
	        }
	    }
	}
}
```

### Deref trait

Rust不直接允许重载解引用运算符（`*`），但允许通过实现`Deref`特性的方式自定义解引用逻辑。在结构体`my_struct`前加星号实际上执行的是`*(my_struct.deref())`，所以只需要实现`deref`方法。

设自定义的智能指针为`MyBox<T>`类型，则其定义、实现如下：

```rust
struct MyBox<T>(T);

// new方法的实现
impl<T> MyBox<T> {
	fn new(x: T) -> MyBox<T> {
		MyBox(x)
	}
}

use std::ops::Deref;

// Deref特性的实现
impl<T> Deref for MyBox<T> {
	type Target = T;

	fn deref(&self) -> &T {
		&self.0
	}
}
```

注意：这只是一个概念模型，并没有实现有限结构体大小。

还有`DerefMut<Target=U>`特性，定义解引用一个可变对象的逻辑。

### Drop trait

