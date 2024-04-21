
## 一、型别推导

### 1、模板型别推导

引例：

```cpp
template <typename T>
void f(const T& param);

int x = 0;
f(x);
```

在上例中，`T`被推导为`int`，与`x`的类型恰恰一致。但这并不代表`T`的类型一定等于`x`的类型，这涉及到模板的型别推导规则。

假设函数模板的模板元为`T`，参数为`ParamType`类型，传入的实参为`expr`，则可以分为三种情形：

```cpp
template <typename T>
void f(ParamType param);

f(expr);
```

**情形一**：`ParamType`是个指针或引用，但不是万能引用

型别推导会这样做：
- 若`expr`具有引用类别，则先忽略引用部分
- 随后，对`expr`的型别和`ParamType`的型别执行*模式匹配*，决定`T`的类型。

因此：

| `expr`的类型    | `ParamType` | `T`         |
| ------------ | ----------- | ----------- |
| `int`        | `T&`        | `int`       |
| `const int`  | `T&`        | `const int` |
| `const int&` | `T&`        | `const int` |
| `int*`       | `T*`        | `int`       |
| `const int*` | `T*`        | `const int` |

**情形二**：`ParamType`是个万能引用

万能引用指`T&&`类型，它能推导为左值引用、右值引用、常引用和非常引用。如果`ParamType`是这种类型，情况会比较复杂：

| `expr`的类型    | `expr`的值类型 | `T`          |
| ------------ | ---------- | ------------ |
| `int`        | 左值         | `int&`       |
| `const int`  | 左值         | `const int&` |
| `const int&` | 左值         | `const int&` |
| `int`        | 右值         | `int`        |

万能引用也是唯一一种会将`T`推导为引用类型的情形。

**情形三**：`ParamType`既非引用也非指针

最常见的情况是按值传递，即`ParamType = T`，此时`param`必会被构造为一个新对象。此时如下推导：
- 如果`expr`具有引用型别，忽略之。
- 忽略`expr`的`const`和`volatile`限定符。

也就是说，前文的`int`、`const int`、`const int&`类型在传入时均会被推导为`int`。

特别地，如果传入了`const void* const`，那么`T`会被推导为`const void*`，因为只有第二个`const`限定了指针变量。

**边缘情形一**：数组实参

在C++中数组和指针是两种类型，数组可以退化为指针。

由于C语言的遗留问题，C++中函数参数为数组则会自动退化为指针，但参数为数组引用则不会退化。这样会引入一些奇怪的问题：

| `expr`类型        | `ParamType` | `T`              |
| --------------- | ----------- | ---------------- |
| `char []`       | `T`         | `char*`          |
| `const char []` | `T`         | `const char*`    |
| `char*`         | `T`         | `char*`          |
| `const char*`   | `T`         | `const char*`    |
| `char [M]`      | `T&`        | `char [M]`       |
| `const char[M]` | `T&`        | `const char [M]` |
| `char*`         | `T&`        | `char*`          |
| `const char*`   | `T&`        | `const char*`    |

`ParamType`为`T`时，传入的数组实参全数退化，但为`T&`时没有发生退化现象。

利用这种非退化机制可以写出一个工具函数模板，获取一个数组长度：

```cpp
template <typename T, std::size_t N> 
constexpr std::size_t arraySize(T (&)[N]) noexcept {
	return N;
}

int keyVals[] = {1, 3, 4, 5, 7, 9};
std::array<int, arraySize(int)> mappedVals;
```

**边缘情形二**：函数实参

和数组类似，函数形参也会在推导`T`时退化为函数指针，而在推导`T&`时不会退化：

| `expr`类型      | `ParamType` | `T`              |
| ------------- | ----------- | ---------------- |
| `P (Args...)` | `T`         | `P (*)(Args...)` |
| `P (Args...)` | `T&`        | `P (Args...)`    |

**总结**：
- 在模板型别推导过程中，具有引用型别的实参（`U&`）会一律当作非引用型别（`U`）处理。
- 对万能引用形参（`T&&`）进行推导时，左值实参会进行特殊处理。
- 对按值传递形参（`T`）进行推导时，会自动忽略实参的`const`和`volatile`限定。
- 在模板型别推导过程中，函数或数组型别的实参会退化为对应的指针型别，除非是被用来初始化引用。

