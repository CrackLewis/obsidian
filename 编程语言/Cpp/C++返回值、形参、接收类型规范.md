
## 返回值类型

考虑如下代码（一个具备移动/复制构造+析构函数+默认构造/析构的类）：

```cpp
class Dummy {
 public:
  Dummy() noexcept { std::cout << "Dummy::Dummy()" << std::endl; }

  Dummy(const Dummy&) noexcept {
    std::cout << "Dummy::Dummy(const Dummy&)" << std::endl;
  }

  Dummy(Dummy&&) noexcept { std::cout << "Dummy::Dummy(Dummy&&)" << std::endl; }

  ~Dummy() noexcept { std::cout << "Dummy::~Dummy()" << std::endl; }

  Dummy& operator=(const Dummy&) noexcept {
    std::cout << "Dummy::operator=(const Dummy&)" << std::endl;
    return *this;
  }

  Dummy& operator=(Dummy&&) noexcept {
    std::cout << "Dummy::operator=(Dummy&&)" << std::endl;
    return *this;
  }
};

template <typename A>
A foo() {
  return Dummy();
}

int main() {
  auto&& a = foo<???>();
  std::cout << "bar" << std::endl;
  return 0;
}
```

上述例子需要修改`???`的内容，观察`a`的类型和程序输出：
（输出简写：DC=默认构造，DD=默认析构）

返回局部变量引用类型的效果：

| `???`内容        | `a`类型          | 是否有警告        | 是否编译错误         | 输出内容        |
| -------------- | -------------- | ------------ | -------------- | ----------- |
| `Dummy`        | `Dummy&&`      | 否            | 否              | DC, bar, DD |
| `Dummy&`       | `Dummy&`       | 否            | 是，提示将右值转换为左值非法 | 无           |
| `const Dummy&` | `const Dummy&` | 是，提示引用临时变量不妥 | 否              | DC, DD, bar |
| `Dummy&&`      | `Dummy&&`      | 是，提示引用临时变量不妥 | 否              | DC, DD, bar |

向`Dummy`类增加一个字段，被移动后字段为空，被复制时字段同步复制。更改`foo`函数及其调用如下：

```cpp
template <typename A, typename B>
A foo(B&& var) {
  return std::forward(var);
}

int main() {
  auto&& d = foo<???>(Dummy{42});
  std::cout << "bar" << std::endl;
  return 0;
}
```

返回外部右值引用变量的效果：
（DC=默认构造，DD=默认析构，MC=移动构造，CC=复制构造）

| `???`内容        | `d`类型          | 编译错误和警告    | 输出                             |
| -------------- | -------------- | ---------- | ------------------------------ |
| `Dummy`        | `Dummy&&`      | 无          | DC(42), MC, DD(0), bar, DD(42) |
| `Dummy&&`      | `Dummy&&`      | 无          | DC(42), DD(42), bar            |
| `Dummy&`       | -              | 错误：右值不能转左值 | -                              |
| `const Dummy&` | `const Dummy&` | 无          | DC(42), DD(42), bar            |

将调用改为如下：

```cpp
int main() {
  auto c = Dummy{42}; // c是一个左值
  auto&& d = foo<???>(c);
  std::cout << "bar" << std::endl;
  return 0;
}
```

返回外部左值引用变量的效果：

| `???`内容        | `d`类型          | 编译错误和警告    | 输出                              |
| -------------- | -------------- | ---------- | ------------------------------- |
| `Dummy`        | `Dummy&&`      | 无          | DC(42), CC, bar, DD(42), DD(42) |
| `Dummy&&`      | -              | 错误：左值不能转右值 | -                               |
| `Dummy&`       | `Dummy&`       | 无          | DC(42), bar, DD(42)             |
| `const Dummy&` | `const Dummy&` | 无          | DC(42), bar, DD(42)             |

总结：
- 返回局部变量时：只能用原类型。返回左右值引用都可能触发编译错误
- 返回外部值时：
	- 确定是左值：返回左值
	- 确定是右值：返回右值
	- 不确定：返回`const T&`。但这样会导致接收类型不可改写内容
- 返回动态内存对象：用`T*`、`void*`或智能指针

## 形参类型

参考：Effective Modern C++

如果不确定其具体类型，最好的方案是`T&&`（`T`为模板元）。