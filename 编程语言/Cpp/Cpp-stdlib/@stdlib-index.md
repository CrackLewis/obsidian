此文档由Codex协助整理

## 多用途头文件

| 头文件 | 说明 |
| --- | --- |
| `<cstdlib>` | 通用工具：程序控制、动态内存分配、随机数、排序与搜索 |
| `<execution>` (C++17) | 算法并行版本和执行控制组件的预定义执行策略 (C++26 起) |

## 语言支持库

| 头文件 | 说明 |
| --- | --- |
| `<cfloat>` | 浮点类型限制 |
| `<climits>` | 整数类型限制 |
| `<compare>` (C++20) | 三路比较运算符支持 |
| `<contracts>` (C++26) | 契约支持库 |
| `<coroutine>` (C++20) | 协程支持库 |
| `<csetjmp>` | 保存（和跳转）到执行上下文的宏（和函数） |
| `<csignal>` | 信号管理函数和宏常量 |
| `<cstdarg>` | 可变长度参数列表处理 |
| `<cstddef>` | 标准宏和 typedef |
| `<cstdint>` (C++11) | 固定宽度整数类型和其他类型限制 |
| `<exception>` | 异常处理工具 |
| `<initializer_list>` (C++11) | std::initializer_list 类模板 |
| `<limits>` | 查询算术类型属性 |
| `<new>` | 低级内存管理工具 |
| `<source_location>` (C++20) | 提供获取源代码位置的方法 |
| `<stdfloat>` (C++23) | 固定宽度浮点类型 |
| `<typeindex>` (C++11) | std::type_index |
| `<typeinfo>` | 运行时类型信息工具 |
| `<version>` (C++20) | 提供宏以验证库的实现状态 |

## 概念库

| 头文件 | 说明 |
| --- | --- |
| `<concepts>` (C++20) | 基本库概念 |

## 诊断库

| 头文件 | 说明 |
| --- | --- |
| `<cassert>` | 将参数与零比较的条件编译宏 |
| `<cerrno>` | 包含上次错误码的宏 |
| `<debugging>` (C++26) | 调试库 |
| `<stacktrace>` (C++23) | 栈回溯库 |
| `<stdexcept>` | 标准异常类型 |
| `<system_error>` (C++11) | 定义 std::error_code，一个依赖于平台的错误码 |

## 内存管理库

| 头文件 | 说明 |
| --- | --- |
| `<memory>` | 高级内存管理工具 |
| `<memory_resource>` (C++17) | 多态分配器和内存资源 |
| `<scoped_allocator>` (C++11) | 嵌套分配器类 |

## 元编程库

| 头文件 | 说明 |
| --- | --- |
| `<ratio>` (C++11) | 编译时有理数运算 |
| `<type_traits>` (C++11) | 编译时类型信息工具 |

## 通用工具库

| 头文件 | 说明 |
| --- | --- |
| `<any>` (C++17) | std::any 类 |
| `<bit>` (C++20) | 位操作函数 |
| `<bitset>` | std::bitset 类模板 |
| `<expected>` (C++23) | std::expected 类模板 |
| `<functional>` | 函数对象、函数调用、绑定操作和引用包装器 |
| `<optional>` (C++17) | std::optional 类模板 |
| `<tuple>` (C++11) | std::tuple 类模板 |
| `<utility>` | 各种实用组件 |
| `<variant>` (C++17) | std::variant 类模板 |

## 容器库

| 头文件 | 说明 |
| --- | --- |
| `<array>` (C++11) | std::array 容器 |
| `<deque>` | std::deque 容器 |
| `<flat_map>` (C++23) | std::flat_map 和 std::flat_multimap 容器适配器 |
| `<flat_set>` (C++23) | std::flat_set 和 std::flat_multiset 容器适配器 |
| `<forward_list>` (C++11) | std::forward_list 容器 |
| `<hive>` (C++26) | std::hive 容器 |
| `<inplace_vector>` (C++26) | std::inplace_vector 容器 |
| `<list>` | std::list 容器 |
| `<map>` | std::map 和 std::multimap 关联容器 |
| `<mdspan>` (C++23) | std::mdspan 视图 |
| `<queue>` | std::queue 和 std::priority_queue 容器适配器 |
| `<set>` | std::set 和 std::multiset 关联容器 |
| `<span>` (C++20) | std::span 视图 |
| `<stack>` | std::stack 容器适配器 |
| `<unordered_map>` (C++11) | std::unordered_map 和 std::unordered_multimap 无序关联容器 |
| `<unordered_set>` (C++11) | std::unordered_set 和 std::unordered_multiset 无序关联容器 |
| `<vector>` | std::vector 容器 |

## 迭代器库

| 头文件 | 说明 |
| --- | --- |
| `<iterator>` | 范围迭代器 |

## 范围库

| 头文件 | 说明 |
| --- | --- |
| `<generator>` (C++23) | std::generator 类模板 |
| `<ranges>` (C++20) | 范围访问、原语、需求、工具和适配器 |

