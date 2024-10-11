
2401210309 李博宇

## 环境配置

根据实验文档介绍，在本地搭建实验环境有以下数种方案：
- CLab云主机：学校提供的主机，最高支持4核4GB内存。
- 虚拟机：利用虚拟机软件在本地创建虚拟机，在虚拟机内配置并运行xv6系统。
- WSL：在WSL（Windows的Linux子系统）下搭建并运行系统。
- Docker：在Docker容器中搭建并运行系统。

综合权衡后，我选择的是Docker方案，因为运行虚拟机需要更大的开销，而个人的WSL环境比较杂乱，在内部搭建、运行xv6的可行性并不高，而Docker容器的开销较低，更适合实验环境的搭建。

我个人是从网上拉取的一个自带交叉编译器和QEMU的镜像，原因是xv6对环境要求较为严苛，版本安装错可能导致xv6启动失败：

```sh
$ docker pull dockerproxy.cn/svkv/riscv-tools:v1.0
$ docker run -it -v G:\vm-shared:/shared --privileged=true dockerproxy.cn/svkv/riscv-tools:v1.0 /bin/bash
```

启动后克隆xv6项目到本地，并编译、运行：

```sh
$ cd /shared/
$ git clone https://github.com/HUST-OS/xv6-k210.git
$ cd xv6-k210/
```

对Makefile作简单修改：
- QEMU选项：
	- 增大分配内存：`-m 32M`
	- 由于未知原因，Rust SBI一直不能正确启动，即使是替换后也不行，所以我改成了默认SBI：`-bios default`
- 其它：
	- 默认编译器是`riscv64-linux-gnu-`前缀的，而环境内编译器是`riscv64-unknown-elf-`前缀，所以需要改过来
	- 由于实验全程需要依赖QEMU，所以默认的K210平台不需要，因此直接修改`platform := qemu`

运行：

```sh
$ make run
```

发现依次出现了OpenSBI界面、xv6 logo、`hart 0 init done`、`init: starting sh`等字样，最后是终端指示符`-> / $`，但输出后输入无响应。

经过一系列检查，发现是该版本xv6未采用UART导致的，所以需要在`consoleinit`中重新引入UART逻辑：

```c
// the UART control registers are memory-mapped
// at address UART0. this macro returns the
// address of one of the registers.
#define Reg(reg) ((volatile unsigned char *)(UART + reg))

// the UART control registers.
// some have different meanings for
// read vs write.
// see http://byterunner.com/16550.html
#define RHR 0  // receive holding register (for input bytes)
#define THR 0  // transmit holding register (for output bytes)
#define IER 1  // interrupt enable register
#define IER_TX_ENABLE (1 << 0)
#define IER_RX_ENABLE (1 << 1)
#define FCR 2  // FIFO control register
#define FCR_FIFO_ENABLE (1 << 0)
#define FCR_FIFO_CLEAR (3 << 1)  // clear the content of the two FIFOs
#define ISR 2                    // interrupt status register
#define LCR 3                    // line control register
#define LCR_EIGHT_BITS (3 << 0)
#define LCR_BAUD_LATCH (1 << 7)  // special mode to set baud rate
#define LSR 5                    // line status register
#define LSR_RX_READY (1 << 0)    // input is waiting to be read from RHR
#define LSR_TX_IDLE (1 << 5)     // THR can accept another character to send

#define ReadReg(reg) (*(Reg(reg)))
#define WriteReg(reg, v) (*(Reg(reg)) = (v))

void consoleinit(void) {
  initlock(&cons.lock, "cons");

  // 写入UART控制存储器
  WriteReg(IER, 0x00);
  WriteReg(LCR, LCR_BAUD_LATCH);
  WriteReg(0, 0x03);
  WriteReg(1, 0x00);
  WriteReg(LCR, LCR_EIGHT_BITS);
  WriteReg(FCR, FCR_FIFO_ENABLE | FCR_FIFO_CLEAR);
  WriteReg(IER, IER_TX_ENABLE | IER_RX_ENABLE);
  
  cons.e = cons.w = cons.r = 0;

  devsw[CONSOLE].read = consoleread;
  devsw[CONSOLE].write = consolewrite;
}
```

引入后重新编译、运行内核，即可恢复正常的终端操作。

## 240927-生成和移植测试用例

大赛的测试用例在GitHub上，需要克隆到本地：

```sh
$ git clone https://github.com/oscomp/testsuits-for-oskernel.git
$ cd testsuits-for-oskernel/riscv-syscalls-testing/user/
```

