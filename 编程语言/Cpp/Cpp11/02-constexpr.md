
关键字；表示一个编译期便可确定的量、过程或行为

*与const区别*：const修饰的变量通过特殊手段仍可修改，但constexpr是编译期确定的，其值在代码段/rdata内，不可修改；constexpr兼含const的语义

*constexpr变量*：
- 基本类型：用字面量初始化
- 指针和引用类型：只能引用其他已定义的constexpr变量
- 组合类型：必须定义`constexpr`构造函数，构造函数必须满足constexpr函数规范，其实参必须均为constexpr变量

*constexpr函数*：
- C++11的constexpr函数只能有一个返回语句。循环结构是禁止的
- C++14可以定义内部变量，使用分支/循环/跳转结构等

*if-constexpr*：如果条件是常量表达式，那么if-constexpr可以在编译期确定使用哪个分支

## CppRef上的例子

```cpp
#include <iostream>
#include <stdexcept>

// C++11 constexpr functions use recursion rather than iteration
constexpr int factorial(int n) { return n <= 1 ? 1 : (n * factorial(n - 1)); }

// C++14 constexpr functions may use local variables and loops
#if __cplusplus >= 201402L
constexpr int factorial_cxx14(int n) {
  int res = 1;
  while (n > 1) res *= n--;
  return res;
}
#endif  // C++14

// A literal class
class conststr {
  const char* p;
  std::size_t sz;

 public:
  template <std::size_t N>
  constexpr conststr(const char (&a)[N]) : p(a), sz(N - 1) {}

  // constexpr functions signal errors by throwing exceptions
  // in C++11, they must do so from the conditional operator ?:
  constexpr char operator[](std::size_t n) const {
    return n < sz ? p[n] : throw std::out_of_range("");
  }

  constexpr std::size_t size() const { return sz; }
};

// C++11 constexpr functions had to put everything in a single return statement
// (C++14 does not have that requirement)
constexpr std::size_t countlower(conststr s, std::size_t n = 0,
                                 std::size_t c = 0) {
  return n == s.size()                ? c
         : 'a' <= s[n] && s[n] <= 'z' ? countlower(s, n + 1, c + 1)
                                      : countlower(s, n + 1, c);
}

// An output function that requires a compile-time constant, for testing
template <int n>
struct constN {
  constN() { std::cout << n << '\n'; }
};

int main() {
  std::cout << "4! = ";
  constN<factorial(4)> out1;  // computed at compile time

  volatile int k = 8;  // disallow optimization using volatile
  std::cout << k << "! = " << factorial(k) << '\n';  // computed at run time

  std::cout << "The number of lowercase letters in \"Hello, world!\" is ";
  constN<countlower("Hello, world!")> out2;  // implicitly converted to conststr

  constexpr int a[12] = {0, 1, 2, 3, 4, 5, 6, 7, 8};
  constexpr int length_a = sizeof a / sizeof(int);  // std::size(a) in C++17,
                                                    // std::ssize(a) in C++20
  std::cout << "Array of length " << length_a << " has elements: ";
  for (int i = 0; i < length_a; ++i) std::cout << a[i] << ' ';
  std::cout << '\n';
}
```