
240715：大名鼎鼎的GNU Debugger，今天才学，惭愧。

参考：
- [blog1](https://blog.csdn.net/lovely_dzh/article/details/109160337)
- [blog2](https://blog.csdn.net/weixin_45031801/article/details/134399664)

## 基本指令

| 指令简写/指令名       | 指令格式                    | 功能                   |
| -------------- | ----------------------- | -------------------- |
| `l/list`       | `list [<line>\|<func>]` | 显示函数、行号或当前位置附近的源码    |
| `r/run`        | `run`                   | 继续执行                 |
| `b/breakpoint` | `breakpoint <pos>`      | 在指定位置打断点             |
| `info`         | `info b`                | 查看断点信息               |
| `d/delete`     | `delete <bp_id>`        | 删除指定编号的断点            |
|                | `delete breakpoints`    | 删除所有断点               |
| `disable`      | `disable b(reakpoints)` | 禁用所有断点               |
| `enable`       | `enable b(reakpoints)`  | 启用所有断点               |
| `n/next`       | `next`                  | 逐过程执行                |
| `s/step`       | `step`                  | 逐语句执行                |
| `bt`           | `bt`                    | 看到底层函数调用的过程          |
| `set`          | `set <var> <value>`     | 修改变量的值               |
| `p/print`      | `print <var>`           | 输出变量的值               |
| `display`      | `display <var>`         | 跟踪查看一个变量，每次暂停时都输出它的值 |
| `undisplay`    | `undisplay <var>`       | 取消跟踪变量               |
| `until`        | `until <line>`          | 执行到指定的行              |
| `finish`       | `finish`                | 执行到当前函数返回，然后暂停       |
| `c/continue`   | `continue`              | 继续执行，直到下一个断点或结束      |

## 断点相关指令

