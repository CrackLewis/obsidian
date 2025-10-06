
## TL;DR

型别推导篇：
- 

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

### 8、优先选用nullptr，而非0或NULL

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

### 9、优先选用别名声明，而非typedef

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
- 使用`typedef`声明的别名时，必须加`typename`前缀，因为上例中形如`MyAllocList2<T>::type`称为*依赖型别*。（为啥，因为`type`也有可能是类成员变量，这里是为了提醒编译器它确实是别名）

`std::remove_reference_t<T>`就是一个著名示例，在C++11之前得使用`typename std::remove_reference<T>::type`才能去除模板元型别`T`的引用饰词。

**总结**：
- `typedef`不支持直接模板化，但别名声明支持。
- 别名声明可以让人免写`::type`后缀和在模板内使用`typename`前缀。

### 10、优先选用限定作用域的枚举型别

绝大部分情形下，大括号扩起的内容要么对括号外不可见，要么必须用`::`、`.`或`->`进行访问。但一个最显著的例外是*C++98风格枚举*，它会将内部成员暴露在外，因此又称*不限范围的枚举型别*（unscoped enumeration）。

与C++98枚举不同，C++11引入的枚举类不会对外暴露成员，其成员必须通过`::`访问，因此又称*限定作用域的枚举型别*（scoped enumeration），后面简称*枚举类*：

```cpp
enum UnscopedEnum {
	E1, E2, E3
};

enum class ScopedEnum {
	E4, E5, E6
};

E1; // 成功，访问UnscopedEnum中的E1
auto E1 = 2; // 失败，E1已被定义

E5; // 失败，符号未定义
auto E5 = "string"; // 成功
E5; // 成功，访问的是变量E5
ScopedEnum::E5; // 成功，访问的是ScopedEnum中的E5
```

枚举类是强类型的（strongly typed）：它没有默认型别，只能手动指定一个底层型别。底层型别可以通过`std::underlying_type_t<T>`获取。相比之下C++98风格枚举如果没有指定底层型别，则会让编译器自行决定（通常是`int`）。

```cpp
enum class Color: unsigned int {
	RED = 1u,
	GREEN = 2u,
	BLUE = 3u,
};

using ColorUTy = std::underlying_type_t<Color>; // unsigned int
```

C++98风格枚举允许到各种基本类型的自动转换，但枚举类不会自动转换为其他型别，而只能进行强制型别转换：

```cpp
auto color = Color::BLUE; // Color类型
unsigned int color2 = Color::RED; // 错误
unsigned int color3 = static_cast<unsigned int>(Color::GREEN); // 正确
```

C++98风格枚举只有在指定底层型别的情况下才能前置声明，但枚举类总是可以前置声明。

```cpp
enum Status: unsigned char; // OK
enum Status2; // 错误

enum class Status3; // OK
```

**总结**：
- C++98风格枚举又称*不限范围的枚举型别*。
- 限定作用域的枚举型别仅在枚举型别内可见。它们只能通过强制型别转换以转换至其他型别。
- 限定作用域的枚举型别和不限范围的枚举型别都支持底层型别指定。限定作用域的枚举型别的默认底层型别是`int`，而不限范围的枚举型别没有默认底层型别。
- 限定作用域的枚举型别总是可以进行前置声明，而不限范围的枚举型别却只有在指定了默认底层型别的前提下才可以进行前置声明。

### 11、优先选用删除函数，而非private未定义函数

C++会在用户未显式定义时为类添加下列函数：
- 默认构造函数
- 复制构造函数、复制赋值运算符
- 空析构函数

在C++11之前，压制复制构造函数和复制赋值运算符的通用方法是将其设置为`private`，并且不给出函数定义：

```cpp
class A {
	// ...
private:
	A(const A&);
	A& operator=(const A&);
};
```

C++11开始，可以通过`=delete`将这两个函数设置为*删除函数*（deleted function），并设置为`public`。原因是，编译器会先检查类成员函数的可访问性，后检查其是否删除，声明为`public`可以让任何对该函数的访问都得到关于函数删除的报错信息，而非访问权限不足的报错信息：

```cpp
class A {
	// ...
public:
	A(const A&) = delete;
	A& operator=(const A&) = delete;
};
```

与`private`相比，删除函数不必是一个类成员函数。下面的这个实例演示了如何阻止类型不适合的函数调用通过编译：