### 2、auto型别推导

`auto`可以推导：
- 变量声明的类型
- 函数声明的返回类型

`auto`变量型别推导是根据变量声明*初值的类型*和`auto`的*型别饰词*推导出变量型别的过程。

与模板型别推导十分类似，`auto`型别推导也有三种情形：
- 是指针或（非万能）引用（`auto*`或`auto&`）。
- 是万能引用（`auto&&`）。
- 既非指针也非引用（`auto`）。

常规情形与模板型别推导几乎一致：

| 初值类型         | `auto`饰词      | `auto`推导结果   |
| ------------ | ------------- | ------------ |
| `int&`       | `auto&`       | `int`        |
| `int&`       | `const auto&` | `const int`  |
| `int&`       | `auto&&`      | `int&`       |
| `const int&` | `auto&&`      | `const int&` |
| `int&&`      | `auto&&`      | `int`        |
| `int&`       | `auto`        | `int`        |
| `int&&`      | `auto`        | `int`        |
| `int&`       | `const auto`  | `int`        |

函数和数组型别推导也几乎一致：

| 初值类型             | `auto`饰词 | `auto`推导结果       |
| ---------------- | -------- | ---------------- |
| `const char [M]` | `auto`   | `const char*`    |
| `const char [M]` | `auto&`  | `const char [M]` |
| `P (Args...)`    | `auto`   | `P (*)(Args...)` |
| `P (Args...)`    | `auto&`  | `P (Args...)`    |

只有*一处不同*：如果初值是`{ ... }`形式，那么`auto`会被推导为`std::initializer_list<T>`，这是一条特殊规则。与`auto`不同的是，模板型别推导不能推导这种形式，会产生编译错误。

`auto`型别推导的通用要求是：列表非空，且表内各元素型别相同。

在遇到大括号列表时，`auto`型别推导分等号和非等号形式：
- 等号形式：`auto var={...}`。无特殊要求。
- 占位符形式：`auto var{...}`。要求表内有且仅有一个元素。

```cpp
auto x{1, 2, 3.0}; // ERROR! not the same type
auto x{}; // ERROR! cannot derive type
auto x = {1ull, 2ull}; // ok: std::initializer_list<unsigned long long>
auto x{1, 2, 3}; // ERROR! only 1 element is required
```

值得提一嘴的是：从C++14开始，函数返回值和函数形参也允许使用`auto`型别推导。但由于其本质还是*模板型别推导*，所以不适用前面的大括号列表。

```cpp
auto ft = [&](auto&& nv) { std::cout << nv << std::endl; };

ft(1); // 1
ft("233"); // 233
ft(2 == 3); // 0
ft(nullptr); // nullptr
ft({1}); // ERROR! no matching function ft
```

**总结**：
- `auto`型别推导与模板型别推导最显著的区别是`auto`对初始化列表的处理。
- C++14起支持在函数返回值和函数形参处使用`auto`，但其本质是模板型别推导。

### 3、decltype

`decltype(expr)`可以获取`expr`的类型。

示例：指定容器`c`和索引`idx`，需要编写一个先检查权限，后按索引随机访问容器的函数。下面的代码提出了三种实现方案：

```cpp
template <typename Container, typename Index>
#if (SCHEME == 1) // C++11的返回值型别尾序语法
auto authAndAccess(Container& c, Index idx) -> decltype(c[idx]) {
#elif (SCHEME == 2) // C++14的auto返回值型别
auto authAndAccess(Container& c, Index idx) {
#else // C++14的decltype(auto)
decltype(auto) authAndAccess(Container& c, Index idx) {
#endif
	authenticateUser(c, idx);
	return c[i];
}
```

方案一：OK。

方案二：不太对，因为无论`c[idx]`为`T`还是`T&`，`auto`都会推导为`T`。这会导致针对`c[idx]`的赋值操作失败：原先它是左值，auto将它转换成了右值。

方案三：也OK，

### 4、查看型别推导结果



## 二、auto关键字

## 三、转向现代C++

## 四、智能指针

## 五、右值引用、移动语义和完美转发

## 六、lambda表达式

## 七、并发API

## 八、微调