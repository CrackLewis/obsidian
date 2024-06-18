
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

系统环境变量可以导入Makefile，但如果存在同名的自定义变量，则会被覆盖。指定