然后编译出测试用例，并将其复制到xv6目录下：

```sh
$ make
$ cp -r build /shared/xv6-k210/testcases
```

修改Makefile，使得生成的xv6镜像包含这些测试用例，以便在xv6终端内调用：

```sh
fs: $(UPROGS)
	@if [ ! -f "fs.img" ]; then \
		echo "making fs image..."; \
		dd if=/dev/zero of=fs.img bs=512k count=512; \
		mkfs.vfat -F 32 fs.img; fi
	@mount fs.img $(dst)
	@if [ ! -d "$(dst)/bin" ]; then mkdir $(dst)/bin; fi
	@cp README $(dst)/README
# for oscomp tests
	@cp -r testcases $(dst)/testcases
	@for file in $$( ls $U/_* ); do \
		cp $$file $(dst)/$${file#$U/_};\
		cp $$file $(dst)/bin/$${file#$U/_}; done
	@umount $(dst)
```

重新生成镜像并启动xv6，即可访问到测试用例：

```sh
# in terminal
$ cd /shared/xv6-k210
$ make fs
$ make run

# in QEMU
$ cd testcases
```

## 240928-系统调用表修改

大赛赛题要求实现一系列系统调用，基本上是Linux 5.x系统调用的一个子集。但这些系统调用的调用号与xv6系统调用有冲突。

首先需要确定xv6和赛题的系统调用各自占有哪个调用号，其次要将修改应用到现有的xv6源码中。

### 确定系统调用号

优先级：高优先级的系统调用优先拥有调用号
- xv6的`exec`、`exit`系统调用：这两个调用号硬编码到`initcode`中，一旦修改会非常麻烦
- 赛题的系统调用
- xv6的其它调用

冲突规则：
- 同名同号冲突：合并
- 同名不同号冲突：xv6调用持有原名，赛题调用改名
- 同号不同名冲突：优先级高的占有调用号，优先级低的使用第一个空闲编号

| NO  | 赛题SC           | 赛题NO | xv6 SC      | xv6 NO | 备注               |
| --- | -------------- | ---- | ----------- | ------ | ---------------- |
| 1   |                |      | `fork`      | 1      |                  |
| 2   |                |      | `exit`      | 2      |                  |
| 3   |                |      | `wait`      | 3      |                  |
| 4   |                |      | `pipe`      | 4      |                  |
| 5   |                |      | `read`      | 5      |                  |
| 6   |                |      | `kill`      | 6      |                  |
| 7   |                |      | `exec`      | 7      |                  |
| 8   |                |      | `fstat`     | 8      |                  |
| 9   |                |      | `chdir`     | 9      |                  |
| 10  |                |      | `dup`       | 10     |                  |
| 11  |                |      | `getpid`    | 11     |                  |
| 12  |                |      | `sbrk`      | 12     |                  |
| 13  |                |      | `sleep`     | 13     |                  |
| 14  |                |      | `uptime`    | 14     |                  |
| 15  |                |      | `open`      | 15     |                  |
| 16  |                |      | `write`     | 16     |                  |
| 17  | `getcwd`       | 17   |             |        | 重命名为`getcwd2`    |
| 18  |                |      | `trace`     | 18     |                  |
| 19  |                |      | `sysinfo`   | 19     |                  |
| 20  |                |      | `mkdir`     | 20     |                  |
| 21  |                |      | `close`     | 21     |                  |
| 22  |                |      | `test_proc` | 22     |                  |
| 23  | `dup`          | 23   |             |        | 重命名为`dup2`       |
| 24  | `dup3`         | 24   |             |        |                  |
| 25  |                |      | `getcwd`    | 25     |                  |
| 26  |                |      | `rename`    | 26     |                  |
| 27  |                |      | `mknod`     | 27     | 非原生xv6系统调用，后续添加  |
| 28  |                |      | `remove`    | 17     | 与赛题的`getcwd`调用冲突 |
| 29  |                |      | `dev`       | 23     | 与赛题的`dup`调用冲突    |
| 30  |                |      | `readdir`   | 24     | 与赛题的`dup3`调用冲突   |
| 31  |                |      |             |        | 未使用              |
| 32  |                |      |             |        | 未使用              |
| 33  |                |      |             |        | 未使用              |
| 34  | `mkdirat`      | 34   |             |        |                  |
| 35  | `unlinkat`     | 35   |             |        |                  |
| 36  |                |      |             |        | 未使用              |
| 37  | `linkat`       | 37   |             |        |                  |
| 38  |                |      |             |        | 未使用              |
| 39  | `umount2`      | 39   |             |        |                  |
| 40  | `mount`        | 40   |             |        |                  |
| 49  | `chdir`        | 49   |             |        | 重命名为`chdir2`     |
| 56  | `openat`       | 56   |             |        |                  |
| 57  | `close`        | 57   |             |        | 重命名为`close2`     |
| 59  | `pipe2`        | 59   |             |        |                  |
| 61  | `getdents64`   | 61   |             |        |                  |
| 63  | `read`         | 63   |             |        | 重命名为`read2`      |
| 64  | `write`        | 64   |             |        | 重命名为`write2`     |
| 80  | `fstat`        | 80   |             |        | 重命名为`fstat2`     |
| 93  | `exit`         | 93   |             |        | 重命名为`exit2`      |
| 101 | `nanosleep`    | 101  |             |        |                  |
| 124 | `sched_yield`  | 124  |             |        |                  |
| 153 | `times`        | 153  |             |        |                  |
| 160 | `uname`        | 160  |             |        |                  |
| 169 | `gettimeofday` | 169  |             |        |                  |
| 172 | `getpid`       | 172  |             |        |                  |
| 173 | `getppid`      | 173  |             |        |                  |
| 214 | `brk`          | 214  |             |        |                  |
| 215 | `munmap`       | 215  |             |        |                  |
| 220 | `clone`        | 220  |             |        |                  |
| 221 | `execve`       | 221  |             |        |                  |
| 222 | `mmap`         | 222  |             |        |                  |
| 260 | `wait4`        | 260  |             |        |                  |

