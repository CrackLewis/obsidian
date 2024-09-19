
## 环境配置



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

## 进程管理

