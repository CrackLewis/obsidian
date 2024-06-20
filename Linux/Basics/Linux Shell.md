
参考：
- [runoob](https://www.runoob.com/linux/linux-shell.html)
- 

## 变量

变量需要先定义后使用。

命名规则：
- 只包含字母、数字、下划线，不能以数字开头，不能使用特殊符号和空格。
- 不能使用Shell关键字：`if`、`fi`、`then`、`else`、`case`、`esac`、`for`、`endfor`、`while`等。

字符串变量的声明格式为`varname=value`，等号左侧不能有空格。等号右侧如有空格，则需要用双引号包裹：

```sh
VAR="hello, world"
```

整数变量的声明通过`declare -i`实现：

```sh
declare -i MY_INT=42
```

索引数组变量的声明通过`declare -a`实现，类似于其它语言的数组：

```sh
declare -a MY_INDEXED_ARR=(1 2 3 4 5)
echo ${MY_INDEXED_ARR[0]} # 1
echo ${MY_INDEXED_ARR[3]} # 4
```

关联数组的声明通过`declare -A`实现，类似于其它语言的字典：

```sh
declare -A MY_ASSOC_ARR
MY_ASSOC_ARR["name"]="John"
MY_ASSOC_ARR["age"]=30
echo ${MY_ASSOC_ARR[name]} # John
```

*访问变量*可通过在前加`$`的方式访问，但更推荐`${}`：

```sh
VAR="hello, world"
echo $VAR
echo ${VAR}
```

*声明只读变量*可以使用`readonly`关键字：

```sh
myUrl="https://www.google.com"  
readonly myUrl  
myUrl="https://www.runoob.com" # /bin/sh: NAME: This variable is read only.
```

*删除变量*需要使用`unset`关键字：

```sh
VAR=hello
echo $VAR # hello
unset VAR
echo $VAR # <无输出>
```

## 数据类型

### 字符串

| 项目\\类型  | 单引号字符串      | 双引号字符串        |
| ------- | ----------- | ------------- |
| 格式      | `'content'` | `"content"`   |
| 特点      | 字符原样输出      | 字符可能会转义、代入变量等 |
| 可包含变量   | 否           | 是             |
| 可包含转义字符 | 否           | 是             |
| 可包含单引号  | 必须成对        | 是             |
| 可包含双引号  | 是           | 必须成对          |

示例：

```sh
your_name="runoob"
# 使用双引号拼接
greeting="hello, "$your_name" !"
greeting_1="hello, ${your_name} !"
echo $greeting  $greeting_1
# 输出：hello, runoob ! hello, runoob !

# 使用单引号拼接
greeting_2='hello, '$your_name' !'
greeting_3='hello, ${your_name} !'
echo $greeting_2  $greeting_3
# 输出：hello, runoob ! hello, ${your_name} !
```

*获取字符串长度*可用`${#str}`的方式：

```sh
VAR=0123456789ABCDEF
echo ${#VAR[0]} # 16
echo ${#VAR} # 16
```

*提取子字符串*可用`${str:a:b}`的方式，表示截取偏移区间为`[a,a+b)`的子串。注意汉字算一个索引：

```sh
VAR=0123456789ABCDEF一二三四五六
echo ${VAR:9:8} # 9ABCDEF一
```

*查找子字符串*可借助后面会用到的`expr`命令。注意，输出值为下标值（起始为1）而非偏移值。

```sh
VAR=0123456789ABCDEF一二三四五六
echo $(expr index "$VAR" 二) # 输出：18
```

### 数组

数组定义可以借助`declare -[Aa]`。特别地，索引数组也可以直接定义：

```sh
ARR=(apple banana cherry grape kiwi lemon)
```

*读取数组元素*建议采取`${arrname[idx]}`的形式：

```sh
echo ${ARR[3]} # grape
```

特别地，*获取所有数组元素*采用`${arrname[@]}`的形式：

```sh
echo ${ARR[@]} # apple banana cherry grape kiwi lemon
```

*获取数组长度*可以加`#`：

```sh
echo ${#ARR[@]} # 6
echo ${#ARR[*]} # 6
echo ${#ARR[0]} # 5，注意这是单个元素的长度
```

## 运算符

### 运算符种类

主要种类：
- 算术运算符：四则、取模、赋值
- 关系运算符：相等（`==`）、不相等（`!=`）、`-lt`、`-le`、`-gt`、`-ge`、`-eq`、`-ne`。
- 布尔运算符：非（`!`）、与（`-a`）、或（`-o`）。
- 逻辑运算符：`&&`、`||`。
- 字符串运算符：相等（`=`）、不相等（`!=`）、长度为0（`-z`）、长度不为0（`-n`）、串不为空（`$`）
- 文件测试运算符：见下表。
- 其他检查符：
	- 判断某个文件是否为socket：`-S`
	- 判断某个文件是否为软链接：`-L`

|操作符|说明|举例|
|---|---|---|
|-b file|检测文件是否是块设备文件，如果是，则返回 true。|[ -b $file ] 返回 false。|
|-c file|检测文件是否是字符设备文件，如果是，则返回 true。|[ -c $file ] 返回 false。|
|-d file|检测文件是否是目录，如果是，则返回 true。|[ -d $file ] 返回 false。|
|-f file|检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。|[ -f $file ] 返回 true。|
|-g file|检测文件是否设置了 SGID 位，如果是，则返回 true。|[ -g $file ] 返回 false。|
|-k file|检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。|[ -k $file ] 返回 false。|
|-p file|检测文件是否是有名管道，如果是，则返回 true。|[ -p $file ] 返回 false。|
|-u file|检测文件是否设置了 SUID 位，如果是，则返回 true。|[ -u $file ] 返回 false。|
|-r file|检测文件是否可读，如果是，则返回 true。|[ -r $file ] 返回 true。|
|-w file|检测文件是否可写，如果是，则返回 true。|[ -w $file ] 返回 true。|
|-x file|检测文件是否可执行，如果是，则返回 true。|[ -x $file ] 返回 true。|
|-s file|检测文件是否为空（文件大小是否大于0），不为空返回 true。|[ -s $file ] 返回 true。|
|-e file|检测文件（包括目录）是否存在，如果是，则返回 true。|[ -e $file ] 返回 true。|

### 运算符使用

使用*算术运算符*计算表达式需要恰好符合以下形式，多打或少打空格都不允许：
- 一元运算符：`$(expr op a)`
- 二元运算符：`$(expr a op b)`

使用*其他运算符*在非Bash的Shell中用单方括号包围，Bash则建议使用双方括号包围。

算术运算符示例：

```sh
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

a=10
b=20

val=`expr $a + $b`
echo "a + b : $val"

val=`expr $a - $b`
echo "a - b : $val"

val=`expr $a \* $b`
echo "a * b : $val"

val=`expr $b / $a`
echo "b / a : $val"

val=`expr $b % $a`
echo "b % a : $val"

if [ $a == $b ]
then
   echo "a 等于 b"
fi
if [ $a != $b ]
then
   echo "a 不等于 b"
fi
```

关系运算符示例：

```sh
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

a=10
b=20

if [ $a -eq $b ]
then
   echo "$a -eq $b : a 等于 b"
else
   echo "$a -eq $b: a 不等于 b"
fi
if [ $a -ne $b ]
then
   echo "$a -ne $b: a 不等于 b"
else
   echo "$a -ne $b : a 等于 b"
fi
if [ $a -gt $b ]
then
   echo "$a -gt $b: a 大于 b"
else
   echo "$a -gt $b: a 不大于 b"
fi
if [ $a -lt $b ]
then
   echo "$a -lt $b: a 小于 b"
else
   echo "$a -lt $b: a 不小于 b"
fi
if [ $a -ge $b ]
then
   echo "$a -ge $b: a 大于或等于 b"
else
   echo "$a -ge $b: a 小于 b"
fi
if [ $a -le $b ]
then
   echo "$a -le $b: a 小于或等于 b"
else
   echo "$a -le $b: a 大于 b"
fi
```

逻辑运算符示例：

```sh
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

a=10
b=20

if [[ $a -lt 100 && $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"
fi

if [[ $a -lt 100 || $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"
fi
```

字符串运算符示例：

```sh
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

a="abc"
b="efg"

if [ $a = $b ]
then
   echo "$a = $b : a 等于 b"
else
   echo "$a = $b: a 不等于 b"
fi
if [ $a != $b ]
then
   echo "$a != $b : a 不等于 b"
else
   echo "$a != $b: a 等于 b"
fi
if [ -z $a ]
then
   echo "-z $a : 字符串长度为 0"
else
   echo "-z $a : 字符串长度不为 0"
fi
if [ -n "$a" ]
then
   echo "-n $a : 字符串长度不为 0"
else
   echo "-n $a : 字符串长度为 0"
fi
if [ $a ]
then
   echo "$a : 字符串不为空"
else
   echo "$a : 字符串为空"
fi
```



## 注释

Shell的注释格式比较乱。最常见的是行首加`#`：

```sh
# comment
###### comment begins
# he
# ll
# o
###### comment ends
```

对于多行注释，可以采用*Here文档*，一种独有格式：

```sh
:<<COMMENT
This script does what you think it does.
You're not expected to understand this.
COMMENT
```

也可以直接使用冒号：

```sh
: '
This script is deprecated.
V
V
V
V
V (after 9,223,372,036,854,775,808 lines)
V
WHY ARE YOU STILL READING IT?
'
```

