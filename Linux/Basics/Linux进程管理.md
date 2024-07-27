
## 常见概念

- 进程
- 进程ID
- 父子进程
- 进程状态：Running/Sleeping/Zombie/Terminated
- 前台和后台进程
- 进程优先级和调度
- 作业（Job）：一组与终端会话关联的相关进程
- 信号（Signal）：通知进程发生某个事件的机制
- 守护进程
- 进程组
- 会话：一或多个进程组
- cgroups：对进程组的资源管理策略
- 内核线程

## 进程管理命令

1. `ps`：用于列出当前系统中运行的进程的信息。
    - 常见选项：
        - `ps aux`：列出所有用户的所有进程。
        - `ps aux | grep processname`：查找特定进程名称。
        - `ps -e`：列出系统上所有进程。
2. `top`：以实时动态方式显示系统的运行进程和系统性能信息。
3. `htop`：类似于`top`，但提供更多的交互性和可视化信息。
4. `kill`：用于终止（杀死）正在运行的进程。
    - `kill PID`：根据进程ID（PID）终止一个进程。
    - `killall processname`：根据进程名称终止多个进程。
5. `pkill`：根据进程名称终止进程。
    - `pkill processname`：根据进程名称终止进程。
6. `killall`：终止具有相同名称的所有进程。
    - `killall processname`：终止具有相同名称的所有进程。
7. `systemctl`：用于管理系统服务（systemd管理的服务）。
    - `systemctl start servicename`：启动服务。
    - `systemctl stop servicename`：停止服务。
    - `systemctl restart servicename`：重新启动服务。
    - `systemctl status servicename`：查看服务状态。
    - `systemctl enable servicename`：在系统启动时启用服务。
    - `systemctl disable servicename`：在系统启动时禁用服务。
8. `service`：用于管理传统的init.d脚本启动的服务。
    - `service servicename start`：启动服务。
    - `service servicename stop`：停止服务。
    - `service servicename restart`：重新启动服务。
    - `service servicename status`：查看服务状态。

## ps：进程查看

实用：
- `ps aux`
- `ps -ef`
- `ps axjf`、`ps -ejH`：以进程树格式输出信息

![[Pasted image 20240727195039.png]]

参数说明：
- `USER`：创建该进程的用户
	- `UID`：用户ID
	- `GROUP`：用户进程组
- `PID`：进程ID
	- `PGID`：进程组ID
	- `PPID`：父进程ID
	- `TPGID`：前台进程组ID
	- `SESSION`：会话ID
- `%CPU`：CPU占用率
- `%MEM`：内存占用率
	- `VSZ`：进程使用的虚拟内存大小
	- `RSS`：进程使用的物理内存大小
- `STAT`：进程状态
	- `R(eady)`：运行或就绪状态
	- `S(leep)`：中断睡眠状态。
	- `D`：不可中断睡眠状态。
	- `T(raced)`：被追踪或已停止的进程。
	- `Z(ombie)`：僵尸进程。
	- `(e)X(terminated)`：死去的进程。
- `TTY`：进程在哪个终端上，如果无终端则为`?`。
- 时间字段：
	- `TIME`：使用的CPU时间
	- `START`：启动时刻
	- `ELAPSED`：已经运行的时间
- 优先级字段：
	- `NI`：nice值，表示动态优先级
	- `PRI`：静态优先级
	- `C`：CPU优先级

## 会话管理相关

`&`：当前命令后台执行

`disown`：解除所有后台进程的归属关系

`fg %<session_id>`：将一个后台进程调至前台

`bg %<session_id>`：将一个前台进程调至后台

`jobs`：获取所有会话
- `jobs -l`：获取所有会话的进程ID
	- 如：等待所有后台进程执行完成：`wait $(jobs -l)`

`wait <pid>`：等待某些进程执行完毕

## crontab：定时任务计划

`cron`命令也可以指定定时任务，但没有直接修改`crontab`来的直接。

执行`crontab -e`以编辑用户自己的任务计划表。

任务计划表格式为：`min hour day month week command`，表示在时间符合的条件下将会执行对应的指令。

每个时间字段的合法取值：
- `*`：所有合法值。
- `a-b`：表示`[a,b]`内的所有合法值。
- `a,b,c`：离散合法值。
- `*/d`：表示每隔`d`取一个合法值。

例如：
- `* * * * * comm`：每分钟执行一次`comm`。
- `3,15 * * * * comm`：每小时的第3和第15分钟执行一次`comm`。
- `3,15 8-11 * * 1 comm`：在每周一上午8:03、8:15、9:03、9:15、10:03、10:15、11:03、11:15共8个时刻各执行一次`comm`
- `30 23 * * * /etc/init.d/smb restart`：每晚23:30重启`smb`
- `0 23-7/1 * * * /etc/init.d/smb restart`：每天晚上11点至次日7点间，每隔一小时重启一次`smb`