## 算法库

| 头文件 | 说明 |
| --- | --- |
| `<algorithm>` | 在范围上操作的算法 |
| `<numeric>` | 对范围内的值进行数值操作 |

## 字符串库

| 头文件 | 说明 |
| --- | --- |
| `<cstring>` | 各种窄字符字符串处理函数 |
| `<string>` | std::basic_string 类模板 |
| `<string_view>` (C++17) | std::basic_string_view 类模板 |

## 文本处理库

| 头文件 | 说明 |
| --- | --- |
| `<cctype>` | 确定窄字符类别的函数 |
| `<charconv>` (C++17) | std::to_chars 和 std::from_chars |
| `<clocale>` | C 本地化工具 |
| `<codecvt>` (C++11) (C++17 中已弃用) (C++26 中已移除) | Unicode 转换工具 |
| `<cuchar>` (C++11) | C 风格的 Unicode 字符转换函数 |
| `<cwchar>` | 各种宽和多字节字符串处理函数 |
| `<cwctype>` | 确定宽字符类别的函数 |
| `<format>` (C++20) | 格式化库，包括 std::format（[[stdlib-format]]） |
| `<locale>` | 本地化工具 |
| `<regex>` (C++11) | 支持正则表达式处理的类、算法和迭代器 |
| `<text_encoding>` (C++26) | 文本编码识别 |

## 数值库

| 头文件 | 说明 |
| --- | --- |
| `<cfenv>` (C++11) | 浮点环境访问函数 |
| `<cmath>` | 常用数学函数 |
| `<complex>` | 复数类型 |
| `<linalg>` (C++26) | 基本线性代数算法 (BLAS) |
| `<numbers>` (C++20) | 数学常数 |
| `<random>` (C++11) | 随机数生成器和分布 |
| `<simd>` (C++26) | 数据并行类型以及对这些类型的操作 |
| `<valarray>` | 表示和操作值数组的类 |

## 时间库

| 头文件 | 说明 |
| --- | --- |
| `<chrono>` (C++11) | C++ 时间工具 |
| `<ctime>` | C 风格时间/日期工具 |

## 输入/输出库

| 头文件 | 说明 |
| --- | --- |
| `<cinttypes>` (C++11) | 格式化宏，intmax_t 和 uintmax_t 数学和转换 |
| `<cstdio>` | C 风格输入/输出函数（[[stdlib-cstdio]]） |
| `<filesystem>` (C++17) | std::filesystem::path 类和支持函数 |
| `<fstream>` | std::basic_fstream、std::basic_ifstream、std::basic_ofstream 类模板和 typedef |
| `<iomanip>` | 帮助函数以控制输入和输出的格式 |
| `<ios>` | std::ios_base 类、std::basic_ios 类模板和 typedef |
| `<iosfwd>` | 输入/输出库中所有类的前向声明 |
| `<iostream>` | 几个标准流对象 |
| `<istream>` | std::basic_istream 类模板和 typedef |
| `<ostream>` | std::basic_ostream、std::basic_iostream 类模板和 typedef |
| `<print>` (C++23) | 格式化输出库，包括 std::print |
| `<spanstream>` (C++23) | std::basic_spanstream、std::basic_ispanstream、std::basic_ospanstream 类模板和 typedef |
| `<sstream>` | std::basic_stringstream、std::basic_istringstream、std::basic_ostringstream 类模板和 typedef |
| `<streambuf>` | std::basic_streambuf 类模板 |
| `<strstream>` (在 C++98 中已废弃) (在 C++26 中已移除) | std::strstream、std::istrstream、std::ostrstream |
| `<syncstream>` (C++20) | std::basic_osyncstream、std::basic_syncbuf 和 typedef |

## 并发支持库

| 头文件 | 说明 |
| --- | --- |
| `<atomic>` (C++11) | 原子操作库 |
| `<barrier>` (C++20) | 屏障 |
| `<condition_variable>` (C++11) | 线程等待条件 |
| `<future>` (C++11) | 异步计算原语 |
| `<hazard_pointer>` (C++26) | 危险指针 |
| `<latch>` (C++20) | 闩 |
| `<mutex>` (C++11) | 互斥原语 |
| `<rcu>` (C++26) | 读-复制-更新机制 |
| `<semaphore>` (C++20) | 信号量 |
| `<shared_mutex>` (C++14) | 共享互斥原语 |
| `<stop_token>` (C++20) | std::jthread 的停止令牌 |
| `<thread>` (C++11) | std::thread 类和支持函数 |

## C 兼容头文件

对 C 标准库头文件 `<xxx.h>`，C++ 同时提供同名头文件和 `<cxxx>` 头文件（所有有意义的 `<cxxx>` 均已列于上文）。`<xxx.h>` 的预期用途仅限于与 C 互操作；纯 C++ 代码不建议使用。

