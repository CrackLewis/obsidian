
## 环境配置

烂尾了，靠一个Docker镜像续命中

## 有关文件

头文件：
- 全局：
	- `defs.h`：源文件函数定义
	- `param.h`：系统参数，如进程数、CPU核数等
	- `riscv.h`：RISC-V架构相关
	- `types.h`：基础类型的别名
- 进程相关：
	- `proc.h`：进程管理结构
	- `sleeplock.h`：进程用的长期锁
	- `spinlock.h`：自旋互斥锁
	- `elf.h`：ELF程序结构
	- `syscall.h`：系统调用编号
- 内存相关：
	- `memlayout.h`：内存布局
- I/O相关：
	- `buf.h`：缓存结构
	- `virtio.h`：virtio设备相关
- 文件系统相关：
	- `stat.h`：stat结构（文件记录？）
	- `fcntl.h`：文件描述符模式
	- `file.h`：底层文件设施
	- `fs.h`：文件系统

源文件：
- 特殊：
	- `main.c`：操作系统入口
	- `start.c`：开机时操作
	- `string.c`：字符串操作
- 进程管理：
	- 中断和系统调用：
		- `trap.c`：中断响应逻辑
		- `plic.c`：平台级中断控制
		- `syscall.c`：系统调用实现（其它）
		- `sysfile.c`：系统调用实现（文件相关）
		- `sysproc.c`：系统调用实现（进程相关）
	- 互斥：
		- `sleeplock.c`：长期锁操作
		- `spinlock.c`：自旋锁操作
	- `proc.c`：进程相关操作
	- `exec.c`：加载并执行用户程序
- 内存管理：
	- `vm.c`：虚拟内存实现
	- `kalloc.c`：用户内存分配
- I/O管理：
	- `bio.c`：缓存块I/O
	- `uart.c`：UART逻辑，似乎是一种异步串行I/O控制器
	- `virtio_disk.c`：VirtI/O逻辑
	- `pipe.c`：管道
	- `console.c`：控制台操作
	- `printf.c`：控制台格式化输出
- 文件管理：
	- `file.c`：单文件操作
	- `fs.c`：文件系统操作
	- `log.c`：文件系统操作原子化

汇编码：
- `entry.S`：为每个CPU分别初始化不同的栈桢，并让它们跳转到`start`函数
- `kernelvec.S`：内核态下中断的处理
- `swtch.S`：切换进程上下文
- `trampoline.S`：用户态自陷（trap）的底层实现

## 读手册

[book-riscv-rev4](https://pdos.csail.mit.edu/6.828/2024/xv6/book-riscv-rev4.pdf)

### ch01-os界面

进程=用户内存空间+PCB
- fork
- exit
- wait
- kill
- getpid
- sleep
- exec
- sbrk

万物皆文件：外存文件、目录、设备、管道等
- open、close
- read、write
- dup：复制fd到第一个可用的空余fd

管道：由2个文件描述符`(p,q)`表示的内核缓冲区，从`q`写入的数据可以被`p`读出。
- pipe

文件系统：描述系统资源层次结构的系统
- chdir、mkdir
- mknod：创建一个设备文件
- fstat：获取文件信息
- link：创建软链接
- unlink：删除文件

### ch02-os组织

- time-share resources among processes
- ensure all processes can be executed
- isolation (but not complete)

ref: The RISC-V Reader: An Open Architecture Atlas

qemu: RISC-V hardware simulator
- RAM+ROM (with boot code)+serial ports+disk

