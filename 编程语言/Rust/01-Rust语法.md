
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

### 特性的动态分发

有时程序要求处理一类实现了特定`trait`的对象，但不知道这些对象是什么类别。这时需要通过`dyn`关键字声明为动态分发：

```rust
struct Circle { radius: i32 }
struct Square { border: i32 }
trait Drawable {
	fn draw(&self);
}

impl Drawable for Circle {
    fn draw(&self) {
	    let area = (self.radius * self.radius as f64) * 3.14159;
        println!("Circle r={}, S={}", self.radius, area);
    }
}

impl Drawable for Square {
    fn draw(&self) {
	    let area = self.border * self.border;
        println!("Square a={} S={}", self.radius, area);
    }
}

fn main() {
    let circle = Circle { radius: 5 };
    let square = Square { border: 6 };
    let shapes: Vec<Box<dyn Drawable>> = vec![Box::new(circle), Box::new(square)];
    for shape in shapes.iter() {
        shape.draw();
    }
}
// Circle r=5, S=78.53975
// Square a=6 S=36
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

### Deref特性：解引用逻辑

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

### Drop特性：删除逻辑

`Drop`特性允许用户自定义结构体被删除时的逻辑。

示例：

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
	// drop方法会在结构体被删除时调用
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer { data: String::from("my stuff") };
    let d = CustomSmartPointer { data: String::from("other stuff") };
    println!("CustomSmartPointers created.");
}
```

Rust不允许传统意义上的禁用`drop`逻辑。

Rust不允许显式调用`drop`方法。如果需要*提前释放对象*，则需要使用`std::mem::drop`方法：

```rust
fn main() {
    let c = CustomSmartPointer { data: String::from("some data") };
    println!("CustomSmartPointer created.");
    drop(c);
    println!("CustomSmartPointer dropped before the end of main.");
}
```

### Rc\<T\>

```rust
use std::rc::Rc; // 搞不懂，Box都能默认引入，Rc不行
```

`Rc<T>`适合用于在单线程程序中共享值的所有权。其基本原理是维护一个引用计数器，记录持有该值的指针数，当引用计数归零时删除值。

调用`Box::new(v)`会移动`v`值到指针`Box<T>`内，这是唯一创建`Box<T>`的方法。与其不同的是，`Rc::new(v)`和`Rc::clone(&p)`都可以创建`Rc<T>`，前者将`v`值移动到新的`Rc<T>`中，后者基于`p`创建一个共享值所有权的`Rc<T>`。

使用示例：

```rust
let pa = Rc::new(5);
let pb = Rc::clone(&pa); // pa.clone()也可以，但Rc::clone是惯用用法
let pc = Rc::clone(&pa);
```

`Rc::strong_count(&p)`可以获取引用计数：

```rust
enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};
use std::rc::Rc;

fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    println!("count after creating a = {}", Rc::strong_count(&a));
    // 此处打印1
    let b = Cons(3, Rc::clone(&a));
    println!("count after creating b = {}", Rc::strong_count(&a));
    // 此处打印2
    {
        let c = Cons(4, Rc::clone(&a));
        println!("count after creating c = {}", Rc::strong_count(&a));
        // 此处打印3
    }
    println!("count after c goes out of scope = {}", Rc::strong_count(&a));
    // 此处打印2
}
```

引用计数的自动减少，以及计数归零时值的销毁是`Rc<T>`对`Drop`特性自定义实现的行为。

注意：`Rc<T>`只提供*不可变的共享数值*。提供完全可变的共享数值可能违反变量借用规则，造成数据竞争和不一致。

### RefCell\<T\>、内部可变性模式

内部可变性模式指的是一种设计模式，它允许在持有不可变引用时也可改变数据。通用的做法是在数据结构中使用不安全代码模糊通常的可变形和借用规则。

借用规则：
- 任意时刻，只能有一个可变引用*或*任意个不可变引用*之一*
- 引用必须总是有效的

