
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
	- `start.c`：开机时操作，执行在machine mode下
	- `string.c`：字符串操作
- 进程管理：
	- 中断和系统调用：
		- `trap.c`：中断响应和返回逻辑
		- `plic.c`：RISC-V架构的中断控制
		- `syscall.c`：系统调用实现（其它）
		- `sysfile.c`：系统调用实现（文件相关）
		- `sysproc.c`：系统调用实现（进程相关）
		- `exec.c`：exec系统调用，加载并执行用户程序
	- 互斥：
		- `sleeplock.c`：长期锁（会让出CPU的锁）操作
		- `spinlock.c`：自旋锁（不会让出CPU的锁）操作
	- `proc.c`：进程相关操作
- 内存管理：
	- `vm.c`：虚拟内存，对页表和地址空间进行管理
	- `kalloc.c`：物理内存分配
- I/O管理：
	- `bio.c`：文件系统的磁盘块缓存
	- `uart.c`：串行端口控制台驱动
	- `virtio_disk.c`：磁盘驱动
	- `pipe.c`：管道
	- `console.c`：控制台操作
	- `printf.c`：控制台格式化输出
- 文件管理：
	- `file.c`：文件描述符操作
	- `fs.c`：文件系统操作
	- `log.c`：文件系统日志和故障恢复

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

2.1: abstracting physical resources
- isolation
- forbid apps from accessing hardwares themselves
- time-share CPUs among processes, saving and restoring process states when necessary
- use file descriptors to abstract away I/O details

2.2: user mode, supervisor mode, system calls
- strong isolation: app failure shall not affect the system and other apps
- *RISC-V privileges*: machine mode>supervisor mode>user mode
	- supervisor mode: run in kernel space, can use privileged instrs
	- user mode: run in user space, arithmetic, jump, func call/ret, push/pop, move, etc.
- accessing kernel from app: 
	- system calls
	- kernel controls the kernel entry point

2.3: kernel organization
- *monolithic kernel*（宏内核）: 
	- the entire OS runs in supervisor mode, when apps run in user mode
	- OS design is easier
	- interactions within kernel is complex, and mistakes are pretty much fatal
- *microkernel*:
	- minimalize OS parts running in supervisor mode, so the bulk of OS runs in user mode instead
	- OS services run as special processes called servers
	- kernel interface is simpler
- xv6 is monolithic

2.4: xv6 organization
[[#有关文件]]

2.5: process overview
- xv6 isolation unit is a process
	- process cannot wreck or spy on kernel or other processes, or circumvent isolation
	- mechanisms: user/supervisor mode flags, addr spaces, time-slicing of threads, etc.
	- each process thinks it owns a private machine
- page table:
	- one for each process, records their address space
	- xv6 uses 38 bits to represent a phys. addr., so the maximum addr. is `0x3fffffffff`
- process state:
	- `struct proc`: page table, kernel stack, run state, etc.
		- `p->state`: process running state (allocated, ready, running, waiting, exiting)
		- `p->pagetable`: RISC-V page table
	- "thread": holds the state needed to execute the process
	- process switch: suspend the current thread->save its state->restore another process's thread
	- user stack VS kernel stack: former is used when running app, latter is used in kernel
- system call:
	- `ecall` instr. raise hw. priv. lvl. and changes PC to kernel entry
	- the code at kernel entry switches to kernel stack and executes the syscall impl.
	- after the syscall, kernel switches back to user stack and returns to user space by calling `sret` instr., which lowers hw. priv. and recovers old PC
- in general: address space by pagetable + thread by process state

2.6: code: starting xv6, the first proc. and syscall

State: (A|B)
- A: privilege mode (Machine/Supervisor/User)
- B: paging hardware status (Enabled/Disabled)

Boot process:
- machine powers on
- state: (M|D)
- machine initializes itself and runs a bootloader in ROM, which loads xv6 into memory address `0x80000000`
- CPU executes xv6 starting at `_entry` (*kernel/entry.S:7*)
- instr.s at `_entry` set up a stack at `stack0` (*kernel/start.c:11*) so xv6 can run C code
- func `start` (*kernel/start.c:15*) is called
- func `start` performs some machine mode-specific configs, and then switches into supervisor mode by instr `mret`:
	- `mret` returns to priv. lvl. in `mstatus` and addr `mepc` from a supervisor mode func call, so `start` sets priv. in `mstatus` to be supervisor mode, and `mepc` to be addr. of func `main`
	- virt. addr. mapping in sup. mode is disabled by setting page-table reg. `satp` to 0
	- all interrupts and exceptions are delegated to sup. mode
	- programs the clock chip to generate time interrupts
	- state: (M|D)
	- instr `mret` is executed
	- state: (S|D)
	- PC is set to func `main` (*kernel/main.c:11*)
- `main` initializes several devs. and subsys.
- `main` creates the 1st process by calling `userinit` (*kernel/proc.c:233*)
- the 1st process execs. a RISC-V program, which makes the first syscall in xv6:
	- `initcode.S` loads the number for the `exec` syscall, i.e. `SYS_EXEC`, into reg. `a7`, and then calls `ecall` to re-enter the kernel
	- `a7` is used as syscall nums in func `syscall` (*kernel/syscall.c:132*). kernel maps `SYS_EXEC` to func `sys_exec` in syscall table, and then calls it to replace the current program of the process to `/init`
- `/init` creates a new console device file if needed, and then opens it as fd 0, 1, and 2
- `/init` starts a shell on the console
- the system is up