
在某一次关闭并重启Hyper-V后，WSL2无法启动，经过一个weishi的修复流程才解决问题。这里简作备忘。

首先打开`appwiz.cpl`，点击“打开或关闭Windows功能”，确保这三个项目*全部勾选*：
- Hyper-V
- 适用于Windows的Linux子系统
- 虚拟机平台

在管理员控制台下，执行`bcdedit /set hypervisorlaunchtype Auto`。

检查`bcdedit | find /i "hypervisor"`，确保`hypervisorlaunchtype`变量为`Auto`而非`off`。

240626：目测无后续问题