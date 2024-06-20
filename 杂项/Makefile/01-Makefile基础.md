
240618：3年前就接触过，一直拖拖拉拉，到今天才开坑，惭愧

参考资料：
- [blog](https://blog.csdn.net/weixin_38391755/article/details/80380786)：写的比较全但也比较乱

## Makefile基本结构

生成规则：

```makefile
target : prerequisites
	command1
	command2
	...
```

假设有一个C/C++的项目目录：

```
my_project
+ src
	+ main.cpp
	+ sub1.cpp
	+ sub2.cpp
+ include
	+ common.h
+ Makefile
```

那么可以这么写项目的`Makefile`：

```
.PHONY: all clean

CPPFLAGS = -Wall -g

all: main.o sub1.o sub2.o
	$(CXX) $(CPPFLAGS) -o main $@

clean:
	rm -rf *.o main
```

## 变量

变量是在定义后可用于Makefile内其他地方的标识符。

变量总是需要先定义，后使用。

变量会在使用的位置精确地展开，就像C/C++的宏一样：

```
foo = c

prog.o : prog.$(foo)  
	$(foo)$(foo) -$(foo) prog.$(foo) # 展开为cc -c prog.c
```

### 变量定义

太长不读：
- `=`：递归展开
- `:=`：立即展开
- `+=`：追加定义
- `?=`：仅当不存在时定义

变量定义时如使用其他变量，则不会展开，而是会等到使用时再展开。

```
FOO = $(BAR)
BAR = $(LAC)
LAC = Huh?

all:
	@echo $(FOO)$(FOO) # 输出Huh?Huh?
```

*循环引用*是不允许的，Makefile会自行检测这种引用并阻止：

```
FOO = $(BAR)
BAR = $(FOO)

all:
	@echo $(FOO)
```

一种解决方案是使用立即展开符号`:=`。立即展开要求使用的变量必须存在：

```
x := foo
y := $(x) bar  # 这个y会立刻展开为foo bar，不会作为$(x) bar
x := later # x重定义为later，但不影响y
```

`?=`可以避免非预期的重定义：

```
FOO ?= val
```

等价于：

```
ifeq ($(origin FOO), undefined)  
FOO = val
endif
```

追加变量符号`+=`可以为变量追加值：

```
FOO = foo
FOO += bar # 此时FOO展开为foo bar
```

### 变量高级用法

太长不读：
- 变量值的替换：`$(varname:old=new)`
- 变量的值作为变量：`$($(varname))`、`$($(a)_$(b))`等。
- 覆盖赋值：`override VAR=value`。

### 多行变量

变量定义可以展开为多行，需要用`define-endef`块包裹：

```
define two_lines
echo foo
echo $(bar)
endef
```

### 环境变量

系统环境变量可以导入Makefile，但如果存在同名的自定义变量，则会被覆盖。指定`-e`参数可以让环境变量覆盖自定义变量。

### 目标和模式变量

假设全局的`CFLAGS`是`-O2 -g`，但对于部分规则需要将`CFLAGS`设为`-Wall -g`。可以通过指定*目标内变量*进行修改：

```
prog : CFLAGS = -Wall -g
prog : prog.o foo.o bar.o  
	$(CC) $(CFLAGS) prog.o foo.o bar.o  
  
prog.o : prog.c  
	$(CC) $(CFLAGS) prog.c  
  
foo.o : foo.c  
	$(CC) $(CFLAGS) foo.c  
  
bar.o : bar.c  
	$(CC) $(CFLAGS) bar.c
```

类似地，也支持设置*模式内变量*：

```
%.o: CFLAGS = -o
```

### 自动化变量

详见[[#隐含规则]]

## 函数

函数是一种内建的可调用方法，用于实现变量计算、执行命令等。

调用格式：

```
$(func_name args)
```

示例：

```
comma:= ,
empty:=  # 注意这里有个空格
space:= $(empty) $(empty)
foo:= a b c
bar:= $(subst $(space),$(comma),$(foo)) # bar此时为a,b,c
```

### 字符串处理函数

| 函数签名                          | 功能                                     |
| ----------------------------- | -------------------------------------- |
| `$(subst from,to,text)`       | 将`text`内的所有`from`子串替换为`to`子串           |
| `$(patsubst patt,repl,text)`  | 将`text`内所有匹配`patt`模式的*单词*替换为`repl`子串   |
| `$(strip text)`               | 去除`text`前后的空字符                         |
| `$(findstring find,in)`       | 在`in`字符串中寻找`find`，找到则返回`find`，否则返回空串   |
| `$(filter patterns,text)`     | 在`text`中过滤，保留并返回匹配至少一个`pattern`的单词     |
| `$(filter-out patterns,text)` | 在`text`中过滤，去除匹配至少一个`pattern`的单词，返回其余单词 |
| `$(sort words)`               | 对单词序列`words`按字典序升序排列                   |
| `$(word n,text)`              | 取`text`字符串的第`n`个单词，下标为1                |
| `$(wordlist a,b,text)`        | 取`text`字符串的第`a~b`个单词并返回                |
| `$(words text)`               | 返回`text`单词数量                           |
| `$(firstword text)`           | 等价于`$(word 1,text)`                    |

例子：make会依赖`VPATH`进行依赖文件查找，利用字符串函数可以在`CFLAGS`中添加对应的头文件包含路径，这样`VPATH=src:../headers`对应`CFLAGS+=-Isrc -I../headers`。

```
override CFLAGS += $(patsubst %,-I%,$(subst :, ,$(VPATH)))
```

### 文件名操作函数

| 函数签名                        | 功能                       |
| --------------------------- | ------------------------ |
| `$(dir names)`              | 从文件名序列`names`中取出文件所在目录序列 |
| `$(notdir names)`           | 从文件名序列`names`中取出文件名序列    |
| `$(suffix names)`           | 从文件名序列`names`中取出文件名后缀序列  |
| `$(basename names)`         | 从文件名序列`names`中取出文件名前缀序列  |
| `$(addsuffix suffix,names)` | 对序列`names`的每个成员添加后缀      |
| `$(addprefix prefix,names)` | 对序列`names`的每个成员添加前缀      |
| `$(join list1,list2)`       | 拼接两个等长列表内的对应元素           |

### foreach

`$(foreach var,list,text)`

含义：将`list`成员依次绑定到`var`上，每绑定一次，便展开一次`text`。

例子：

```
names := a b c d
objects := $(foreach n, $(names), $(n).o)
# 展开结果为a.o b.o c.o d.o
```

### if

`$(if cond,then[,else])`

含义：如果`cond`代表的串非空，则展开为`then`。如果`cond`为空则展开为`else`，如果`else`也为空则返回空。

### call

`$(call expr,arg1,arg2[,...])`

含义：根据`arg1,arg2,...`的具体内容对`expr`进行展开，可以理解为类似C/C++的宏展开。`expr`内通过`$(1),$(2),...`依次访问代入的各个参数。

例子：

```
reverse = $(2) $(1)  
foo = $(call reverse,a,b)
# 此时foo为b a
```

### origin

`$(origin var)`

含义：解释变量`var`来自于哪里：
- `undefined`：未定义
- `default`：默认定义的变量
- `environment`：环境变量
- `file`：Makefile内定义的变量
- `command line`：命令行定义的变量
- `override`：被override指示符重新定义的
- `automatic`：自动化变量

### shell

`$(shell command)`

含义：生成一个Shell进程，专门执行`command`命令。

### wildcard

`$(wildcard pattern)`

含义：展开为符合`pattern`的所有本地路径。

### 控制函数

`$(error msg)`

含义：产生一个信息为`msg`的致命错误。

`$(warning msg)`

含义：产生一个信息为`msg`的警告。

## 隐含规则

一些常见的源文件或中间文件有默认的生成规则。如无人为指定规则，则会按默认规则生成这些文件：

| 目标            | 源            | 命令                                            |
| ------------- | ------------ | --------------------------------------------- |
| `1.o`（C依赖）    | `1.c`        | `$(CC) -c $(CPPFLAGS) $(CFLAGS)`              |
| `1.o`（C++依赖）  | `1.cc`或`1.C` | `$(CXX) -c $(CPPFLAGS) $(CFLAGS)`             |
| `1.o`（汇编依赖）   | `1.s`        | `$(AS) $(ASFLAGS) 1.s`                        |
| `1.s`         | `1.S`        | `$(AS) $(ASFLAGS) 1.S`                        |
| `1`           | `1.o`        | `$(CC) $(LDFLAGS) 1.o $(LOADLIBES) $(LDLIBS)` |
| `1.c`（Yacc依赖） | `1.y`        | `$(YACC) $(YFLAGS)`                           |
| `1.c`（Lex依赖）  | `1.l`        | `$(LEX) $(LFLAGS)`                            |


隐含规则可通过*模式规则*定义。规则中需要使用`%`替代一或多个任意字符。与变量和函数在Makefile加载时展开不同，`%`在运行时才展开。

使用`%`的规则会将所有的`%`展开为相同内容。

示例：

```
%.o : %.c
	$(CC) -c $(CFLAGS) $(CPPFLAGS) $< -o $@
```

*自动化变量*：在模式规则中有特定含义。
- `$<`：指代第一个依赖项。
- `$^`：指代所有依赖项（去重）。
- `$+`：指代所有依赖项（不去重）。
- `$?`：指代依赖项中比目标文件更新的（即需要重新生成的）项。
- `$@`：指代目标。
- `$%`：比较抽象，它仅在目标是函数库文件时，表示规则中的目标成员名。例如，如果一个目标是“foo.a(bar.o)”，那么，`$%`就是“bar.o”，“$@”就是“foo.a”。如果目标不是函数库文件（Unix下是`.a`，Windows下是`.lib`），那么，其值为空。
- `$*`：指代目标模式中`%`及之前部分。假如模式为`a.%.b`，匹配目标为`src/a.foo.b`，则`$*`展开为`src/a.foo`。

部分自动化变量可以加后缀，表示扩展含义：
- `D`：表示目录部分。例如：`$(@D)`表示目标的目录部分。
- `F`：表示文件部分。例如：`$(?F)`表示被更新的依赖项的文件部分。

模式规则可以重载隐含规则。

## Makefile书写技巧

命令前加`-`表示无视可能的错误，继续执行后面的命令。

命令前加`@`表示命令不回显。

`.PHONY`用于显式声明伪目标。

`include`用于包含其他Makefile文件。

`VPATH`是一个特殊的内置变量，用于文件搜索。

嵌套执行make指令可以采用这种方式：

```
submod1 submod2 submod3:
	cd $@ && $(MAKE)
```

可以将大量重复的指令序列定义为指令包：

```
define gcomm
comm1
comm2
endef
```

## Makefile运行



## Makefile参数

WIP