```cpp
bool isLucky(int);

bool isLucky(double) = delete;
bool isLucky(bool) = delete;
bool isLucky(char) = delete;

isLucky(3); // OK
isLucky(false); // 报错
isLucky('a'); // 报错
isLucky(3.5); // 报错
```

删除函数还可以用于*特化函数模板*，阻止一些特定模板元下的函数被调用：

```cpp
template <typename T>
void processPtr(T* ptr) { /* ... */ }

template <>
void processPtr(void* ptr) = delete;
```

**总结**：
- `private`未定义函数对阻止使用某一函数的作用有限；相比之下，删除函数既可以删除非成员函数，也可以删除模板具现。

### 12、为意在改写的函数添加override声明

首先区分`override`（改写）和`overload`（重载）：

| 概念  | 含义                                 | 参与者           | 目的              | 发生时机 |
| --- | ---------------------------------- | ------------- | --------------- | ---- |
| 重载  | 在同一作用域内使用同一名称定义多个函数，但它们的形参不同       | 数个成员函数或数个全局函数 | 使函数更直观，提升可读和易用性 | 编译时  |
| 改写  | 子类重新定义父类虚函数，使调用子类对象虚函数时，只使用子类的函数定义 | 父类和子类         | 实现多态性           | 运行时  |

正确的改写有数个必须满足的要求：
- 基类的对应函数必须是虚函数。
- 基类和派生类中的*函数名字*必须完全相同（析构函数除外）。
- 基类和派生类中的函数*形参型别*、函数*常量性*必须完全相同。
- 基类和派生类中的函数*返回值*和*异常规格*必须兼容。
- （C++11开始）基类和派生类中的函数*引用饰词*必须完全相同。

函数常量性指的是函数是否确保不修改成员变量；引用饰词用于限定类对象为左值或右值时，调用哪一个函数定义：

```cpp
class Widget {
public:
	void doWork() &;
	void doWork() &&;

	static Widget makeWidget();
};

Widget w;
w.doWork(); // 调用前者
Widget::makeWidget().doWork(); // 调用后者
```

有时在基类和派生类中确定哪个函数继承或被继承很容易混淆，因此`override`关键字可以确保派生类的特定成员函数*一定会改写*基类的对应函数。

```cpp
class Base {
public:
	virtual void foo1(int) = 0;
	virtual bool foo2(double) = 0;
};

class Derived {
public:
	virtual void foo1(int x) override { /* ... */ } // 合法
	virtual bool foo2(float x) override { /* ... */ } // 不合法，形参不匹配
};
```

C++11的`final`关键字有类似的作用，它阻止派生类*重载或改写*这个函数。

**总结**：
- 为意在改写的函数添加`override`声明。
- 成员函数引用饰词能够区分对于左值和右值对象的处理。
### 13、优先选用const_iterator，而非iterator

`iterator`在C++17被弃用，本条款仅供参考。

本条款出现在这里的原因是C++98的历史遗留，当时获取容器的常迭代器很麻烦。但从C++11开始，诸多容器都通过`cbegin`和`cend`方法提供了相对可用的常迭代器支持。

常迭代器确保不会通过访问容器修改其内容，如果没有修改容器内容的需要，则应当尽可能使用常迭代器而不是非常迭代器。

尽管如此，C++11的支持仍非最完善，因为该版本的`cbegin`、`rbegin`、`crbegin`等方法通过非成员函数提供，即必须通过`cbegin(container)`返回。虽然C++14开始提供了成员函数版本，但最通用的代码仍应当积极考虑使用非成员函数形式：

```cpp
template <typename C, typename V>
void findAndInsert(C& container, const V& targetVal, const V& insertVal)
{
	using std::cbegin;
	using std::cend;

	// 使用非成员函数形式
	auto it = std::find(cbegin(container), cend(container), targetVal);
	container.insert(it, insertVal);
}
```

**总结**：
- 优先选用`const_iterator`，而非`iterator`。
- 在最通用的代码中，优先选用非成员函数版本的`begin`、`end`函数及其变种，而非成员函数版本。

### 14、只要函数不会抛出异常，就为其加上noexcept声明

C++11的`noexcept`关键字可用于修饰函数，确保该函数不会抛出任何异常。该关键字属于接口规格的一种，应加而不加属于接口缺陷。

对不会抛出异常的函数添加`noexcept`不仅可以改善代码的异常安全性，还可以允许编译器进行更激进的代码优化。