`RefCell<T>`确保同一时刻只有一个可变引用。这种确保是在运行时实现的，如果违反会导致程序错误退出。

如何选择`Box`、`Rc`、`RefCell`：

| 特点     | `Box<T>` | `Rc<T>` | `RefCell<T>` |
| ------ | -------- | ------- | ------------ |
| 所有者数量  | 1        | 多个      | 1            |
| 借用检查时期 | 编译期      | 编译期     | 运行期          |
| 可变性    | 不可变      | 不可变     | *内部可变*       |

下面是一个演示*内部可变性模式*的示例：

```rust
// Messenger特性：规定必须实现send方法
pub trait Messenger {
    fn send(&self, msg: &str);
}

pub struct LimitTracker<'a, T: Messenger> {
    messenger: &'a T,
    value: usize,
    max: usize,
}

impl<'a, T> LimitTracker<'a, T>
    where T: Messenger {
    // new方法是默认的构造方法
    pub fn new(messenger: &T, max: usize) -> LimitTracker<T> {
        LimitTracker {
            messenger,
            value: 0,
            max,
        }
    }

	// set_value是内部可变方法
    pub fn set_value(&mut self, value: usize) {
        self.value = value;

        let percentage_of_max = self.value as f64 / self.max as f64;

        if percentage_of_max >= 1.0 {
            self.messenger.send("Error: You are over your quota!");
        } else if percentage_of_max >= 0.9 {
             self.messenger.send("Urgent warning: You've used up over 90% of your quota!");
        } else if percentage_of_max >= 0.75 {
            self.messenger.send("Warning: You've used up over 75% of your quota!");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;

    struct MockMessenger {
	    // sent_messages用RefCell修饰，确保只有一个活动的可变引用
        sent_messages: RefCell<Vec<String>>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger { sent_messages: RefCell::new(vec![]) }
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
	        // 如果去掉borrow_mut()或者只使用borrow()，
	        // 这个语句便不能通过编译。
            self.sent_messages.borrow_mut().push(String::from(message));
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        let mock_messenger = MockMessenger::new();
        let mut limit_tracker = LimitTracker::new(&mock_messenger, 100);

        limit_tracker.set_value(80);

		// 这里的borrow()只借用不可变引用
        assert_eq!(mock_messenger.sent_messages..borrow().len(), 1);
    }
}
```

结合`Rc<T>`和`RefCell<T>`可以实现多个可变数据拥有者：

```rust
#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};
use std::rc::Rc;
use std::cell::RefCell;

fn main() {
    let value = Rc::new(RefCell::new(5));

    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));

    let b = Cons(Rc::new(RefCell::new(6)), Rc::clone(&a));
    let c = Cons(Rc::new(RefCell::new(10)), Rc::clone(&a));

// 图结构：
// 	b(6)
// 	 \
// 	  \
// 	   a(5) ---> NIL
// 	  /
// 	 /
// 	c(10)

    *value.borrow_mut() += 10;
    // 此时a的值变成了15

    println!("a after = {:?}", a);
    println!("b after = {:?}", b);
    println!("c after = {:?}", c);

// 输出：
// a after = Cons(RefCell { value: 15 }, Nil)
// b after = Cons(RefCell { value: 6 }, Cons(RefCell { value: 15 }, Nil))
// c after = Cons(RefCell { value: 10 }, Cons(RefCell { value: 15 }, Nil))
}
```

Rust标准库内的其他设施，如`Cell<T>`和`Mutex<T>`等也提供类似的功能，前者与`RefCell`的区别是不提供引用，而是将值移出和移入，后者则是提供互斥访问。

总结：
- `RefCell<T>`允许且仅允许借用一个可变引用，用于修饰值。
- `RefCell<T>`可与`Rc<T>`合用，从而支持借用多个可变引用。

### 引用循环问题

与C++的`std::shared_ptr<T>`类似，Rust也有引用循环问题。通过人为构造`Rc<T>`的循环引用，可以在Rust复现这个问题：

