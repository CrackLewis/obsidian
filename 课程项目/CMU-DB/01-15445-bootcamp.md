
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

与代表变量的*左值*相对，*右值*指向一个表达式。左值引用确保所引值必是一个变量