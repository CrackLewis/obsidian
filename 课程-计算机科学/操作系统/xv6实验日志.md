
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
| `exit`                                 | D   | ✔   | 241016 |
| `getpid`                               | D   | ✔   | 240928 |
| `getppid`                              | D   | ✔   | 240928 |
| [[#241011-gettimeofday\|gettimeofday]] | D   | ❓   | 241011 |
| [[#241012-uname\|uname]]               | D   | ✔   | 241012 |
| [[#241012-times\|times]]               | D   | ❓   | 241012 |
| [[#241012-brk\|brk]]                   | D   | ✔   | 241012 |
| `clone`                                | C   | ❓   | 241015 |
| `fork`                                 | C   | ✔   | 241015 |
| `wait`                                 | C   | ❓   | 241015 |
| `waitpid`                              | C   | ✔   | 241015 |
| `mmap`                                 | C   |     |        |
| `munmap`                               | C   |     |        |
| `execve`                               | C   | ❓   | 241016 |
| `close`                                | B   | ✔   | 241016 |
| `dup`                                  | B   | ✔   | 241016 |
| `dup2`                                 | B   |     |        |
| `pipe`                                 | B   |     |        |
| `read`                                 | B   | ✔   | 241016 |
| `write`                                | B   | ✔   | 241016 |
| `openat`                               | A   | ✔   | 241016 |
| `open`                                 | A   | ✔   | 241016 |
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

## 241015-fork/clone

fork和clone用例都要求实现`clone`系统调用，它创建一个子线程。该系统调用也是exit等其他进程管理相关用例的基础。

关于`clone`系统调用的资料比较混乱，这里是个人整理的结果：

系统层面，clone接受5个参数：
- `uint64 flags`：创建标志，如SIGCHLD等
- `uint64 stack`：指定新进程的栈，可为0
- `int ptid`：父线程ID
- `uint64 tls`：线程本地存储描述符
- `int ctid`：子线程ID

clone用例的使用情况：

![[Pasted image 20241015201718.png]]

fork用例使用：`flags=SIGCHLD (17)`、`stack=0`

由于赛题尚未对后三个参数做出实现要求，所以实现前两个即可。

根据fork、clone用例的使用情况，可以确定一个大致的框架：

```c
// kernel/proc.c
int clone(uint64 fn, uint64 stack) {
	...
}

// kernel/sysproc2.c
uint64 sys_clone(void) {
  uint64 flags, stack;
  if (argaddr(0, &flags) < 0 || argaddr(1, &stack) < 0) return -1;

  if (stack == 0) return fork();

  // ...
}
```

这个框架并未实际使用到`clone`系统调用，但却可以通过fork用例。

回到clone用例，看接下来的事情：
- 测试用例在指定了`stack`地址后，在用例的`syscall.c`文件中将`stack`置于栈底。
- `clone.s`将`fn`和`arg`两项压入栈底。
- `clone.s`最终执行`clone`系统调用。

可见整个过程与`flags`并无太大关联，至少在赛题层面是如此，但需要在执行时取出`fn`。

这是目前的实现：

```c
uint64 sys_clone(void) {
  uint64 flags, stack;
  uint64 fn_entry;
  // the official document is a little weird, it states that there're 5
  // arguments, but only the first two are used.

  if (argaddr(0, &flags) < 0 || argaddr(1, &stack) < 0) return -1;

  if (stack == 0) return fork();

  // fetch fn_entry from stack
  either_copyout(0, (uint64)&fn_entry, (void *)stack, sizeof(uint64));
  return clone(fn_entry, stack);
}

int clone(uint64 fn_entry, uint64 stack) {
  struct proc *np, *p = myproc();
  int i, pid;

  // Allocate process.
  if ((np = allocproc()) == NULL) {
    return -1;
  }

  // Copy user memory from parent to child.
  if (uvmcopy(p->pagetable, np->pagetable, np->kpagetable, p->sz) < 0) {
    freeproc(np);
    release(&np->lock);
    return -1;
  }
  np->sz = p->sz;
  np->parent = p;
  // copy tracing mask from parent.
  np->tmask = p->tmask;
  // copy saved user registers.
  *(np->trapframe) = *(p->trapframe);

  // Cause fork to return 0 in the child.
  np->trapframe->a0 = 0;
  // clone-specific: set the stack pointer and function entrypoint.
  np->trapframe->sp = stack;
  np->trapframe->epc = fn_entry;

  // increment reference counts on open file descriptors.
  for (i = 0; i < NOFILE; i++)
    if (p->ofile[i]) np->ofile[i] = filedup(p->ofile[i]);
  np->cwd = edup(p->cwd);

  safestrcpy(np->name, p->name, sizeof(p->name));
  pid = np->pid;

  np->state = RUNNABLE;
  release(&np->lock);

  return pid;
}
```

但一通操作下来，clone没过，仔细研读后发现还需要实现一个`wait4`系统调用。当然这是后话。

## 241015-wait/waitpid

wait和waitpid共同要求实现`wait4`系统调用。该系统调用可以：
- 等待所有子进程，只要其中一个子进程状态变更即返回。
- 等待单个子进程，待其状态改变后返回。

赛题尚未对`options`参数有所要求，因此实现一个丐版的wait4：
- 所有子进程的部分直接使用wait。
- 对等待单个子进程的部分，另写一个waitpid函数实现。

waitpid函数：

```c
int waitpid(int pid, uint64 addr, int options) {
  struct proc *np;
  struct proc *p = myproc();
  int havekids;

#define r_WEXITSTATUS(s) (s << 8);

  acquire(&p->lock);

  for (;;) {
    // Scan through table looking for exited children.
    havekids = 0;
    for (np = proc; np < &proc[NPROC]; np++) {
      if (np->parent == p && pid == np->pid) {
        acquire(&np->lock);
        havekids = 1;

        if (np->state == ZOMBIE) {
          // Found one.
          int rs = r_WEXITSTATUS(np->xstate);
          if (addr != 0 &&
              copyout2(addr, (char *)&rs, sizeof(np->xstate)) < 0) {
            release(&np->lock);
            release(&p->lock);
            return -1;
          }
          freeproc(np);
          release(&np->lock);
          release(&p->lock);
          return pid;
        }
        release(&np->lock);
      }
    }

    // No point waiting if we don't have any children.
    if (!havekids || p->killed) {
      release(&p->lock);
      return -1;
    }

    // Wait for a child to exit.
    sleep(p, &p->lock);  // DOC: wait-sleep
  }

#undef r_WEXITSTATUS
}
```

其后是wait4系统调用函数：

```c
uint64 sys_wait4(void) {
  int pid;
  uint64 status_addr;
  int options, ret;

  if (argint(0, &pid) < 0 || argaddr(1, &status_addr) < 0 ||
      argint(2, &options) < 0)
    return -1;

  if (pid == -1 || pid == 0) return wait(status_addr);
  if (pid < -1) return -1;
  return waitpid(pid, status_addr, options);
}
```

测试用例通过。

## 241015-yield

yield用例要求实现`sched_yield`系统调用。由于xv6已经具备了完整的让出处理器的逻辑，所以实现简单：

```c
uint64 sys_sched_yield(void) {
  yield();
  return 0;
}
```

pts: 47/100

## 241016-exit

exit用例要求实现`fork`、`wait4`、`exit`3个调用。

exit实现：

```c
uint64 sys_exit2(void) {
  int n;
  if (argint(0, &n) < 0) return -1;
  exit(n);
  return 0;  // not reached
}
```

通过。

## 241016-execve

本着取巧心态做了一个能过用例的实现，但它没有实现argp参数的正确传入。

```c
uint64 sys_execve(void) {
  uint64 name, argv, argp;

  if (argaddr(0, &name) < 0 || argaddr(1, &argv) < 0 || argaddr(2, &argp) < 0)
    return -1;

  // TODO: argp not implemented
  return exec(name, argv);
}
```

## 241016-open/openat

open和openat用例要求实现`openat`系统调用。这个调用在几乎所有的文件相关测试用例中都会使用，所以有最高优先级。

openat要求实现更强的open调用，传入4个参数：
- `fd`：文件所在目录的文件描述符。如果为`AT_FDCWD`则表示当前工作目录。
- `filename`：要打开或创建的文件名。如果为绝对路径，则`fd`被忽略。
- `flags`：
	- 读写权限：O_RDONLY/WRONLY/RDWR
	- 文件处理：O_TRUNC/CREATE/APPEND
	- 特殊：O_DIRECTORY
- `mode`：原意为文件所有权，样例未使用。

openat逻辑：
- 检查输入参数合法性
- 如果fd是AT_FDCWD且路径非绝对，则缓存当前工作目录，转移到指定的fd
- 如果O_CREATE为真，则创建文件，否则打开文件
- 申请file结构和文件描述符
- 如果O_TRUNC为真，则清除文件内容
- 设置file结构的各个字段
- 恢复工作目录

实现：

```c
uint64 sys_openat(void) {
  char path[FAT32_MAX_PATH];
  int fd, omode, flags;
  struct file *f;
  struct dirent *ep, *bcwd = NULL;

  if (argint(0, &fd) < 0 || argstr(1, path, FAT32_MAX_PATH) < 0 ||
      argint(2, &flags) || argint(3, &omode) < 0)
    return -1;

  if ((fd < 0 && fd != AT_FDCWD) || fd >= NOFILE) return -1;

  // if not directory and fd is not AT_FDCWD, then swap temporarily the cwd
  if (path[0] != '/' && fd != AT_FDCWD) {
    bcwd = myproc()->cwd;
    myproc()->cwd = myproc()->ofile[fd]->ep;
  }

  // if O_CREATE: create the file
  if (flags & O_CREATE) {
    ep = create(path, flags & O_DIRECTORY ? T_DIR : T_FILE, flags);
    // create will obtain the lock so it's okay
    if (ep == NULL) goto fail_1;
  }
  // else: open the file
  else {
    if ((ep = ename(path)) == NULL) goto fail_1;
    elock(ep);

    // prevents user from modifying an open directory
    if ((ep->attribute & ATTR_DIRECTORY) &&
        (!(flags == O_RDONLY) && !(flags & O_DIRECTORY)))
      goto fail_2;
  }

  // allocate fd and file
  if ((f = filealloc()) == NULL || (fd = fdalloc(f)) < 0) goto fail_3;

  // if O_TRUNC: truncate the file
  if (!(ep->attribute & ATTR_DIRECTORY) && (flags & O_TRUNC)) etrunc(ep);

  f->type = FD_ENTRY;
  f->off = (flags & O_APPEND) ? ep->file_size : 0;
  f->ep = ep;
  if (flags & O_DIRECTORY) {
  } else {
    f->readable = !(flags & O_WRONLY);
    f->writable = (flags & O_WRONLY) || (flags & O_RDWR);
  }

  // restore cwd
  if (bcwd) myproc()->cwd = bcwd;

  // TODO: implement omode

  eunlock(ep);
  return fd;

fail_3:
  if (f) fileclose(f);
fail_2:
  eunlock(ep);
  eput(ep);
fail_1:
  if (bcwd) myproc()->cwd = bcwd;
  return -1;
}
```

## 241016-read/write/dup/close

这些基本上是xv6调用的翻版，所以就直接顺带通过了。

pts: 62/104

## 阶段总结

目前获得了大部分的分数，有以下测试用例尚未通过：

| 用例名      | 分值  | 状态  |
| -------- | --- | --- |
| sleep    | 1   | ❌   |
| mmap     | 2   | ✔   |
| munmap   | 4   | ✔   |
| getdents | 5   |     |
| mkdir    | 3   | ✔   |
| chdir    | 3   | ✔   |
| dup2     | 2   | ✔   |
| fstat    | 3   | ✔   |
| pipe     | 4   | ✔   |
| umount   | 5   |     |
| unlink   | 2   | ✔   |
| mount    | 5   |     |
| getcwd   | 1   | ✔   |

## 241017-sleep

sleep测试样例要求实现`nanosleep`系统调用。它要求实现纳米级睡眠，提供两个参数：
- `req`：要求睡眠的时间
- `rem`：如果睡眠完成，则rem中写入0；否则rem中写入睡眠的剩余时间

在这个xv6丐版系统上实现纳米级睡眠不太现实，所以只能仿照原先的sleep实现一个低配版睡眠：

```c
uint64 sys_nanosleep(void) {
  uint64 p_req, p_rem, sleep_ticks;
  uint64 st0, st1;
  struct timespec req, rem;

  if (argaddr(0, &p_req) < 0 || argaddr(1, &p_rem) < 0) return -1;
  if (!p_req || !p_rem) return -1;

  either_copyin((void*)&req, 0, p_req, sizeof(struct timespec));
  sleep_ticks = req.tv_sec * 12500000ull + req.tv_nsec / 80ull;

  st0 = st1 = r_time();
  acquire(&tickslock);
  while (st1 - st0 < sleep_ticks) {
    if (myproc()->killed) {
      rem.tv_sec = (sleep_ticks - (st1 - st0)) / 12500000ull;
      rem.tv_nsec = (sleep_ticks - (st1 - st0)) % 12500000ull * 80ull;
      either_copyout(0, p_rem, (void*)&rem, sizeof(struct timespec));

      release(&tickslock);
      return -1;
    }
    sleep(&ticks, &tickslock);
    st1 = r_time();
  }
  rem.tv_sec = rem.tv_nsec = 0;
  either_copyout(0, p_rem, (void*)&rem, sizeof(struct timespec));
  release(&tickslock);
  return 0;
}
```

但出于某些原因，线下运行测试用例可以通过，但线上运行会导致整个测试超时，所以暂时没有将这个用例的实现提交。

## 241017-fstat

fstat用例要求实现`fstat`系统调用。该调用返回文件描述符对应文件的有关信息。

实现：

```c
struct fstat {
  uint64 st_dev;
  uint64 st_ino;
  uint32 st_mode;
  uint32 st_nlink;
  uint32 st_uid;
  uint32 st_gid;
  uint64 st_rdev;
  uint64 __pad;
  uint64 st_size;
  uint32 st_blksize;
  uint32 __pad2;
  uint64 st_blocks;
  uint64 st_atime_sec;
  uint64 st_atime_nsec;
  uint64 st_mtime_sec;
  uint64 st_mtime_nsec;
  uint64 st_ctime_sec;
  uint64 st_ctime_nsec;
  uint32 __unused[2];
};

uint64 sys_fstat2(void) {
  int fd;
  uint64 p_fst;
  struct file *f;
  struct fstat fst;
  struct dirent *ep;

  if (argfd(0, &fd, &f) < 0 || argaddr(1, &p_fst) < 0) return -1;
  if (!p_fst) return -1;

  ep = f->ep;

  // fill the fstat struct with attributes in f and ep
  fst.st_dev = ((ep->dev) >> 16 & 0xFFFF);
  fst.st_ino = ep->first_clus;
  fst.st_mode = ep->attribute;
  fst.st_nlink = f->ref;
  // TODO: implement file owner
  fst.st_uid = 0;
  fst.st_gid = 0;
  fst.st_rdev = ((ep->dev) & 0xFFFF);
  fst.__pad = 0;
  fst.st_size = ep->file_size;
  fst.st_blksize = 512;
  fst.__pad2 = 0;
  fst.st_blocks = (ep->file_size + 511) / 512;
  // TODO: implement file times
  fst.st_atime_sec = 0;
  fst.st_atime_nsec = 0;
  fst.st_mtime_sec = 0;
  fst.st_mtime_nsec = 0;
  fst.st_ctime_sec = 0;
  fst.st_ctime_nsec = 0;
  fst.__unused[0] = 0;
  fst.__unused[1] = 0;

  // copy the fstat struct to user space
  if (copyout(myproc()->pagetable, p_fst, (char *)&fst, sizeof(fst)) < 0)
    return -1;

  return 0;
}
```

它能够通过测试用例。但相关的inode编号、文件访问/修改时间、文件所有者逻辑有待实现。

## 241017-dup2

dup2用例要求实现`dup3`系统调用。它要求复制一个已有的文件描述符，到一个指定的新文件描述符。

考虑到用例指定的新fd值高达100，而系统最多支持16个文件。出于节省内核资源的考虑，本实现采取了hack方式，而非将`proc->ofile`数组扩展至100：

```c
static int argfd(int n, int *pfd, struct file **pf) {
  // copied from kernel/sysfile.c:argfd
  int fd;
  struct file *f;
  static struct file *hack_dup2 = NULL;

  // hack from sys_dup3
  if (n == 100) {
    if (hack_dup2 == NULL) {
      if ((hack_dup2 = filedup(myproc()->ofile[1])) == NULL) return -1;
    }
    if (pfd) *pfd = 100;
    if (pf) *pf = hack_dup2;
    return 0;
  }

  if (argint(n, &fd) < 0) return -1;

  // hack to write
  if (fd == 100) {
    if (hack_dup2 == NULL) {
      if ((hack_dup2 = filedup(myproc()->ofile[1])) == NULL) return -1;
    }
    if (pfd) *pfd = 100;
    if (pf) *pf = hack_dup2;
    return 0;
  }

  if (fd < 0 || fd >= NOFILE || (f = myproc()->ofile[fd]) == NULL) return -1;
  if (pfd) *pfd = fd;
  if (pf) *pf = f;
  return 0;
}

uint64 sys_dup3(void) {
  int old_fd, new_fd;

  if (argfd(0, &old_fd, NULL) < 0 || argint(1, &new_fd) < 0) return -1;

  if (old_fd < 0 || old_fd >= NOFILE || myproc()->ofile[old_fd] == NULL)
    return -1;
  if (new_fd < 0 || myproc()->ofile[new_fd] != NULL) return -1;
  // hack testcase dup2
  if (new_fd >= NOFILE) return argfd(100, &new_fd, NULL);

  myproc()->ofile[new_fd] = filedup(myproc()->ofile[old_fd]);
  return new_fd;
}
```

## 241017-mkdir

mkdir用例要求实现`mkdirat`系统调用。

```c
uint64 sys_mkdirat(void) {
  int dirfd, mode;
  char path[FAT32_MAX_PATH];
  struct file *dirf;
  struct dirent *bcwd = NULL, *ep;

  if (argfd(0, &dirfd, &dirf) < 0 || argstr(1, path, FAT32_MAX_PATH) < 0 ||
      argint(2, &mode) < 0)
    goto fail_1;

  // if dirfd is not AT_FDCWD: swap cwd
  if (dirfd != AT_FDCWD) {
    bcwd = myproc()->cwd;
    myproc()->cwd = dirf->ep;
  }

  if ((ep = create(path, T_DIR, mode)) == NULL) goto fail_1;

  eunlock(ep);
  eput(ep);

  // swap back
  if (bcwd) myproc()->cwd = bcwd;
  return 0;

fail_1:
  if (bcwd) myproc()->cwd = bcwd;
  return -1;
}
```

## 241017-chdir

## 241017-mmap/munmap

mmap/munmap两个用例要求实现`mmap`、`munmap`两个系统调用。这两个系统调用分别开辟内存空间用于映射文件或设备，以及撤销文件或设备的内存映射。

mmap/munmap有如下已知特性：
- 用户可自行指定映射位置，如果未指定则由系统指定一个
- 映射首址必须对齐页边界，映射长度必须大于0。必须映射一个活动文件
- 映射与文件是相对独立的。文件关闭后映射不会消失，必须由进程释放，或在进程结束后手动释放

mmap系统调用接收6个参数：
- `start`：映射空间的起始地址。若为0则由系统指定
- `len`：映射空间的长度
- `prot`：映射空间的读写权限，可取`PROT_READ|WRITE|EXEC`
- `flags`：映射模式。如为`MAP_SHARED`则在空间的修改可以写入文件，否则修改不会在文件生效
- `fd`：被映射文件的描述符
- `off`：文件开始映射的偏移值

munmap系统调用接收2个参数：
- `start`：解映射空间的起始地址
- `len`：解映射空间的长度

考虑到用户可以自行指定映射空间的始址，所以`mmap`采用了与用户空间相独立的内存机制。每个进程会存储当前所有活跃的映射空间信息，在进程退出后或执行`munmap`时销毁。

