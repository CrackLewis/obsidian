
240618：3年前就接触过，一直拖拖拉拉，到今天才开坑，惭愧

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

循环引用是不允许的，Makefile会自行检测这种引用并阻止：

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

### 环境变量

系统环境变量可以导入Makefile，但如果存在同名的自定义变量，则会被覆盖。指定`-e`参数可以让环境变量覆盖自定义变量。

