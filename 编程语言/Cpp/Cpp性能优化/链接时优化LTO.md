
*链接时优化*（link-time optimization, LTO）允许链接器实现跨翻译单元的优化，如：跨目标文件内联、优化内存布局，等等

编译和链接阶段都必须使用`-flto`标记。另外必须使用编译器而非链接器`ld`。

```sh
# 1. 编译阶段：为每个源文件生成包含GIMPLE中间表示的目标文件
gcc -c -O2 -flto file1.c -o file1.o
gcc -c -O2 -flto file2.c -o file2.o

# 2. 链接阶段：执行LTO优化并生成最终可执行文件
gcc -O2 -flto file1.o file2.o -o my_program
```

Clang启用的方式总体类似，但Clang支持完全（`-flto=full`）和部分（`-flto=thin`）LTO。前者将所有中间表示合成为一个大模块，后者则是通过全局索引和并行优化，在接近Full-LTO的情形下降低开销。