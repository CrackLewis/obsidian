
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