除 `<complex.h>` 外，每个 `<xxx.h>` 与对应 `<cxxx>` 声明相同的名称：`<cxxx>` 把名称放入 `std` 命名空间（也可能放入全局命名空间），`<xxx.h>` 把名称放入全局命名空间（也可能放入 `std`）。`<xxx.h>` 在 C++98 中已弃用、C++23 起取消弃用，将来不会被移除。

### 与 `<cxxx>` 对应的 C 头文件

| 头文件                    | 说明                                                        |
| ---------------------- | --------------------------------------------------------- |
| `<assert.h>`           | 行为与 `<cassert>` 相同                                        |
| `<ctype.h>`            | 行为如同将 `<cctype>` 中的每个名称都放置在全局命名空间中                        |
| `<errno.h>`            | 行为与 `<cerrno>` 相同                                         |
| `<fenv.h>` (C++11)     | 行为如同将 `<cfenv>` 中的每个名称都放置在全局命名空间中                         |
| `<float.h>`            | 行为与 `<cfloat>` 相同                                         |
| `<inttypes.h>` (C++11) | 行为如同将 `<cinttypes>` 中的每个名称都放置在全局命名空间中                     |
| `<limits.h>`           | 行为与 `<climits>` 相同                                        |
| `<locale.h>`           | 行为如同将 `<clocale>` 中的每个名称都放置在全局命名空间中                       |
| `<math.h>`             | 行为如同将 `<cmath>` 中的每个名称都放置在全局命名空间中，除了数学特殊函数的名称             |
| `<setjmp.h>`           | 行为如同将 `<csetjmp>` 中的每个名称都放置在全局命名空间中                       |
| `<signal.h>`           | 行为如同将 `<csignal>` 中的每个名称都放置在全局命名空间中                       |
| `<stdarg.h>`           | 行为如同将 `<cstdarg>` 中的每个名称都放置在全局命名空间中                       |
| `<stddef.h>`           | 行为如同将 `<cstddef>` 中的每个名称都放置在全局命名空间中，除了 std::byte 及相关函数的名称 |
| `<stdint.h>` (C++11)   | 行为如同将 `<cstdint>` 中的每个名称都放置在全局命名空间中                       |
| `<stdio.h>`            | 行为如同将 `<cstdio>` 中的每个名称都放置在全局命名空间中                        |
| `<stdlib.h>`           | 行为如同将 `<cstdlib>` 中的每个名称都放置在全局命名空间中                       |
| `<string.h>`           | 行为如同将 `<cstring>` 中的每个名称都放置在全局命名空间中                       |
| `<time.h>`             | 行为如同将 `<ctime>` 中的每个名称都放置在全局命名空间中                         |
| `<uchar.h>` (C++11)    | 行为如同将 `<cuchar>` 中的每个名称都放置在全局命名空间中                        |
| `<wchar.h>`            | 行为如同将 `<cwchar>` 中的每个名称都放置在全局命名空间中                        |
| `<wctype.h>`           | 行为如同将 `<cwctype>` 中的每个名称都放置在全局命名空间中                       |

### 特殊 C 兼容头文件

| 头文件 | 说明 |
| --- | --- |
| `<stdatomic.h>` (C++23) | 定义 _Atomic 并提供 C 标准库中的相应组件 |

### 空 C 头文件

| 头文件 | 说明 |
| --- | --- |
| `<ccomplex>` (C++11) (C++17 中已弃用) (C++20 中已移除) | 仅仅包含头文件 `<complex>` |
| `<complex.h>` (C++11) | 仅仅包含头文件 `<complex>` |
| `<ctgmath>` (C++11) (C++17 中已弃用) (C++20 中已移除) | 仅仅包含头文件 `<complex>` 和 `<cmath>`：与 C 头文件 `<tgmath.h>` 内容等效的重载已由这些头文件提供 |
| `<tgmath.h>` (C++11) | 仅仅包含头文件 `<complex>` 和 `<cmath>` |

### 无意义的 C 头文件

| 头文件 | 说明 |
| --- | --- |
| `<ciso646>` (C++20 中移除) | 空头文件。C 中 iso646.h 中出现的宏在 C++ 中是关键字 |
| `<cstdalign>` (C++11) (C++17 中已弃用) (C++20 中已移除) | 定义一个兼容宏常量 |
| `<cstdbool>` (C++11) (C++17 中已弃用) (C++20 中已移除) | 定义一个兼容宏常量 |
| `<iso646.h>` | 无效果 |
| `<stdalign.h>` (C++11) | 定义一个兼容宏常量 |
| `<stdbool.h>` (C++11) | 定义一个兼容宏常量 |

### 不支持的 C 头文件

`<stdatomic.h>`（C++23 前）、`<stdnoreturn.h>`、`<threads.h>` 不包含在 C++ 中，也没有 `<cxxx>` 对应物。

---

参考：[C++ 标准库头文件 — cppreference.cn](https://cppreference.cn/w/cpp/header)
