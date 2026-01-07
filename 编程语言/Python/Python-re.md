
```python
import re
```

refs:
- [1](https://zhuanlan.zhihu.com/p/721484078)
- [runoob](https://www.runoob.com/python/python-reg-expressions.html)

## Python正则表达式语法

流程控制：
- `^`：匹配字符串开头
- `$`：匹配字符串末尾
- `.`：匹配任意字符（除换行符外，`re.DOTALL`启用时也会匹配换行符）
- `\A`：匹配字符串开始
- `\z`：匹配字符串结束（无视换行）
- `\Z`：匹配字符串结束（如果存在换行，只匹配到换行前）
- `\G`：匹配最后匹配完成的位置
- `\b`：匹配单词边界
- `\B`：匹配非单词边界（如：`er\B`可以匹配`verb`中的`er`，但不能匹配`never`中的`er`）

特殊字符：
- `\n`、`\r`、`\f`、`\t`：换行、回车、分页、缩进
- `\s`：任意空白字符（上述四种+空格）
- `\S`：任意非空字符
- `\d`：任意阿拉伯数字
- `\D`：任意非阿拉伯数字

组合表达式：
- `[...]`：匹配一个列表内的字符
	- `x-y`：匹配ASCII在区间`[x, y]`内的一个字符，须在`[]`内使用
- `[^...]`：匹配不在列表内的一个字符
- `re*`：匹配0或多个`re`
- `re+`：匹配1或多个`re`
- `re?`：匹配0或1个`re`，非贪婪方式
- `re{n}`：匹配n个`re`
- `re{n,}`：匹配至少n个`re`
- `re{n,m}`：匹配至少n个、至多m个`re`
- `a|b`：匹配a或b

表达式分组：参见runoob，懒得整理了

## 库方法

串查找/匹配：
- `re.match(regexp, text)`：从文本串开头匹配，返回匹配内容或`None`
- `re.search(regexp, text)`：全文搜索，返回首个匹配或`None`
- `re.findall(regexp, text)`：全文搜索，返回所有匹配的列表或`[]`

串处理：
- `re.sub(regexp, to, text, count?)`：全文搜索所有匹配实例并全部替换为`to`
- `re.split(regexp, text)`：将所有匹配删除，并将剩余部分作为列表返回

## 编译模式串

```python
ptn = re.compile(r'\d+')
result = ptn.match('123abc') # '123'
result = ptn.match('abc321') # None
```

## 控制常量

作为库方法的最后一个位置参数（可选），控制方法的行为

- `re.IGNORECASE`、`re.I`：忽略大小写
- `re.DOTALL`、`re.S`：令英文句点`.`可匹配所有字符，*包括换行符*
- `re.M`：多行匹配
- `re.L`：本地化识别（local-aware）匹配
- `re.U`：根据Unicode字符集解析字符
- `re.X`：允许更灵活、易懂的regex语法

## hack

```python
ptn_word = r'\b\w+\b' # 单个英语单词
ptn_telnum = r'\d{3}-\d{4}-\d{4}' # 移动号码
ptn_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # 邮箱
ptn_html_label = r'<.*?>' # HTML标签
```