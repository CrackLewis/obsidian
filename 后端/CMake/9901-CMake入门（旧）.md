CMake：C++项目编译的跨平台一致性

项目根目录下的CMakeLists.txt文件说明了生成规则

## 基本使用

指令语法：`指令(参数1 参数2 ...)`

项目生成方法：

- `cd [项目根目录]`
- `mkdir build`
- `cd build`
- `cmake .. -A [平台名称]  -T [工具集名称] -D[外部参数]`
- 在`build`目录下，会有对应平台的C++项目文件，在各平台下生成目标程序

## 重要指令

1、形式化（~~八股化~~）：放在CMakeLists.txt文件头部

`cmake_minimum_required(VERSION [版本号])`：指定CMake程序的最低版本

`project([项目名] [CXX/C/JAVA] [VERSION 版本号])`：工程名称定义

2、文件内部变量定义：

`set(变量名 [变量值] [CACHE TYPE DOCSTRING [FORCE]])`

访问变量用`${变量名}`的形式，大小写敏感

3、添加目录：

`include_directories([AFTER|BEFORE] [SYSTEM] dir1 dir2 ...)`：添加头文件搜索路径（-I），作用范围为整个项目

`link_directories(dir1 dir2 ...)`：添加库文件搜索路径（-L），作用于整个项目

4、添加特定文件：

`add_executable(目标文件名 src1 src2 ...)`：添加目标程序文件（-o），这些目标文件可作为target被后文的target_*命令使用

`add_library(库名 [SHARED|STATIC|MODULE] [EXCLUDE_FROM_ALL] source1 source2 ..)`：添加目标库文件`lib***.(a/so)`

`add_compile_options(参数)`：添加编译参数

5、针对特定目标的动作：

`target_link_libraries(target lib1 [debug/optimized] lib2 ..)`：为特定目标添加库文件

6、其他

`add_subdirectory(srcdir [bindir] [EXCLUDE_FROM_ALL])`：添加源文件子目录（要求子目录有CMakeLists.txt）

`aux_source_directory(文件夹路径 变量名)`：将一个路径下的所有源码文件存储到一个变量中

## 常用变量

CMAKE_C_FLAGS：gcc编译选项

CMAKE_CXX_FLAGS：g++编译选项

CMAKE_BUILD_TYPE：编译类型（Debug/Release）

EXECUTABLE_OUTPUT_PATH：可执行文件输出路径

LIBRARY_OUTPUT_PATH：库文件输出的存放路径

