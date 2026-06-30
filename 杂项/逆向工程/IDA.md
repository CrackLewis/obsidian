
ref's:
- IDA Pro 权威指南第二版，Chris Eagle原著，人民邮电出版社

*IDA（Interactive DisAssembler）* 是一个强大的反汇编程序、反编译器和多功能调试器

下载链接：[baidu](https://pan.baidu.com/s/18aY2AAr23XUZUhrD5W33nw?pwd=6666)
- IDA安装密码：QQ565887

## 相关概念

*反汇编*（disassemble）：对应平台机器码转换到对应平台的汇编码
- 大致步骤：确定代码段，解析指令并生成符号表，符号表前后链接，汇编语言格式化和输出
- 算法：线性扫描/递归下降

*逆向与反汇编工具*：
- 分类工具：
	- `file`：分析文件，确认文件类型
	- PE tools：分析Windows所有活动进程
	- PEiD：识别PE文件使用的编译器
- 摘要工具：
	- `nm <binary_file>`：列举二进制目标文件中的符号
	- `ldd <binary_file>`：列举目标文件的动态库依赖
	- `objdump <options> <binary_file>`：显示目标文件的详细信息，如：节信息、专用头部、调试信息、符号信息、反汇编代码清单等
	- `otool <options> <binary>`：在MacOS系列系统中显示动态库依赖
	- `dumpbin <options> <binary>`：在Windows系列系统中起到objdump的作用
	- `c++filt`：将nm输出的符号转换为可读性更高的函数签名等
- 深度检测工具：
	- `strings <binary>`：输出目标文件中的符号表
	- 反汇编器：nasm等

## IDA基本用法