### 修改xv6源码以添加系统调用

修改分以下数步：
- 修改`kernel/include/sysnum.h`中`SYS_***`的定义
- 在`kernel/syscall.c`中增加系统调用函数`sys_***`的外部定义，并对应修改`syscalls`和`sysnames`数组
- 在其它源文件中新增`sys_***`的实现

修改具体内容略。

## milestones

| 系统调用           | 调用号 | 难度  | 进度  | 完成时间   |
| -------------- | --- | --- | --- | ------ |
| `exit`         |     | D   |     |        |
| `getpid`       |     | D   | ✔   | 240928 |
| `getppid`      |     | D   | ✔   | 240928 |
| `gettimeofday` |     | D   | ❓   | 241011 |
| `uname`        |     | D   |     |        |
| `times`        |     | D   |     |        |
| `brk`          |     | D   |     |        |
| `clone`        |     | C   |     |        |
| `fork`         |     | C   |     |        |
| `wait`         |     | C   |     |        |
| `waitpid`      |     | C   |     |        |
| `mmap`         |     | C   |     |        |
| `munmap`       |     | C   |     |        |
| `execve`       |     | C   |     |        |
| `close`        |     | B   |     |        |
| `dup`          |     | B   |     |        |
| `dup2`         |     | B   |     |        |
| `pipe`         |     | B   |     |        |
| `read`         |     | B   |     |        |
| `write`        |     | B   |     |        |
| `openat`       |     | A   |     |        |
| `open`         |     | A   |     |        |
| `fstat`        |     | A   |     |        |
| `getdents`     |     | A   |     |        |
| `chdir`        |     | A   |     |        |
| `getcwd`       |     | A   |     |        |

## 240928-getpid/getppid

`getpid`和`getppid`是相对最易于实现的系统调用，只需要访问当前进程结构`myproc()`的`parent`和`pid`字段即可。

实现：

```c
uint64 sys_getppid(void) {
  return myproc()->parent->pid;
}

uint64 sys_getpid2(void) {
  return myproc()->pid;
}
```

经过试验，它能够通过测试用例，并符合操作系统逻辑。

## 241011-gettimeofday

十一假期期间在阅读导师布置的材料，耽搁了一些进度。

`gettimeofday`调用要求返回系统时钟的秒数和毫秒数。按照规范，返回的应当为Unix时间戳，但由于赛题给出的编译指令没有打开QEMU实时时钟，所以采用返回CPU时钟计数器的方式。

```c
uint64 sys_gettimeofday(void) {
  uint64 p_ts, tsc;
  int tz;

  if (argaddr(0, &p_ts) < 0 || argint(1, &tz)) return -1;

  tsc = r_time();
  *(uint64*)(p_ts + 0) = tsc / 12500000ull;
  *(uint64*)(p_ts + 8) = (tsc % 12500000ull) * 80ull / 1000ull;

  return 0;
}
```

目前测试程序报告通过，但返回时间是否合理有待进一步检验。