涉及异常的函数一般分三类：
- 异常中立型：不确定会抛出什么异常，其调用的函数抛出的异常会不经处理地跳出它。
- `noexcept`型：确定不会抛出异常。
- 异常抛出型：会显式使用`throw`语句抛出特定类型的异常。

**总结**：
- `noexcept`声明是函数接口的组成部分，意味着调用方可能依赖这个性质。
- 相对于不带`noexcept`的函数，带有`noexcept`声明的函数有更多机会得到优化。
- `noexcept`性质对于移动操作、`swap`、函数释放函数和析构函数最有价值。
- 大多数函数都是异常中立的，不具备`noexcept`性质。

### 15、尽可能使用constexpr

`constexpr`在不同的情况下有不同的语义：
- `constexpr`对象：加强版的`const`，定义编译期常量。
- `constexpr`函数：当且仅当实参都是编译期常量时，返回值是编译期常量。

`constexpr`函数可以用于在编译期自动计算一些常量，而不必由程序员打表完成或在运行时计算：

```cpp
// 打表法
constexpr int pow3[] = {1, 3, 9, 27, 81, 243, 729, 2187, 6561, ...};

// constexpr函数
constexpr int pow3(int x) {
	return x <= 0 ? 1 : pow3(x - 1) * 3;
}
constexpr int p5 = pow3(5);
```

在C++11中，`constexpr`函数只能包含一个`return`语句，而从C++14开始放宽了限制，允许循环、分支等结构：

```cpp
constexpr int pow3(int x) {
	int ret = 1;
	while (x > 0) {
		ret *= 3;
		x--;
	}
	return ret;
}
```

`constexpr`函数的形参和返回类型只允许*字面型别*（literal type）。C++14前除`void`外的内建型别都是字面型别。用户自定义的类、结构体如果在使用了`constexpr`构造函数，则同样是字面型别：

```cpp
class Point {
public:
	constexpr Point(double xVal = 0, double yVal = 0) noexcept 
	: x(xVal), y(yVal) {}
	
	constexpr double getX() const noexcept { return x; }
	constexpr double getY() const noexcept { return y; }

	constexpr void setX(double xVal) noexcept { x = xVal; }
	constexpr void setY(double yVal) noexcept { y = yVal; }
	
private:
	double x, y;
};
```

`constexpr`是对象和函数接口的组成部分。只要有可能就使用它，但要注意`constexpr`对相关函数和对象施加的种种限制。

**总结**：
- `constexpr`对象都具备`const`属性，并由编译期已知的值完成初始化。
- `constexpr`函数在调用时若传入的实参值是编译期已知的，则会产出编译期结果。
- `constexpr`函数和对象可以用在更广的语境中。

### 16、保证const成员函数的线程安全性

`const`函数饰词确保一个类成员函数不会访问非`mutable`属性，但函数仍可以修改`mutable`成员。如果多个线程同时执行该函数，则有可能出现*数据冒险*（data race）：

```cpp
class Polyn {
public:
	using RootsType = std::vector<double>;

	RootsType roots() const {
		if (!rootsAreValid) { // 如果缓存无效
			// ...
			rootsAreValid = true; 
			// 修改了rootsAreValid，可能出现数据冒险
		}
		return rootVals;
	}

private:
	mutable bool rootsAreValid{ false };
	mutable RootsType rootVals{};
}
```

由于`const`函数本身符合语法要求，所以只能强制将有关部分互斥处理，一种常见做法是*互斥锁*：

```cpp
RootsType roots_thread_safe() const {
	std::lock_guard<std::mutex> g(m);
	// lock_guard确保只有一个进程可以进入其生存域
	// ...
}
mutable std::mutex m;
```

也可以用*原子量*：

```cpp
mutable std::atomic<bool> rootsAreValid;
```

原子量的一个好处是其提供更轻量级的互斥，只在读写其值时确保不会发生冒险，因此开销较小。

**总结**：
- 除非确信`const`成员函数不会在并发语境中被调用，否则必须保证其线程安全性。
- `std::atomic`等原子量可以比互斥锁提供更好的性能，但仅适用于单个变量或内存区域的互斥操作。

### 17、理解特种成员函数的生成机制

C++11中，假设某个类是空类，则它会隐式定义这些成员：

