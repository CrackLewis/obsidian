
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

`decltype(expr)`可以获取`expr`的声明类型（declared type），但使用不当也会出现一些意外结果。

[[#^9ed8a7|跳过这个示例，直接看规则]]

**示例**：指定容器`c`和索引`idx`，需要编写一个先检查权限，后按索引随机访问容器的函数。下面的代码提出了三种实现方案：

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
	return c[idx];
}
```

方案一：OK。

方案二：不太对，因为无论`c[idx]`为`T`还是`T&`，`auto`都会推导为`T`。这会导致针对`c[idx]`的赋值操作失败：原先它是左值，auto将它转换成了右值。

方案三：也OK。因为`decltype(auto)`为`auto`打了个补丁，它不处理函数返回值（`Container::operator[](Index idx)`）的型别，所以也能正确推导。

题外话：上面的版本不支持临时容器，所以支持临时容器要这么写：

```cpp
template <typename Container, typename Index>
#if __cplusplus >= 201402L
// C++14版本允许decltype(auto)作为返回类型
decltype(auto) authAndAccess(Container&& c, Index idx) {
#elif __cplusplus >= 201103L
// C++11只能用回型别尾序语法
auto authAndAccess(Container&& c, Index idx) -> decltype(std::forward<Container>(c)) {
#else
#error "Your C++ version is ramshackle old."
#endif
	authenticateUser(c, idx);
	return std::forward<Container>(c)[idx];
}
```

`decltype`规则： ^9ed8a7
- 对于变量、类成员访问：推出其声明类型。
- 对于函数调用：推出其返回值类型。
- 对于其他表达式：若为左值则推出引用类型，否则推出值类型。
- 如果出现冗余符号（多个左值引用符号、`const`、`volatile`限定），会省到只剩一个

下面是一些示例（难于理解的打了`*`）：

| `x`类型                 | `expr`                         | `decltype(expr)`     | 费解  |
| --------------------- | ------------------------------ | -------------------- | --- |
| `int`                 | `x`                            | `int`                |     |
| `int`                 | `++x`                          | `int&`               |     |
| `int`                 | `x++`                          | `int`                |     |
| `int`                 | `(x)`                          | `int&`               | `*` |
| `int`                 | `x += 2`                       | `int&`               |     |
| `int&`                | `x`                            | `int&`               |     |
| `const int&`          | `x`                            | `const int&`         |     |
| `const char* const`   | `(x)`                          | `const char* const&` | `*` |
| `int& (int&, int&)`   | `x(y, z)`                      | `int&`               |     |
| `std::pair<int, int>` | `x.second`                     | `int`                |     |
| `std::pair<int, int>` | `(x.second)`                   | `int&`               |     |
| /                     | `std::pair<int, int>::first`   | `int`                |     |
| /                     | `(std::pair<int, int>::first)` | `int&`               | `*` |
| `int [M]`             | `x`                            | `int [M]`            |     |
| `int [M]`             | `(x)`                          | `int (&)[M]`         | `*` |
| `int [M]`             | `x[0]`                         | `int&`               | `*` |
| `int (int, int)`      | `(x)`                          | `int (&)(int, int)`  | `*` |
| `int&& ()`            | `x()`                          | `int&&`              | `*` |
| `int*`                | `*x`                           | `int&`               |     |
| /                     | `"lval"`                       | `const char(&)[5]`   | `*` |

**总结**：
- 绝大部分情况下，`decltype(expr)`会返回`expr`的声明类型。
	- `expr`为左值表达式时，会返回其左值引用类型。
- C++14支持的`decltype(auto)`可以实现完美的返回值型别推导。

### 4、查看型别推导结果

- IDE的语法功能
- `typeid(expr).name()`
- 编写模板工具类

模板工具类可以故意构造一个不完整类型，从而暴露出模板元的类型：

```cpp
template <typename Ty> class TyDis;

TyDis<int(int,double,char)> _; // ERROR: TyDis<int(int,double,char)> has incomplete type
```

`std::type_info::name`是用来干这个的，但并不准确，更可靠的是`Boost.TypeIndex`库提供的类似功能。

## 二、auto关键字

### 5、优先auto而非显式型别声明

`auto`型别声明有一些好处：
- 可以避免无意的无初始值声明。
- 如果声明变量的型别较冗长，用`auto`可以省得手敲一遍型别。
- 可以推导出一些只有编译器才能掌握的型别（如`lambda`表达式）。
- 可以避免填错类型，导致预期之外的对象拷贝或类型转换（本来要填`const A& x=...`，但实际填成了`const B&`，导致调用了一次`B(const A&)`）。

### 6、带显式型别的初始化物习惯用法

尽管`auto`型别推导大部分情况下很有用，但个别情况下可能不会按预期效果工作。

书内用两页的篇幅（P47-48）介绍了一个例子：

```cpp
std::vector<bool> features(const Widget& w);
void processWidget(const Widget& w, bool isHighPriority);

Widget w;
// ...
bool highPriority1 = features(w)[5]; // [1]
processWidget(w, highPriority1);

auto highPriority2 = features(w)[5]; // [2]
processWidget(w, highPriority2);
```

用例`[1]`是正常工作的。但用例`[2]`有所不同，它做了这么一些事情：
- 将`highPriority2`推导为`std::vector<bool>::reference`类型，而不是`bool`或`bool&`类型。
- 在某些编译器中，`std::vector<bool>::reference`实现为代理对象。因此`features(w)[5]`所在的字节会生成一个临时拷贝，而返回的`highPriority2`指向该拷贝的第5个比特。
- 在将`highPriority2`传递给`processWidget`时，临时字节已经析构，因此`highPriority2`悬空，产生未定义行为。

但代理类并不是来捣乱的，有时这么设计确实有效率等其他方面的考量，但这也往往意味着代理类不能和`auto`和平共处。这个时候只能用显式初始化折衷：

```cpp
auto highPriority3 = static_cast<bool>(features(w)[5]);
```

**总结**：
- “隐形”的代理型别可以导致`auto`根据初始化表达式推导出“错误”的型别。
- 带显式型别的初始化物习惯用法强制`auto`推导出你想要的型别。

## 三、转向现代C++

### 7、创建对象时区分()和{}

C++11开始，初始化有三种方法：

```cpp
int y = 1; // 注意这种方法和赋值有本质区别
int z(1);
int x{1};
int x = {1}; // 和上一种方法在大部分情况下是等价的
```

为了解决上述三种初始化语法带来的困惑，C++11引入了统一初始化，也称*大括号初始化*（braced initialization），也就是上面的第三种初始化方法。

大括号初始化有相对更广泛的用法：

| 初始化情形  | 等号初始化                      | 圆括号初始化                     | 大括号初始化 |
| ------ | -------------------------- | -------------------------- | ------ |
| 变量     | Y                          | Y                          | Y      |
| 类成员    | Y                          | <font color="red">N</font> | Y      |
| 不可复制对象 | <font color="red">N</font> | Y                          | Y      |

大括号初始化的*特性*：
- 禁止隐式的窄化型别转换（narrowing conversion）：`double`隐式转`int`不允许
- 在括号内为空时，不会被误推导为函数声明：`Widget w1();`会被误推导为函数，而空大括号不会
- 这算是一个*缺陷*：如果型别有任何形参为`(std::initializer_list<T>)`的构造函数，大括号初始化会*强烈地*优先使用这种构造函数，即使这意味着转换所有成员型别为`T`。
	- 即使是型别会被窄化转换，编译器仍然优先匹配该构造函数，从而报错。
	- 只有在大括号成员完全不能转换为`T`型别时，编译器才会退而选择其他构造函数。

例子：

```cpp
int x{2.0 + 3}; // ERROR!

class A {
public:
	A(std::initializer_list<long double> il) { ... }
	A(int i, bool b) { ... }
	A(int i, double d) { ... }
	A(int i, const char* str) { ... }

	operator float() const { ... }
};

A a(2, true);          // 调用第二个构造函数
A b{2, true};          // 调用第一个构造函数（劫持普通构造函数）

A c(2, 5.0);           // 调用第三个构造函数
A d{2, 0.5};           // 调用第一个构造函数（劫持普通构造函数）

A e{c};                // 调用第一个构造函数（劫持复制构造函数）
A f{std::move(d)};     // 调用第一个构造函数（劫持移动构造函数）
```

**注意**：
- 如果大括号列表为空，则即使存在`(std::initializer_list<T>)`形参的构造函数，也不会使用，而会使用默认构造函数。
	- 嵌套空列表，诸如`A a({})`或`A a{{}}`之类的声明仍然会调用前者。

**总结**：
- 大括号初始化可以应用的语境最为广泛，可以阻止隐式窄化型别转换，也可以避免误解析为函数声明。
- 只要有任何可能，大括号初始化都会优先匹配`std::initializer_list<T>`参数的构造函数，哪怕是存在更相似的构造函数匹配。

### 8、优先使用nullptr，而非0或NULL

`0`和`NULL`在C++中的本质仍是`int`类型，仅在没有匹配`int`类型时才会尝试匹配`void*`类型。

`nullptr`则是另一回事：它是`std::nullptr_t`类型，会优先匹配`void*`而非`int`。

示例：假设要写一个互斥调用器，通过操作互斥锁实现互斥调用并返回结果。

```cpp
int f1(std::shared_ptr<Widget> spw);
double f2(std::unique_ptr<Widget> upw);
bool f3(Widget* pw);

std::mutex f1m, f2m, f3m;
using MuxGuard = std::lock_guard<std::mutex>;

template <typename FuncTy, typename MuxTy, typename PtrTy>
decltype(auto) lockAndCall(FuncTy func, MuxTy& mtx, PtrTy ptr)
{
	MuxGuard g(mtx);
	return func(ptr);
}

// ...

auto result1 = lockAndCall(f1, f1m, 0); // 报错
auto result2 = lockAndCall(f2, f2m, NULL); // 报错
auto result3 = lockAndCall(f3, f3m, nullptr); // OK
```

上面的示例中，前两个都报错，因为`int`不能强转智能指针，但`nullptr`可以实现这种转换。

**总结**：
- 能用`nullptr`表示指针，就用`nullptr`。
- 要尽量规避在整型和指针型别之间重载。

### 9、优先使用别名声明，而非typedef

别名声明指C++11引入的给型别起别名的特殊语法：

```cpp
using vvi = std::vector<std::vector<int> >;
```

相比`typedef`，它更易读，而且不需要定义类或结构体就可以进行模板化，称为*别名模板*（alias template）：

```cpp
// 别名模板
template <typename T>
using MyAllocList = std::list<T, MyAlloc<T>>;

// typedef则必须定义一个类或结构体模板，将typedef声明放入其中
// 同时，使用MyAllocList2<T>::type前面必须加typename
template <typename T>
struct MyAllocList2 {
	typedef std::list<T, MyAlloc<T>> type;
};

template <typename T>
class Widget {
private:
	MyAllocList<T> list;
	typename MyAllocList2<T>::type list2;
};
```

与别名模板相比，基于类模板的`typedef`别名有很大的不便：
- 必须定义一个类模板包含`typedef`声明
- 使用`typedef`s

## 四、智能指针

## 五、右值引用、移动语义和完美转发

## 六、lambda表达式

## 七、并发API

## 八、微调