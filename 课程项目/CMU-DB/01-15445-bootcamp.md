
课程要求回顾/了解一些Modern C++的语法。

## auto型别推断

`auto`可以根据初始化表达式类型，自动推断声明变量的类型。

```cpp
int x = 3;
auto y = 5; // int
auto& xref = x; // int&

YetAnotherSuperDuperComplicatedTypename foo;
auto& bar = foo;
```

`auto&&`则是万能引用，可以推断绝大部分的变量类型。

## 条件变量

```cpp
#include <condition_variable>
```

条件变量是由标准库提供的一种同步原语，它允许进程在获取互斥锁之前，等待一个特定的条件。

条件变量涉及两种角色：
- 等待者：通过`wait(lk, cond)`方法陷入等待，当有唤醒者通知它条件`cond`可能为真时唤醒，重新判断`cond`，如果结果为真则返回，否则继续等待。
- 唤醒者：通过`notify_one`或`notify_all`方法唤醒等待者。

**例**：

定义全局变量`count`，初始值为0。等待者会在`count`增至2时被唤醒，有关定义：

```cpp
int count = 0;
// count的互斥锁
std::mutex m;
// 全局条件变量
std::condition_variable cv;
```

唤醒者例程：

```cpp
void add_count_and_notify() {
  std::scoped_lock slk(m);
  count += 1;
  if (count == 2) {
    cv.notify_one();
  }
}
```

等待者例程：

```cpp
void waiter_thread() {
  // 条件变量要求必须传入一个unique_lock。调用wait时它会被释放，在判断条件为真、wait返回前重新取得
  std::unique_lock lk(m);
  // 等待直至count等于2
  cv.wait(lk, []{return count == 2;});
  std::cout << "Printing count: " << count << std::endl;
}
```

## 迭代器

略

## 移动构造函数&移动赋值运算符

*移动*是一种不额外创造资源、在不同变量间转移数据的方式，与*复制*相对。

如果类型不支持复制，那么在该类型的不同变量间转移数据就必须依赖移动，因此也必须定义对应的*移动构造函数*、*移动赋值运算符*。

CMU bootcamp给出的是这个示例：

```cpp
class Person {
public:
  Person() : age_(0), nicknames_({}), valid_(true) {}

  // 带参构造：注意nicknames是右值
  Person(uint32_t age, std::vector<std::string> &&nicknames)
      : age_(age), nicknames_(std::move(nicknames)), valid_(true) {}

  // 移动构造函数
  Person(Person &&person)
      : age_(person.age_), nicknames_(std::move(person.nicknames_)),
        valid_(true) {
    std::cout << "Calling the move constructor for class Person.\n";
    // The moved object's validity tag is set to false.
    person.valid_ = false;
  }

  // 移动赋值运算符
  Person &operator=(Person &&other) {
    age_ = other.age_;
    nicknames_ = std::move(other.nicknames_);
    valid_ = true;
    // 旧对象非法化
    other.valid_ = false;
    return *this;
  }

  // 显式禁用复制操作
  Person(const Person &) = delete;
  Person &operator=(const Person &) = delete;

  uint32_t GetAge() { return age_; }

  std::string &GetNicknameAtI(size_t i) { return nicknames_[i]; }

  void PrintValid() {
    if (valid_) {
      std::cout << "Object is valid." << std::endl;
    } else {
      std::cout << "Object is invalid." << std::endl;
    }
  }

private:
  uint32_t age_;
  std::vector<std::string> nicknames_;
  // 合法标记
  bool valid_;
};
```

## 移动语义

移动语义概括下来是这几件事情：

与代表变量的*左值*相对，*右值*指向一个表达式。左值引用确保所引值必是左值，右值引用同理。

右值引用可绑定到一个不可赋值的表达式上：

```cpp
int x = 2;

int&& xref1 = 2 + 3;
int&& xref2 = x++;
int&& xref3 = std::move(x);
int&& xrefx = ++x; // 不合法：前缀自增表达式是左值
```

右值引用不能被重新绑定，但非`const`的引用可以被赋值：

```cpp
int&& ref1 = 2 + 3;
ref1 = 6; // 合法

const int&& ref2 = 5 + 7;
ref2 = 13; // 不合法
```

将一个函数返回值绑定到右值引用，而非赋给变量，可以延长返回值的生命期，从而在语义上省去一次复制操作。但GCC系列编译器有NRV机制，会自动这样做。

```cpp
std::vector<int> costly_function() {
	std::vector<int> ans;
	// VERY COSTLY!
	return ans;
}

int main() {
	auto&& res = costly_function();
	// ...
	return 0;
}
```

右值引用可以连环绑定。它们最终都引用同一个表达式。

```cpp
int&& a = 2;
int&& b = a;
int&& c = b;
int&& d = c;
a = 3;
std::cout << a << ':' << b << ':' << c << ':' << d << std::endl;
// 3:3:3:3
```