```cpp
// 定义为空
class A {};

// 实际内容（忽略函数定义）
class A {
public:
	A(); // 默认构造函数
	~A(); // 析构函数
	A(const A&); // 复制构造函数
	A& operator=(const A&); // 复制赋值运算符
	// C++11新增
	A(A&&); // 移动构造函数
	A& operator=(A&&); // 移动赋值运算符
};
```

*特种成员函数*指会由C++自动生成的成员函数：
- 默认构造函数
- 析构函数
- 复制构造函数
- 复制赋值运算符
- （C++11）移动构造函数
- （C++11）移动赋值运算符

*特种成员函数*特点：
- 仅在用户未显式定义时生成
- 如果是自动生成的，则必是`public`、`inline`的非虚函数（基类析构函数为虚的除外）
- 两种复制操作独立；但两种移动操作不独立，定义一个会阻止另一个函数自动生成
- 一旦显式定义了复制操作，则移动函数不会生成；反之亦然，移动操作定义会阻止生成复制函数
- 一旦显式定义了析构函数，便不会生成移动函数，目前仍会生成复制函数（但标注为*废弃的行为*）

*生成规则*对应下表：
- 表头：CC=copy constructor（复制构造函数）、MA=move assignment（移动赋值运算符）、I=implicit（隐式生成）
- 内容：`-`为不定义/生成，`+`为定义/生成，`?`为两者皆有可能
- 左四列表示用户是否定义了这四种函数，右四列表示编译器是否生成了这四种函数

| `CC` | `CA` | `MC` | `MA` | `CC(I)` | `CA(I)` | `MC(I)` | `MA(I)` |
| ---- | ---- | ---- | ---- | ------- | ------- | ------- | ------- |
| -    | -    | -    | -    | +       | +       | +       | +       |
| +    | -    | -    | -    | -       | +       | -       | -       |
| -    | +    | -    | -    | +       | -       | -       | -       |
| +    | +    | -    | -    | -       | -       | -       | -       |
| ?    | ?    | +    | -    | -       | -       | -       | -       |
| ?    | ?    | -    | +    | -       | -       | -       | -       |
| ?    | ?    | +    | +    | -       | -       | -       | -       |

特种成员函数的*大三律*（rule of three）：重写了复制构造函数、复制赋值运算符和析构函数3个函数中的一个，就需要重写另两个。这是因为：重写这3个函数意味着朴素的成员复制不适用于当前类，很可能需要特殊的成员变量管理方式。

假如编译器生成的这些函数的默认行为符合期望，则可以用`= default`表示：

```cpp
A(const A&) = default;
A& operator=(const A&) = default;
```

*特别注意*：如果看到一个类只定义了构造函数和析构函数，这个看似合理的做法实际上阻止了复制和移动函数的自动生成。而对于不可移动的类，在移动时实际会执行复制操作，这样可能会极大降低程序性能。

**总结**：
- 特种成员函数指C++会自动生成的成员函数：默认构造函数、析构函数、复制操作、移动操作。
- 移动操作仅当类中未包含用户显式声明的复制操作、移动操作和析构函数时才生成。
- 复制构造函数仅当类中不包含用户显式声明的复制构造函数时才生成，如果该类声明了移动操作则复制构造函数将被删除。复制赋值运算符仅当类中不包含用户显式声明的复制赋值运算符才生成，如果该类声明了移动操作则复制赋值运算符将被删除。在已经存在显式声明的析构函数的条件下，生成复制操作已经成为了被废弃的行为。
- 成员函数模板在任何情况下都不会抑制特种成员函数的生成。

## 四、智能指针

C++标准库中有4种常见的智能指针：
- `std::auto_ptr`：时代的眼泪
- `std::unique_ptr`：专属所有权指针
- `std::shared_ptr`：共享所有权指针
- `std::weak_ptr`

### 18、std::unique_ptr

`std::unique_ptr<T>`实现了专属所有权语义。该指针不能复制，*只能移动*，只有当前持有它的作用域才能使用它。

`std::unique_ptr<T>`默认使用`delete`运算符作为*默认析构器*，也可以通过模板元实现*自定义析构器*。如果`T`为基类，则它必须使用虚析构函数：

