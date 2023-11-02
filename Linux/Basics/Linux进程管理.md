
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