但如果右值绑定到左值，将触发移动语义：
- 基本类型：直接复制
- 非基本类型：尝试调用*移动构造函数*或*移动赋值运算符*，调用失败则报错

如果需要移动一个非右值，可以使用`std::move`方法。但要注意，它不会实际执行移动，而只是将非右值转为右值，而右值保持不变。

```cpp
// 前文重载了vector输出运算符

std::vector<int> a = {1, 2, 3, 4};
auto&& b = std::move(a);
// 此时b绑定到a的右值，修改b仍然对修改a生效
std::cout << a << ',' << b << std::endl;
// [1,2,3,4],[1,2,3,4]

auto c = std::move(a);
// 此时a的内容移动到c，a,b变为空容器
std::cout << a << ',' << c << std::endl;
// [],[1,2,3,4]
```

## 互斥锁

略

## 命名空间

全局环境中可以声明命名空间，以规避命名冲突。

```cpp
namespace clewis {
	class A {
		// ...
	};
	class B {
		// ...
	};
}

class A {
	// ...
};

clewis::A a;
A b;
```

命名空间允许*嵌套*，访问则通过命名空间运算符`::`逐级访问：

```cpp
namespace D {
int secret = 111;
}

namespace A {
namespace B {
namespace C {
namespace D {
int secret = 222;
}
int reveal() { return D::secret * 1000 + ::D::secret; }
}  // namespace C
}  // namespace B
}  // namespace A

int result = A::B::C::reveal();
// 结果：222111
```

`using`声明可用于便捷访问特定的命名空间或命名空间成员：

```cpp
using A::B::C::reveal;
using namespace A::B::C::D;
// 给命名空间起别名
using E = namespace A::B::C::D;
```

匿名命名空间对同环境（同命名空间、同文件）下的其他成员可见，对外不可见。

```cpp
namespace {
	int i = 1;
}

i++; // OK
```

## 引用

略

## 读写锁

`std::shared_mutex`是C++标准库实现的读写锁。它拥有两种层次的互斥：
- 读互斥：
	- 触发：调用`lock_shared`，或被读锁`std::shared_lock`锁定
	- 性质：允许其它读锁重复锁定，但不允许写锁锁定
- 写互斥：
	- 触发：调用`lock`，或被写锁`std::unique_lock`锁定
	- 性质：不允许其他任何锁重复锁定

## 作用域锁

类似于`std::lock_guard`，也是在生命期内锁定一个互斥体

## std::set

`std::set::find(x)`返回：
- 如果找到元素：返回元素对应的迭代器
- 否则：返回`std::set::end()`

`std::set::erase(begin, end)`：可以移除`[begin, end)`区间内所有元素

## 智能指针

智能指针分三种：
- 独占类指针：`std::unique_ptr<T>`
- 共享类计数指针：`std::shared_ptr<T>`
- 共享类弱指针：`std::weak_ptr<T>`

### std::unique_ptr

`std::unique_ptr<T>`是一种独占类智能指针，表示指针独占一部分内存资源。指针对象析构时，其所指对象也析构。

可由`std::make_unique<T>(args...)`创建：

```cpp
int n = 20;
auto x1 = std::make_unique<std::vector<int>>(n, 0);
```

特别地，当`T`为数组类型（如`int[]`）时，其只接受一个参数，作为数组的长度：

```cpp
auto x1 = std::make_unique<int[]>(5);
```

`std::unique_ptr<T>`不可复制，只能被移动：

```cpp
auto p1 = std::make_unique<int>(233);
auto p2 = p1; // 报错：不允许复制
auto&& p3 = p1; // OK：p3为p1的左值引用
auto&& p4 = std::move(p1); // OK：p1的内容移动到p4，p1悬空
```

获取裸指针可通过`get`方法：

```cpp
auto p1 = std::make_unique<int>(233);
int* rp1 = p1.get();
```

此外还有交换两个指针地址的`swap`方法、解除对裸指针占有的`release`方法，以及重设裸指针的`reset`方法等。

### std::shared_ptr

`std::shared_ptr<T>`是一种共享类智能指针，表示指针与其他的`shared_ptr`共同指向一段内存。每个被指向的内存伴有一个引用计数，表示当前有多少个`std::shared_ptr`指向它。当计数归0时，内存被析构和释放。

可由`std::make_shared<T>(args...)`创建：

```cpp
int n = 30;
auto x1 = std::make_shared<std::vector<int>>(n, 0);
```

与`std::unique_ptr`不同，`std::shared_ptr`既可以复制也可以移动：

```cpp
auto p1 = std::make_shared<int>(20);
auto p2 = p1; // 合法：p2与p1引用相同内容
auto p3 = std::move(p1); // 合法：p1的引用移交给p3，p1悬空
```

引用计数可通过`use_count`方法获取。