```cpp
class Investment {
public:
	virtual ~Investment();
};

auto delInvmt = [](Investment* pInv) {
	makeLogEntry(pInv);
	delete pInv;
};

std::unique_ptr<Investment, decltype(delInvmt)> pInv(nullptr, delInvmt);
```

 `std::unique_ptr`有3个重要的非特种成员函数：
 - `release()`：释放其管理的指针
 - `swap(std::unique_ptr<T>& oth)`：与另一个指针交换管理对象
 - `get()`：获取管理对象的引用
 - `reset(T* obj)`：重设管理对象，如果有旧对象则删除之

除了指向单个对象的`std::unique_ptr<T>`外，还有`std::unique_ptr<T[]>`用于管理对象数组，前者没有`operator[]`运算符，使用`delete`运算符为默认析构器；后者没有`operator->`和`operator*`运算符，使用`delete[]`运算符为默认析构器。这种设计较好地解决了对象指针的二义性问题。

`std::unique_ptr`还可以隐式转换为`std::shared_ptr`：

```cpp
std::unique_ptr<Investment> uInv = makeInvestment(args);
std::shared_ptr<Investment> sInv = uInv;
```

需要注意的是，`std::unique_ptr<T>`仍然仅好于裸指针，能用标准库的其他容器就不要用智能指针。

**总结**：
- `std::unique_ptr`是只移动的专属所有权智能指针。
- `std::unique_ptr`默认使用`delete`和`delete[]`运算符为默认析构器，用户也可自行指定。
- `std::unique_ptr`可以方便地转换为`std::shared_ptr`。

### 19、std::shared_ptr

`std::shared_ptr`可以理解为实现了*简单垃圾回收机制*的智能指针。指向同一内存对象的所有`std::shared_ptr`共享该对象的所有权，当最后一个指向该对象的指针被析构时，对象被析构。

这种自动析构对象的机制是通过引用计数实现的：
- 创建时：所指对象引用计数+1。
- 析构时：所指对象引用计数-1。
- 赋值时：原对象引用计数-1，新对象引用计数+1。

当然这种机制也会引入一些代价：
- 指针尺寸是裸指针的两倍。额外空间指向一个*控制块*，包含引用计数、析构器指针等内容。
- 引用计数的内存必须动态分配。这个不难理解，内存对象不可能知晓引用计数，所以必须由指针全盘托管。
- 引用计数的递增和递减必须是原子操作。

![[Pasted image 20240426163921.png]]

`std::shared_ptr<T>`也支持*自定义析构器*，但不同的是它不是模板元参数的一部分，意味着指向同一类型、使用不同析构器的`std::shared_ptr`属于同一类型：

```cpp
auto del1 = [](Widget* w) { ... };
auto del2 = [](Widget* w) { ... };

std::shared_ptr<Widget> p1(new Widget, del1), p2(new Widget, del2);
std::vector<std::shared_ptr<Widget>> vp{p1, p2};
```

控制块的构造遵循如下规则：
- `std::make_shared`总是创建一个控制块。
- 从裸指针和专属所有权指针构造`std::shared_ptr`时总是创建一个控制块。

上述规则说明：同一个裸指针应当仅用于创建一次`std::shared_ptr`。否则该指针指向的对象可能会由两或多个控制块同时管理，从而形成未定义行为：

```cpp
Widget* w = new Widget;
std::shared_ptr<Widget> p1(w); // OK
std::shared_ptr<Widget> p2(w); // 错误！第二个控制块，可能造成w被析构两次
std::shared_ptr<Widget> p3 = p1; // OK
```

如果有些情况下，类对象需要获取指向自身的`std::shared_ptr`，那么它可以继承`std::enable_shared_from_this`类，使用该类提供的`shared_from_this()`方法：

```cpp
class Widget: public std::enable_shared_from_this<Widget> {
public:
	// ...
	void process();
	// ...
};

void Widget::process() {
	processedWidgets.emplace_back(shared_from_this());
}
```

与`std::unique_ptr`相比，`std::shared_ptr`有这些特点：
- 只能管理单个对象，不能管理对象数组。
- 不能够转化为`std::unique_ptr`，但`std::unique_ptr`可以隐式转化过来。
- 与其管理的对象在全生命期内绑定，即使是引用计数为1，也不能让出资源管理权。

**总结**：
- `std::shared_ptr`提供方便的手段，实现了任意资源在共享所有权语义下进行生命周期管理的垃圾回收。
- `std::shared_ptr`尺寸是裸指针的两倍，会带来控制块的开销，要求原子化引用计数。
- 默认的资源析构行为通过`delete`运算符进行，但也支持自定义析构器。自定义析构器类型不是模板元参数，不影响型别。
- 避免使用裸指针型别变量创建`std::shared_ptr`指针。

