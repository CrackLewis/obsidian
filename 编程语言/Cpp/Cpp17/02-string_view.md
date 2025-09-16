
```cpp
#include <string_view>
```

为啥需要string\_view：
- 字符串拷贝太evil了
- 需要一套统一接口，处理C字符串和C++字符串

## 示例：substr

```cpp
char str1[15] = "abcdefghijkl";
std::string_view view1(str1, 6);
std::cout << view1 << std::endl; // 输出：abcdef

std::string str2 = "0123456789";
std::string_view view2(str2);
std::cout << view2.substr(0, 6) << std::endl; // 输出：012345
```