```rust
use crate::List::{Cons, Nil};
use std::rc::Rc;
use std::cell::RefCell;
#[derive(Debug)]
enum List {
    Cons(i32, RefCell<Rc<List>>),
    Nil,
}

impl List {
    fn tail(&self) -> Option<&RefCell<Rc<List>>> {
        match self {
            Cons(_, item) => Some(item),
            Nil => None,
        }
    }
}

fn main() {
    let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));

    println!("a initial rc count = {}", Rc::strong_count(&a));
    println!("a next item = {:?}", a.tail());
    // a initial rc count = 1 
    // a next item = Some(RefCell { value: Nil })

    let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));
    // 此时是b-->a，a还没有后继结点

    println!("a rc count after b creation = {}", Rc::strong_count(&a));
    println!("b initial rc count = {}", Rc::strong_count(&b));
    println!("b next item = {:?}", b.tail());
    // a rc count after b creation = 2
	// b initial rc count = 1
	// b next item = Some(RefCell { value: Cons(5, RefCell { value: Nil }) })

	// 构造a到b的指针，此时形成了引用循环
    if let Some(link) = a.tail() {
        *link.borrow_mut() = Rc::clone(&b);
    }

    println!("b rc count after changing a = {}", Rc::strong_count(&b));
    println!("a rc count after changing a = {}", Rc::strong_count(&a));
    // b rc count after changing a = 2
	// a rc count after changing a = 2

    // 运行这行代码会导致无休止的循环输出，并最终导致栈溢出
    // println!("a next item = {:?}", a.tail());
}
```

解决方案是，对部分可能产生引用循环的指针替换为`Weak<T>`类型，使得所有的`Rc<T>`不会形成一个环。这是一种类似于C++中`std::weak_ptr<T>`的设施，不会增加强引用计数（即`Rc::strong_count(&p)`的值）。

```rust
use std::rc::{Rc, Weak};
use std::cell::RefCell;

#[derive(Debug)]
struct Node {
    value: i32,
    // parent设为弱指针，破坏了引用循环
    parent: RefCell<Weak<Node>>,
    // children仍然为强指针
    children: RefCell<Vec<Rc<Node>>>,
}

fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
    });

	// Weak<T>可通过upgrade升级为Rc<T>
    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());

    let branch = Rc::new(Node {
        value: 5,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![Rc::clone(&leaf)]),
    });
    
	// Rc<T>可通过downgrade方法降级为Weak<T>
    *leaf.parent.borrow_mut() = Rc::downgrade(&branch);

    println!("leaf parent = {:#?}", leaf.parent.borrow().upgrade());
}
```

创建和销毁弱指针`Weak<T>`会改变弱引用计数（`Rc::weak_count`）。注意，弱引用计数只计算`Weak<T>`的个数，不包含`Rc<T>`的个数。

## 自动化测试

严格来讲测试不算语法，而算是Cargo的功能。

在项目下执行命令`cargo test`可以运行所有测试。

这是一个测试示例：

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn test1() {
        assert_eq!(2 + 2, 4);
        assert_ne!(2 + 2, 5);
    }
    #[test]
    fn test2() {
        let mut x = 1;
        for i in 1..11 {
            x *= i;
        }
        assert_eq!(x, 3628800);
    }
}
// 测试输出：
// running 2 tests
// test tests::test2 ... ok
// test tests::test1 ... ok
// test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
// running 0 tests
// test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

一个测试成功，当且仅当所有断言通过。

一个测试失败，可以由如下条件引起：
- 测试中间调用了`panic!`宏
- 至少一个断言失败

### 自定义测试运行

通过`--test-threads=xx`可以设置由多少个*并发线程运行测试*：

```bash
$ cargo test -- --test-threads=4
```

默认情况下，如果测试通过，测试中的标准输出不会显示。如果测试通过也要检查标准输出，可以加`--show-output`：

```bash
$ cargo test -- --show-output
```

通过指定测试名可以只运行部分测试：

```bash
$ cargo test test2 # 只运行tests::test2
```

