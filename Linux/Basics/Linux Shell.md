
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

| 操作符     | 说明                                       | 举例                     |
| ------- | ---------------------------------------- | ---------------------- |
| -b file | 检测文件是否是块设备文件，如果是，则返回 true。               | [ -b $file ] 返回 false。 |
| -c file | 检测文件是否是字符设备文件，如果是，则返回 true。              | [ -c $file ] 返回 false。 |
| -d file | 检测文件是否是目录，如果是，则返回 true。                  | [ -d $file ] 返回 false。 |
| -f file | 检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。 | [ -f $file ] 返回 true。  |
| -g file | 检测文件是否设置了 SGID 位，如果是，则返回 true。           | [ -g $file ] 返回 false。 |
| -k file | 检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。   | [ -k $file ] 返回 false。 |
| -p file | 检测文件是否是有名管道，如果是，则返回 true。                | [ -p $file ] 返回 false。 |
| -u file | 检测文件是否设置了 SUID 位，如果是，则返回 true。           | [ -u $file ] 返回 false。 |
| -r file | 检测文件是否可读，如果是，则返回 true。                   | [ -r $file ] 返回 true。  |
| -w file | 检测文件是否可写，如果是，则返回 true。                   | [ -w $file ] 返回 true。  |
| -x file | 检测文件是否可执行，如果是，则返回 true。                  | [ -x $file ] 返回 true。  |
| -s file | 检测文件是否为空（文件大小是否大于0），不为空返回 true。          | [ -s $file ] 返回 true。  |
| -e file | 检测文件（包括目录）是否存在，如果是，则返回 true。             | [ -e $file ] 返回 true。  |

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

文件运算符示例：

```sh
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

file="/var/www/runoob/test.sh"
if [ -r $file ]
then
   echo "文件可读"
else
   echo "文件不可读"
fi
if [ -w $file ]
then
   echo "文件可写"
else
   echo "文件不可写"
fi
if [ -x $file ]
then
   echo "文件可执行"
else
   echo "文件不可执行"
fi
if [ -f $file ]
then
   echo "文件为普通文件"
else
   echo "文件为特殊文件"
fi
if [ -d $file ]
then
   echo "文件是个目录"
else
   echo "文件不是个目录"
fi
if [ -s $file ]
then
   echo "文件不为空"
else
   echo "文件为空"
fi
if [ -e $file ]
then
   echo "文件存在"
else
   echo "文件不存在"
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

## 命令

`echo`命令最常见，不多讲。

`printf`命令类似于C中的`printf`函数，也不多讲。

`test`命令可用于测试关系表达式和字符串表达式等，还是不多讲。

`read`命令读取一个值到一个Shell变量中：

```sh
read VAR
echo $VAR # 取决于用户输入
```

`let`命令可以计算参数内的表达式，参数内部无需用`$`引用变量。

```sh
VAR=2
let "VAR=VAR*2+3"
echo $VAR # 7
```

## 流程控制

### 分支控制

条件表达式的编写：
- `[[]]`记法：必须使用`-lt`、`-gt`等，如`[[ "$a" -gt "$b" ]]`
- `(())`记法：可以使用`>`、`<`等，如`(( a > b ))`
- 如果`if`、`then`在同一行，表达式后要加分号

`if-else`语句：与大部分语言不同的是，它不允许子语句为空：

```sh
if condition 
then
	command1
	command2 # 至少一条指令
fi
```

`if-else-if`语句：

```sh
if condition1 then
	command1
elif condition2 then
	command2
elif condition3 then
	command3
else 
	command4
fi
```

`case`语句：格式比较古怪，每个case名后要加右括号，指令后又要加双分号。注意结束符`esac`是`case`的反写。

```bash
case value in
pattern1)
	command1
	;;
pattern2)
	command2
	;;
pattern3)
	command3
	;;
*) # 默认模式
	command4
	;;
esac
```

### 循环控制

`for`循环：用于遍历一个数组或列表：

```sh
for var in item1 item2 item3
do
	command1
	command2
done

for var in arr
do
	command3
	command4
done

# 输出1-20
for var in $(seq 1 20); do echo $var; done
for var in {1..20}; do echo $var; done
```

`while`循环：

```sh
while condition
do
	command
done
```

`until`循环：与`while`相反，它只在condition为假时循环执行命令。

```sh
until condition
do
	command
done
```

*无条件循环*：有以下几种方案：

```sh
while :
do 
	command
done

while true; do
	command
done

until false; do
	command
done

for (( ; ; ))
do
	command
done
```

### 跳转

`break`语句跳出所有循环，例如下面这个例子：

```sh
#!/bin/bash
while :
do
    echo -n "输入 1 到 5 之间的数字:"
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的! 游戏结束"
            break
        ;;
    esac
done
```

`continue`语句跳出本次循环，但仍继续执行后面的循环：

```sh
#!/bin/bash
while :
do
    echo -n "输入 1 到 5 之间的数字: "
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的!"
            continue
            echo "游戏结束"
        ;;
    esac
done
```

## 函数

用户可自行定义Shell函数。基本格式：

```sh
# function可省略
function func()
{
	action;
	# 如果没有return语句，将返回最后一条指令的返回值。
	return int;
}
```

### 传递参数

Shell函数没有类似函数列表的机制，访问参数通过访问特殊变量实现。

访问`$1,$2`表示访问第1、2个参数，依此类推。注意访问第10个参数要写成`${10}`。

| 参数处理 | 说明                              |
| ---- | ------------------------------- |
| $#   | 传递到脚本或函数的参数个数                   |
| $*   | 以一个单字符串显示所有向脚本传递的参数             |
| $$   | 脚本运行的当前进程ID号                    |
| $!   | 后台运行的最后一个进程的ID号                 |
| $@   | 与$*相同，但是使用时加引号，并在引号中返回每个参数。     |
| $-   | 显示Shell使用的当前选项，与set命令功能相同。      |
| $?   | 显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。 |

示例：

```sh
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

funWithParam(){
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
    echo "第十个参数为 ${10} !"
    echo "第十一个参数为 ${11} !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}
funWithParam 1 2 3 4 5 6 7 8 9 34 73
```

## 输入输出重定向

|命令|说明|
|---|---|
|command > file|将输出重定向到 file。|
|command < file|将输入重定向到 file。|
|command >> file|将输出以追加的方式重定向到 file。|
|n > file|将文件描述符为 n 的文件重定向到 file。|
|n >> file|将文件描述符为 n 的文件以追加的方式重定向到 file。|
|n >& m|将输出文件 m 和 n 合并。|
|n <& m|将输入文件 m 和 n 合并。|

### 高级用法

fds:
- 0: stdin
- 1: stdout
- 2: stderr

合并stdout和stderr，并输出到同一文件：

```sh
command 1>file 2>&1
```

黑洞文件：

```sh
command 1>/dev/null
```

### 借助Here文档的重定向

Shell允许将输入或输出重定向到一个脚本内：

```sh
wc -l << EOF
    欢迎来到
    菜鸟教程
    www.runoob.com
EOF
# 输出：3（表示输入共3行）
```

## 文件包含

两种写法（假设被包含的脚本为`test.sh`）：

```sh
. ./test.sh # 注意有一个间隔空格
source ./test.sh
```