### 20、std::weak_ptr

`std::weak_ptr`是`std::shared_ptr`的一种补充。它的一个用途是检测`std::shared_ptr`所指的某个对象是否空悬：

```cpp
auto spa = std::make_shared<A>();
std::weak_ptr<A> wpa(spa);
spa = nullptr;
wpw.expired(); // 返回true
```

由于没有提领操作，`std::weak_ptr`依赖通过`lock`方法转换为`std::shared_ptr`以确保在指针非空时正确访问对象，在指针为空时返回空指针：

```cpp
std::shared_ptr<A> spa1 = wpa.lock();

auto spa2 = wpa.lock();
```

另一种更粗暴的方法是直接转换，但可能抛出异常：

```cpp
try {
	std::shared_ptr<A> spa3(wpa);
} catch (std::bad_weak_ptr& e) {
	std::cerr << e.what() << std::endl;
}
```

`std::weak_ptr`的特性使其适合用于做缓存：
- *不占用引用计数*，其析构不会导致对象被删除。
- 读写为单个原子操作，较方便。

下面是一个示例，`loadWidget`是一个开销较大的函数，而`fastLoadWidget`是缓存函数：

```cpp
std::unique_ptr<Widget> loadWidget(WidgetId id);

std::shared_ptr<Widget> fastLoadWidget(WidgetId id) {
	static std::unordered_map<WidgetId, std::weak_ptr<Widget>> cache;

	auto objPtr = cache[id].lock(); // std::shared_ptr
	if (!objPtr) {
		objPtr = loadWidget(id);
		cache[id] = objPtr;
	}
	return objPtr;
}
```

另一个示例是观察者模式：该模式的各个主题会有一个指向观察者的指针，以便在主题发生变化时通知观察者。如果观察者指针使用`std::weak_ptr`类型而非其他类型，则可以在访问前判断指针是否空悬。

另外，`std::weak_ptr`有助于解决`std::shared_ptr`引入的*指针环路问题*：

假设`A,B`两个类对象保存着指向彼此的`std::shared_ptr`。那么如果外界没有指向这两个对象的裸指针，它们就永远不会被销毁，因为它们会保持彼此的引用计数至少为1，这实质上是另一种内存泄漏。

如果其中一个指针改为`std::shared_ptr`，那么持有弱指针的一者不会阻止另一者被析构，持有`shared_ptr`的一者则会使另一者至少存活至自己析构时。这样便解决了这个问题。

**总结**：
- 使用`std::weak_ptr`来代替可能空悬的`std::shared_ptr`。它不占用引用计数。
- `std::weak_ptr`可用于缓存、观察者列表，以及避免指针环路问题。

### 21、std::make_unique、std::make_shared

WIP

**总结**：
- `std::make_unique`、`std::make_shared`的好处：消除重复代码，改进异常安全性，生成更好的目标代码。
- `std::make_***`不适用于以下情形：需要自定义删除器、期望通过大括号初始化。
- 对于`std::shared_ptr`，不建议使用`std::make_***`的额外场景：
	- 自定义内存管理的类。
	- 内存紧张的系统。
	- 非常大的对象。
	- 存在比指涉到相同对象`std::shared_ptr`生存期更久的`std::weak_ptr`。

### 22、Pimpl习惯用法注意事项

Pimpl=pointer to implementation，指涉到实现的指针

*Pimpl做法*：把类的数据成员用一个类或结构体的指针替代，尔后把原来在主类的数据成员放入该类（或结构体），通过指针访问这些成员：

```cpp
// Widget.h
#ifndef WIDGET_H_
#define WIDGET_H_

class Widget {
public:
	Widget();
	~Widget(); // 析构函数必须声明，否则报错

	Widget(Widget&& rhs);
	Widget& operator=(Widget&& rhs);
private:
	struct Impl; // 此处声明的Impl类型尚不完整
	std::unique_ptr<Impl> pImpl;
};

#endif

// Widget.cpp
#include "Widget.h"
#include "Gadget.h"
#include <vector>
#include <string>

struct Widget::Impl {
	std::string name;
	std::vector<double> data;
	Gadget g1, g2, g3;
};

Widget::Widget(): pImpl(std::make_unique<Impl>()) {}
Widget::~Widget() = default;
Widget::Widget(Widget&& rhs) = default;
Widget& Widget::operator=(Widget&& rhs) = default;
```