如果一个测试在源码被标注为`#[ignore]`，则通过添加`--ignored`参数可以跳过这些测试：

```bash
$ cargo test -- --ignored
```

### 测试的组织结构

模块添加`#[cfg(test)]`表示，该模块只会用于测试，不会用于编译为库或二进制程序。

Rust允许测试私有函数，但不强迫用户测试私有函数：

```rust
pub fn add_two(a: i32) -> i32 {
    internal_adder(a, 2)
}

// 模块内的私有函数，对外不可见
fn internal_adder(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn internal() {
	    // 测试能够正常运行
        assert_eq!(4, internal_adder(2, 2));
    }
}
```

Rust项目下如果存在`tests`目录，则其内所有源码文件将视为测试文件，只会参与测试，不会参与编译。

## 面向对象编程特性

OOP哲学认为对象包含数据和行为。

OOP三大特征：封装、继承、多态

Rust只有两级封装：对模块外是否可见。

Rust不支持传统意义上的继承和多态，只允许通过`trait`的实现和动态分发机制实现。

## 专题

### 模式与匹配

模式包含如下内容：
- 字面量
- 解构的数组、枚举、结构体或者元组
- 变量
- 通配符
- 占位符

模式和匹配语法会在3个场合用到：
- `match`分支
- `if let`条件表达式
- `while let`条件循环
- `for`循环：可能涉及到变量解包，如：`for (idx, val) in it.enumerate()`。
- `let`语句：可能涉及到变量解包，如：`let (x, y) = (1, 2)`。
- 函数参数：同`let`，如：`&(x, y): &(i32, i32)`。

*可反驳性*（refutability）：模式可能匹配失败，则是可反驳的，否则是不可反驳的。

`let`、`for`、`match`、函数参数只允许不可反驳的模式匹配，因此下面这个`let`语句会失败：

```rust
// 报错：可反驳的模式，没有覆盖None
let Some(v) = return_some_or_none();
```

相反，`if let`、`while let`允许可反驳的模式匹配，如果模式匹配失败，则跳过语句块：

```rust
if let Some(v) = return_some_or_none {
	println!("Some!");
} // 匹配失败则跳过语句块
```

`if let`、`while let`也可以进行不可反驳的模式匹配，但通常不被提倡。

下面所有的模式语法都是合法的：
- 字面量：`1`、`2.0`、`true`
- 命名变量：`x`、`y`
- 多个模式：`1 | 2 | 3`
- 范围匹配：`1..=5`（匹配`[1,5]`，注意是闭区间）
- 解构结构体：`Point { x: a, y: b }`，成员`x,y`解构为变量`a,b`
- 解构枚举：`Some(v)`
- 解构嵌套的结构体和枚举（？）
- 解构结构体和元组：`(x, y)`、`((a, b), Point { x, y })`
- 忽略整个值：`_`
- 忽略部分值：`Some(_)`、`(x, _, y, _, z)`
- 忽略剩余值：`(a, b, ..)`、`(first, .., last)`

*匹配守卫*（match guard）允许为匹配添加特定额外条件，如不满足条件则对应模式匹配将失败：

```rust
fn main() {
    let x = Some(5);
    let y = 10;

    match x {
        Some(50) => println!("Got 50"),
        Some(n) if n == y => println!("Matched, n = {}", n),
        _ => println!("Default case, x = {:?}", x),
    }

    println!("at the end: x = {:?}, y = {}", x, y);
	// 输出结果：Default case, x = 5; at the end: x = 5, y = 10
}
```

注意：由于`if`优先级低于`|`，所以`a | b | c if cond`实际上等价于`(a | b | c) if cond`，而非`a | b | (c if cond)`。

*At绑定*（`@`）允许在创建存放值的变量时，对其进行匹配测试：

