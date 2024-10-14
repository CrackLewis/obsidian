
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

| 系统调用                                   | 难度  | 进度  | 完成时间   |
| -------------------------------------- | --- | --- | ------ |
| `exit`                                 | D   |     |        |
| `getpid`                               | D   | ✔   | 240928 |
| `getppid`                              | D   | ✔   | 240928 |
| [[#241011-gettimeofday\|gettimeofday]] | D   | ❓   | 241011 |
| [[#241012-uname\|uname]]               | D   | ✔   | 241012 |
| [[#241012-times\|times]]               | D   | ❓   | 241012 |
| [[#241012-brk\|brk]]                   | D   | ✔   | 241012 |
| `clone`                                | C   |     |        |
| `fork`                                 | C   |     |        |
| `wait`                                 | C   |     |        |
| `waitpid`                              | C   |     |        |
| `mmap`                                 | C   |     |        |
| `munmap`                               | C   |     |        |
| `execve`                               | C   |     |        |
| `close`                                | B   |     |        |
| `dup`                                  | B   |     |        |
| `dup2`                                 | B   |     |        |
| `pipe`                                 | B   |     |        |
| `read`                                 | B   |     |        |
| `write`                                | B   |     |        |
| `openat`                               | A   |     |        |
| `open`                                 | A   |     |        |
| `fstat`                                | A   |     |        |
| `getdents`                             | A   |     |        |
| `chdir`                                | A   |     |        |
| `getcwd`                               | A   |     |        |

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

## 241012-uname

`uname`用于返回操作系统的信息。

为了实现尽量简单，输出采用硬编码方式。

```c
const static char* __sysname = "xv6-qemu";
const static char* __nodename = "CrackLewis";
const static char* __release = "Alpha";
const static char* __version = "0.1.0";
const static char* __machine = "qemu-system-riscv64";
const static char* __domainname = "local";

uint64 sys_uname(void) {
  uint64 uts_addr;
  struct utsname {
    char sysname[65];
    char nodename[65];
    char release[65];
    char version[65];
    char machine[65];
    char domainname[65];
  }* p_uts;

  if (argaddr(0, &uts_addr) < 0) return -1;
  p_uts = (struct utsname*)uts_addr;

  safestrcpy(p_uts->sysname, __sysname, strlen(__sysname) + 1);
  safestrcpy(p_uts->nodename, __nodename, strlen(__nodename) + 1);
  safestrcpy(p_uts->release, __release, strlen(__release) + 1);
  safestrcpy(p_uts->version, __version, strlen(__version) + 1);
  safestrcpy(p_uts->machine, __machine, strlen(__machine) + 1);
  safestrcpy(p_uts->domainname, __domainname, strlen(__domainname) + 1);

  return 0;
}
```

## 241012-times

`times`要求返回当前进程在用户态和内核态各执行了多少刻，以及它的子进程执行了多少刻，返回值写入到用户程序提供的结构体地址中。

由于xv6的进程控制结构`proc`还没有记录运行时间的字段，所以考虑添加以下6个字段：

```c
struct proc {
  // 其他成员
  
  // times-related: defs
  uint64 usince;               // user time since
  uint64 ssince;               // system time since
  uint64 utime;                // user time
  uint64 stime;                // system time
  uint64 cutime;               // children user time
  uint64 cstime;               // children system time
};
```

`usince`和`ssince`字段分别记录进程最近一次进入用户态和内核态的时刻，如果进程当前不在对应状态则置为0。

`utime`和`stime`字段记录当前进程在用户态和内核态的执行刻数。

`cutime`和`cstime`字段记录当前进程所有已结束子进程在用户态和内核态的总执行刻数。

进程生命周期内，有如下情形会造成进程状态转换：
- 进程被某个CPU的`scheduler`选中，由就绪态转为运行态
- 进程放弃CPU，由运行态转为阻塞/就绪态
- 进程触发中断，进入内核态
- 进程离开中断，进入用户态

对内核作如下修改：

第一处，在`kernel/proc.c:allocproc`中增加对6个字段的初始化逻辑：

```c
static struct proc *allocproc(void) {
  // ...

found:
  p->pid = allocpid();

  // times-related
  p->utime = p->stime = p->cutime = p->cstime = 0;
  p->usince = p->ssince = 0;

  // goes on
}
```

第二处，在`kernel/proc.c:sched`中增加进程让出CPU的逻辑：将已运行的时间记录在`utime`、`stime`中，并将`usince`和`ssince`清零。

```c
void sched(void) {
  // ...

  intena = mycpu()->intena;
  // times-related: process p stops running in system mode
  if (p->ssince) p->stime += r_time() - p->ssince;
  if (p->usince) p->utime += r_time() - p->usince;
  p->ssince = p->usince = 0;

  swtch(&p->context, &mycpu()->context);
  mycpu()->intena = intena;
}
```

第三处，在`kernel/proc.c:scheduler`中增加进程获得CPU的逻辑：当前时刻记录在`usince`中，开始运行于用户态。

```c
void scheduler(void) {
  // ...
  for (;;) {
    // ...
    for (p = proc; p < &proc[NPROC]; p++) {
      acquire(&p->lock);
      if (p->state == RUNNABLE) {
        // switch to chosen process
        p->state = RUNNING;
        c->proc = p;

        // times-related: process p starts running in user mode
        p->usince = r_time();

        // process p starts then and returns here
        // ...
      }
      release(&p->lock);
    }
    // ...
  }
}
```

第四处，在`kernel/trap.c:usertrap`中增加进程切换到内核态中的逻辑：当前时刻与`usince`的差值增加到`utime`中，`ssince`设置为当前时刻。

```c
void usertrap(void) {
  // ...
  struct proc *p = myproc();

  // times-related: process p stops running in user mode and
  // starts running in system mode
  if (p->usince) p->utime += r_time() - p->usince;
  p->usince = 0;
  p->ssince = r_time();

  // save user program counter.
  p->trapframe->epc = r_sepc();
  // goes on...
}
```

第五处，在`kernel/trap.c:usertrapret`中增加进程切换回用户态的逻辑：当前时刻与`ssince`的差值增加到`stime`中，`usince`设置为当前时刻。

```c
void usertrapret(void) {
  struct proc *p = myproc();

  // ...
  p->trapframe->kernel_hartid = r_tp();  // hartid for cpuid()

  // times-related: process p stops running in system mode and starts running in
  // user mode
  if (p->ssince) p->stime += r_time() - p->ssince;
  p->ssince = 0;
  p->usince = r_time();

  // goes on...
}
```

第六处，在`kernel/proc.c:wait`中增加子进程退出的逻辑，其父进程将记录子进程的运行时间到`cutime`和`cstime`。

```c
int wait(uint64 addr) {
  struct proc *np;
  int havekids, pid;
  struct proc *p = myproc();
  // ...

  for (;;) {
    // ...
    for (np = proc; np < &proc[NPROC]; np++) {
      if (np->parent == p) {
        // ...
        if (np->state == ZOMBIE) {
          // found one!
          
          // times-related: update cutime and cstime
          p->cutime += np->utime + np->cutime;
          p->cstime += np->stime + np->cstime;

          // ...
        }
        // ...
      }
    }
    // ...
  }
}
```

最后实现系统调用。它访问当前进程的`utime`、`stime`、`cutime`和`cstime`4个成员：

```c
uint64 sys_times(void) {
  uint64 addr_tms;
  struct tms {
    long tms_utime;
    long tms_stime;
    long tms_cutime;
    long tms_cstime;
  } *p_tms;

  if (argaddr(0, &addr_tms) < 0) return -1;

  p_tms = (struct tms*)addr_tms;
  p_tms->tms_utime = myproc()->utime;
  p_tms->tms_stime = myproc()->stime;
  p_tms->tms_cutime = myproc()->cutime;
  p_tms->tms_cstime = myproc()->cstime;

  return 0;
}
```

该实现能够通过官方测试用例。然而，该实现是基于内核行为对程序时间进行的粗略估计，是否能够真实无误地反映程序用时有待进一步考察。

## 241012-brk

`brk`系统调用可以查询进程内存地址空间的末端，或将内存空间长度进行变更。

在Linux下`brk`只返回0或-1，表示执行是否成功。但官方测试用例要求在执行成功时，返回新的程序末端地址。

实现思路：借助`growproc`方法实现。

```c
uint64 sys_brk(void) {
  int new_end, old_end, n;

  if (argint(0, &new_end) < 0) return -1;
  old_end = myproc()->sz;
  if (new_end == 0) {
    return old_end;
  }

  n = new_end - old_end;
  return growproc(n) == 0 ? new_end : old_end;
}
```

## 241012-首次提交评测

首次提交，喜提零鸭蛋。

读文档发现评测不是交互程序，而是内核启动后需要自己跑完所有用例，遂修改`init.c`。

然后修改`init.c`之后发现仍然没用。。。后来仔细阅读文档才发现评测平台采用的是自己的镜像，不会重新制作镜像，因此任何自行修改或增加的用户程序都不能跑在上面，所以需要照着文档的方法自己将`init.c`的可执行程序dump成16进制码，替换掉原本的`initcode`。

生成16进制码的指令如下：

```
xxd -p -c 1 _init | tr -d '\n' | sed 's/\(..\)/0x\1,/g' >init.hex
```

但是整个可执行文件有24KB左右，远超出了`init`进程内存不超过4KB的要求。于是考虑通过objdump指令寻求有用的部分：

```
riscv64-unknown-elf-objdump -s -d _init >init.out
```

发现只有`.text`、`.rodata`和`.data`三个段有用，而这三个段大约2500字节，低于4KB。于是手工截取了`init.hex`文件中的对应部分，替换掉了原来的`initcode`数组。

pts: 19/100

## 241013-fork

fork用例要求实现`clone`系统调用。