这种做法的好处：通过将数据成员放入结构体，使得用户不必依赖`<string>`、`<vector>`和`Gadget.h`等头文件，也不必因为`Widget.h`修改而需要重新编译整个项目。

上面的`pImpl`也可以替换为`std::shared_ptr`类型，可以少写几个特种成员函数，但性能上不如前者。

**总结**：
- Pimpl惯用法降低了类的客户和类实现者之间的依赖性，减少了构建次数。
- 对于采用`std::unique_ptr`实现的`pImpl`，须在类内声明特种成员函数并提供实现，即使默认行为是正确的。
- 上述建议仅适用于`std::unique_ptr`，不适用于`std::shared_ptr`。

## 五、右值引用、移动语义和完美转发

概念：
- *右值引用*：对表达式右值的引用。
- *移动语义*：在不产生额外数据副本的情形下实现对象间的数据转移。
- *完美转发*：接受任意的实参，转发到其他函数，并确保其他函数收到完全相同的实参。

### 23、std::move、std::forward

`std::move`无条件地将实参转化为右值引用：

```cpp
template <typename T>
decltype(auto) move(T&& param) 
{
	using RetT = remove_reference_t<T>&&;
	return static_cast<RetT>(param);
}
```

这也导致贸然使用`std::move`有时会适得其反，比如下面的例子，由于`std::move`会将`v`转为`const std::string&&`类型，而`const std::string&&`只能隐式转为`const std::string&`而非`std::string&&`，所以实际上在赋值时仍然调用的是`std::string`的复制构造函数，而非移动构造函数：

```cpp
class A {
public:
	// 调用std::string(const std::string&)
	explicit A(const std::string v): val(std::move(v)) {}
private:
	std::string val;
};
```

`std::forward`是有条件的强制型别转换。与`std::move`不同的是，它仅当实参使用右值完成初始化时，才会执行向右值型别的强制型别转换：

```cpp
void bar(const std::string&) { std::cout << "lval" << std::endl; }
void bar(std::string&&) { std::cout << "rval" << std::endl; }
template <typename T>
void foo(T&& t) {
	bar(std::forward<T>(t));
}

// 不太正确的例子，实际项目不要这么写
std::string str;
foo(str); // T=std::string&, 输出为lval
foo(str + ""); // T=std::string，输出为rval
```

*权衡*：
- 适合用`std::move`：需要移动操作的情形。
- 适合用`std::forward`：需要无差错转发参数类型，或判断参数左右值的情形。

**总结**：
- `std::move`本身不执行移动操作，而只是无条件向右值型别强制转换。
- 仅当传入的实参绑定右值时，`std::forward`才针对该实参实施向右值型别的强制类型转换。
- 运行期`std::move`和`std::forward`都不会做任何操作。

### 24、万能引用、右值引用

`T&&`的两种含义：
- 万能引用：`auto&&`、或`T`*完全不能确定*。
- 右值引用：`T`被施加了任何限制，如`T=std::vector<U>`，或`T=const U`。

运用万能引用可以写出相当高逼格的函数，比如下面这个计时函数：

```cpp
auto timeFunc = [](auto&& func, auto&&... params)
{
	MyTimer t;
	t.start();
	std::forward<decltype(func)>(func)(
		std::forward<decltype(params)>(params)...
	);
	t.stop();
	return t.getTimeMillis();
};
```

**总结**：
- 当且仅当函数模板形参或对象通过`T&&`或`auto&&`声明型别时，它是万能引用。
- 如果型别声明并不精确地具备`T&&`形式，或没有发生类别推导，则它是右值引用。
- 若采用右值引用初始化万有引用，则得到右值引用，否则得到左值引用。

### 25、针对右值引用实施std::move，针对万能引用实施std::forward

WIP

**总结**：
-  针对右值引用的最后一次使用实施`std::move`，针对万能引用的最后一次使用实施`std::forward`。
- 作为按值返回的函数的右值引用和万能引用，依上一条所述采取相同行为。
- 若局部对象可能适用于返回值优化，则请勿针对其实施`std::move`或`std::forward`。

### 26、避免依万能引用型别进行重载

下面这个函数用于在尽可能少复制对象的情况下给`std::vector`追加对象：

