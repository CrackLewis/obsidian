
我个人没找到如何通过`make target`的方式直接生成目标的方法。但是通过指定变量的方式生成则可以：

例如：C++源码目录，要求通过自定义变量的方式，编译、生成并运行单个源文件。

```makefile
# 约定TARGET是编译目标
CXXFLAGS += -Wall -g -O2

INCLUDE = ./include
SRC_FILE = $(TARGET).cpp

$(TARGET): $(SRC_FILE)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC_FILE)

run: $(TARGET)
	$(TARGET)
```

如需编译并运行`demo.cpp`，可直接：

```
make run TARGET=demo
```