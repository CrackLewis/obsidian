
通过协程实现*单线程并发*

关键概念：
- 事件循环：异步与同步相对，不要求所有子过程在被调用后立刻生成结果，除非它们被等待，常用于执行I/O密集型任务。事件循环负责调度和执行协程，当协程遇到I/O操作时，它会挂起当前协程，让事件循环去执行其他就绪的协程
- 协程：轻量级线程，调度完全在用户态完成。通过`async`关键字定义，通过`await`关键字挂起并等待其他协程执行完毕
- 任务：协程的高级封装，包含各种任务状态。由`asyncio.create_task()`创建，也可以被`await`等待

## 协程的创建/等待

- 异步函数被调用时，即产生一个协程
- 裸协程只有在被`await`时才会确保产生结论（由事件循环驱动）：完成，返回一个结果；失败，抛出一个异常
- `await`会挂起当前协程，等待被`await`的对象完成
	- 只有异步函数可以`await`，普通函数不可以
	- 普通函数执行异步函数，需要借助`asyncio.run(...)`来执行

```python
import asyncio

# sub：子协程
async def sub(sleep_secs: int):
    print(f"sub: sleeping for {sleep_secs} seconds")
    await asyncio.sleep(sleep_secs)
    print("sub: done sleeping")

# main：主协程
async def main():
    print("main: starting")
    coro = sub(2)
    await asyncio.sleep(1)
    print("main: waiting for sub to finish")
    await coro
    print("main: done")

asyncio.run(main())

"""输出：
main: starting
main: waiting for sub to finish
sub: sleeping for 2 seconds
sub: done sleeping
main: done
"""
```

## asyncio.Task

任务是一种*主动的*、*并发的*高级协程：
- 主动执行：普通协程惰性执行，但任务会主动在事件循环内调度执行
- 并发：多个任务会并发执行，但多个协程是串行的
- 生命周期管理：
	- 普通协程如果不被`await`，有可能会被垃圾回收
	- 任务的生命周期独立，可以被取消、查询状态、添加回调
- 结果获取：`task.result()`、`await task`、`task.exception()`可以获取任务执行的结果
- 异常处理：任务内部可捕获异常，或者在`await task`时抛出；未处理则会触发`loop.call_exception_handler`

`asyncio.Task`的有关方法：
- `asyncio.create_task(coro, *, name=)`：基于协程创建一个任务
- 获取结果：
	- `done()`：返回是否完成
	- `result()`：返回任务的执行结果，即协程的返回函数
	- `exception()`：返回任务抛出的异常

### demo：普通协程vs任务

普通协程惰性执行，顺序调度，耗时约为2+3=5秒；任务会被调度且并发执行，耗时约为3秒

```python
import asyncio 

async def my_task(task_id: int, sleep_secs: int):
    print(f"Task {task_id}: sleeping for {sleep_secs} seconds")
    await asyncio.sleep(sleep_secs)
    print(f"Task {task_id}: done sleeping")

async def main():
    # 纯协程调用
    time_start = asyncio.get_running_loop().time()
    await my_task(1, 2)
    await my_task(2, 3)
    time_end = asyncio.get_running_loop().time()
    print(f"Total time taken (coroutines): {time_end - time_start:.2f} seconds")
    
    # 任务调用
    time_start = asyncio.get_event_loop().time()
    task1 = asyncio.create_task(my_task(3, 2))
    task2 = asyncio.create_task(my_task(4, 3))
    await task1
    await task2
    time_end = asyncio.get_event_loop().time()
    print(f"Total time taken (tasks): {time_end - time_start:.2f} seconds")
    
if __name__ == "__main__":
    asyncio.run(main())
```

### 获取任务结果

获取任务的具体结果有3种方式：

| 等待方式               | 任务未完成                 | 任务成功     | 任务失败/被取消 |
| ------------------ | --------------------- | -------- | -------- |
| `await task`       | 挂起直至任务完成，并返回其结果       | 返回任务的结果  | 抛出对应异常   |
| `task.result()`    | 抛出`InvalidStateError` | 返回任务的结果  | 抛出对应异常   |
| `task.exception()` | 抛出`InvalidStateError` | 返回`None` | 返回异常实例   |

还有一些方法可以返回任务的状态：
- `task.done()`：任务是否完成（有了明确的结果：成功/失败/取消）
- `task.cancelled()`：任务是否被取消

### 任务的取消

当一个任务由于某些原因（超时、前驱任务失败等）不宜继续执行时，其可以被`task.cancel()`取消。取消的任务会被移出事件循环，在被`await`或调用`result()`时会抛出`CancelledError`。

`task.cancelled()`可查询一个任务是否被取消

```python
import asyncio

async def rather_long_task(task_id: int, sleep_secs: int):
    print(f"Task {task_id}: sleeping for {sleep_secs} seconds")
    await asyncio.sleep(sleep_secs)
    print(f"Task {task_id}: done sleeping")

async def main():
    task = asyncio.create_task(rather_long_task(1, 500))
    await asyncio.sleep(2)
    if not task.done():
        print("Main: task is taking too long, cancelling it")
        task.cancel()
    # 对一个可能被取消的任务await，必须加try-catch块特殊处理，或者
    # 手动判断task.cancelled()
    try:
        await task
    except asyncio.CancelledError:
        print("Main: task was cancelled")

if __name__ == "__main__":
    asyncio.run(main())
```

## asyncio.wait_for

`asyncio.wait_for(awaitable, *, timeout=)`用于在指定时限内等待一个awaitable。如果时限内awaitable结束，则返回其结果/抛出其异常，否则抛出一个`asyncio.TimeoutError`。

