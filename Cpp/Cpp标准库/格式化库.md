
@since C++20

参考：
- [C++格式化库](https://zh.cppreference.com/w/cpp/utility/format)

## 旧的格式化方案

C方式：

```cpp
void format_by_printf() {
	const char* culprits = {"Hitler", "Goring", "Himmler", "Goebbel"};
	const int ballcnt = {1, 2, 3, 0};
	for(int idx=0;idx<3;++idx)
		printf("%s has got %d ball(s).\n", culprits[i], ballcnt[i]);
}
```

C++的输出流方式：

```cpp
void format_by_stream() {
	const char* culprits = {"Hitler", "Goring", "Himmler", "Goebbel"};
	const int ballcnt = {1, 2, 3, 0};
	for(int idx=0;idx<3;++idx)
		std::cout << std::string(culprits[i]) << " has got " << ballcnt[i]
				  << " ball(s). " << std::endl;
}
```

## C++20的格式化方案

格式串：描述格式的字符串。必须是**编译期常量**。

```cpp
std::format_string fstr("{} has got {} ball(s).");
```

格式化：

```cpp
void format() {
	const char* culprits = {"Hitler", "Goring", "Himmler", "Goebbel"};
	const int ballcnt = {1, 2, 3, 0};
	for(int idx=0;idx<3;++idx)
		std::cout << std::format(fstr, culprits[i], ballcnt[i]) 
		          << std::endl;
}
```

### 替换域

格式串中用大括号包围、中间可根据规则标注替换格式，允许用参数替换的区域。

**规则**：[...](https://zh.cppreference.com/w/cpp/utility/format/formatter#.E6.A0.87.E5.87.86.E6.A0.BC.E5.BC.8F.E8.AF.B4.E6.98.8E)

WIP