
此为内置库，不需要安装。

```python
import multiprocessing
```

## Process

开启另一个进程，该进程执行`target`指定的Python函数，参数由`args`指定。

```python
def straight(st, en):
	for i in range(st, en):
		print(f"Straight: {i}")

# 声明进程
proc = multiprocessing.Process(target=routine, args=(3, 8))
proc.start() # 启动进程，分配pid和其他系统资源
proc.join() # 等待进程结束

print(f"Process #{proc.pid} exited with return code {proc.exitcode}")

# 发送SIGKILL信号给进程
# proc.kill()
# 发送SIGTERM信号给进程
# proc.terminate()
```

## Semaphore

semaphore（信号量）是一种进程/线程间互斥机制。

`acquire(block=True)`会尝试对信号量执行获取操作：
- 信号量为0且：
	- `block`为真时，进程会等待直至信号量恢复为1，随后执行减1，返回True
	- `block`为假：直接返回False
- 信号量为1：减1，返回True

`release()`会执行释放操作，信号量加1

```python
import multiprocessing
import time
from datetime import datetime

def routine(st, label, sem):
    print(f"{datetime.now() - st}: {label} A")
    time.sleep(5)
    print(f"{datetime.now() - st}: {label} B")
    sem.acquire() # 信号量为0则等待，大于0则减1
    print(f"{datetime.now() - st}: {label} C")
    time.sleep(1)
    print(f"{datetime.now() - st}: {label} D")
    sem.release() # 信号量加1
    print(f"{datetime.now() - st}: {label} E")
    time.sleep(5)
    print(f"{datetime.now() - st}: {label} F")

sem = multiprocessing.Semaphore(1)
proc_count = 4
procs = [multiprocessing.Process(target=routine, args=[datetime.now(), idx, sem]) for idx in range(proc_count)]
for proc in procs:
    proc.start()

for proc in procs:
    proc.join()

```