```cpp
std::vector<std::string> names;

template <typename T>
void logAndAdd(T&& name)
{
	log(std::chrono::system_clock::now(), "logAndAdd");
	names.emplace(std::forward<T>(name));
}
```

假设需要添加一个对`T=int`的特化：

```cpp
std::string nameFromIdx(int idx) { ... }

void logAndAdd(int idx) {
	log(std::chrono::system_clock::now(), "logAndAdd(int)");
	names.emplace(nameFromIdx(idx));
}
```

这时传入`short`或`long long`类型则会报错，因为它们匹配到万能引用，而该模板不支持`emplace(short)`之类的操作。这是因为万能引用劫持了`short`和`LL`，使得`int`特化无法被调用。

而在类内用万能引用重载构造函数更糟，它会在诸多情形下劫持复制和移动构造函数：

```cpp
class A {
 public:
  template <typename T>
  explicit A(T&& t) : s(std::forward<T>(t)) {
    std::cout << "A(T&&)" << std::endl;
  }
  explicit A(int idx) : s("name" + std::to_string(idx)) {
    std::cout << "A(int)" << std::endl;
  }
  A(const A& oth) : s(oth.s) { std::cout << "A(const A&)" << std::endl; }
  A(A&& oth) : s(std::move(oth.s)) { std::cout << "A(A&&)" << std::endl; }

 private:
  std::string s;
};

std::string s = "A";
const std::string sc = "A";
A a1(s); // A(T&&)
A a2(sc); // A(T&&)
A a3("nameA"); // A(T&&)
A a4(std::move(a1)); // A(T&&)
A a5(2); // A(int)
```

对所有期望在这种写法下正常工作的型别均提供特化几乎是唯一的解决方案。因为所幸，万能引用在与其他模板有相同的签名匹配度时，优先级会略低。

**总结**：
- 万能引用作为重载候选型别，几乎总会让该重载版本在始料未及的情况下被调用。
- 完美转发构造函数的情形尤其严重，因为对于非常量的左值型别而言，它们一般都会形成相对于复制构造函数的更佳匹配，并且它们还会劫持派生类中对基类的复制和对移动构造函数的调用。

### 27、万能引用型别重载的替代方案

常见替代方案：
- 放弃重载：如果硬要使用不加限制的万能引用形参模板，或许使用不同函数名是一个好主意。
- 传递`const T&`形参：放弃部分效率，保持接口的简洁性。
- 传值：形参直接传值，在初始化成员时用`std::move`。
- 标签分派：用模板元判断类型是否符合某一要求（如`std::is_integral_t<T>`），将其作为参数一并提供给模板函数。

**总结**：
- 如果不使用万能引用和重载的组合，则替代方案包括：使用彼此不同的函数名，传递`const T&`形参、传值、标签分派。
- 经由`std::enable_if`等对模板实施限制，以避免发生预期之外的劫持。
- 万能引用形参在性能方面占优，但在易用性方面较差。

### 28、引用折叠

程序员不能自行定义引用的引用，但编译器可以在特殊语境中产生引用的引用。当引用的引用产生时，遵照以下规则折叠：
- 任意一者为左值引用：折叠为左值引用（`&`）
- 两者均为右值引用：折叠为右值引用（`&&`）

引用折叠会在四种语境出现：
- 模板实例化。
- `auto`变量型别推导。
- 生成和使用`typedef`和别名声明。
- 涉及`decltype`的型别推导过程。

前两种无需多言，在别名声明或`typedef`中可能会引入多重引用，这时引用折叠机制会介入：

```cpp
template <typename T>
class A {
public:
	typedef T&& rval_ref_type;
	// 若T=U&，则T&&=U&；若T=U，则T&&=U&&
};
```

**总结**：
- 引用折叠四种语境：`auto`型别生成、模板实例化、创建和运用`typedef`和别名声明、`decltype`。
- 当编译器生成引用的引用时，结果会通过引用折叠变为单个引用，当引用中包含左值引用时，结果为左值引用，否则结果为右值引用。
- 万能引用就是在型别推导过程中会区分左值和右值，以及会发生引用折叠的语境中的右值引用。

### 29、

### 30、

## 六、lambda表达式

### 31、

### 32、

### 33、

### 34、

## 七、并发API

### 35、

### 36、

### 37、

### 38、

### 39、

### 40、

## 八、微调

### 41、

### 42、