```rust

#![allow(unused)]
fn main() {
	enum Message {
	    Hello { id: i32 },
	}
	
	let msg = Message::Hello { id: 5 };
	
	match msg {
		// 为什么匹配这个分支，因为这个分支首先符合了条件
	    Message::Hello { id: id_variable @ 3..=7 } => {
	        println!("Found an id in range: {}", id_variable)
	    },
	    Message::Hello { id: 10..=12 } => {
	        println!("Found an id in another range")
	    },
	    Message::Hello { id } => {
	        println!("Found some other id: {}", id)
	    },
	}
	// 输出结果：Found an id in range: 5
}
```

### 不安全Rust

Rust默认不允许不安全的程序行为，但出于底层编程的考虑，允许通过`unsafe`关键字人为开启一些不安全功能：
- [[#解引用裸指针]]
- 调用不安全函数和方法
- 访问或修改可变静态变量
- 实现不安全trait
- 访问union的字段

注意：开启不安全功能不会关闭其他的Rust安全检查。

#### 解引用裸指针

不安全Rust涉及*裸指针*（raw pointer）类型，分为`*const T`和`*mut T`两个不可变或可变类型。

裸指针和引用有一些区别：
- 允许忽略借用规则，可以持有任意个不可变和可变指针
- 不保证指向的内存有效
- 允许为空
- 不能实现任何自动清理功能

通过引用可以创建裸指针：

```rust
#![allow(unused)]
fn main() {
	let mut num = 5;

	// 注意：安全代码也可以创建裸指针，只是不能解引用
	let r1 = &num as *const i32;
	let r2 = &mut num as *mut i32;
	// 不安全块内可以解引用
	unsafe {
	    println!("r1 is: {}", *r1);
	    println!("r2 is: {}", *r2);
	}
}
```

也可以通过逻辑地址创建裸指针，但大部分情况下这么做没啥理由：

```rust
#![allow(unused)]
fn main() {
	let address = 0x012345usize;
	let r = address as *const i32;
}
```

#### 调用不安全的函数或方法

如果被调用的函数也用`unsafe`进行了修饰，则调用方必须处于`unsafe`函数或`unsafe`块中，否则报错：

```rust
#![allow(unused)]
fn main() {
	unsafe fn dangerous() {}
	
	unsafe {
	    dangerous();
	}
}
```

#### 创建不安全代码的安全抽象

有一些功能无法通过安全Rust实现，而必须在实现中借助不安全Rust的功能，但对外仍暴露为安全接口：

```rust
use std::slice;

fn split_at_mut(slice: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = slice.len();
    let ptr = slice.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (slice::from_raw_parts_mut(ptr, mid),
         slice::from_raw_parts_mut(ptr.add(mid), len - mid))
    }
    // 如果直接这么写，会因为不允许2个可变引用而报错
    // (&mut slice[..mid], &mut slice[mid..])
}

#![allow(unused)]
fn main() {
	let mut v = vec![1, 2, 3, 4, 5, 6];
	
	let r = &mut v[..];
	
	let (a, b) = r.split_at_mut(3);
	
	assert_eq!(a, &mut [1, 2, 3]);
	assert_eq!(b, &mut [4, 5, 6]);
}
```

#### 调用非Rust代码

通过`extern`关键字可以创建和使用*外部函数接口*（foreign function interface，FFI）。由于调用外部代码不会经过Rust检查，所以会被认为总是不安全的。

`extern "C"`块内可声明C函数。对C函数的使用应遵循C语言的*应用二进制接口*（application binary interface，ABI）规范，即如何在汇编层面实施调用。

调用C标准库的`int abs(int)`函数示例：

```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        println!("Absolute value of -3 according to C: {}", abs(-3));
        // 输出：Absolute value of -3 according to C: 3
    }
}
```

从其他语言调用Rust代码，需要指定遵循的ABI，并通过标注`#[no_mangle]`提示编译器不要修改函数名：

```rust
#[no_mangle]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

#### 访问和修改可变静态变量

Rust的静态变量约等于C/C++的静态全局变量。根据可变性分为可变静态变量和不可变静态变量。通过`static`关键字声明：

```rust
static HELLO_WORLD: &str = "Hello, World!";
static mut COUNTER: u32 = 0;
```