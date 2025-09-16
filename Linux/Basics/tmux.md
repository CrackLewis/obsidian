 
参考资料：
- [博客](https://blog.csdn.net/CSSDCC/article/details/121231906)

## 基本概念

tmux=Terminal Multiplexer，终端复用器

基本概念：
- `session`：一个tmux会话（任务），在前台或后台运行一或多个窗口
- `window`：一个窗口，运行在一个会话中，维护一或多个窗格
- `pane`：一个窗格

## session操作

新建会话：新建一个会话`my_session`，并将终端绑定到会话中。

```bash
$ tmux new -s my_session
```

分离会话（快捷键：`^b d`）：将会话与终端解绑。会话脱离终端，作为独立进程继续运行。

```bash
$ tmux detach
```

绑定会话：将会话`my_session`与终端绑定。终端将被阻塞直至解绑或会话结束。

```bash
$ tmux attach -t my_session
```

切换会话：从当前会话切换到`my_session`会话。

```bash
$ tmux switch -t my_session
```

重命名会话（快捷键：`^b $`）：

```bash
$ tmux rename-session -t my_old_session my_new_session
```

强制结束会话：

```bash
$ tmux kill-session -t my_session
```

查看所有活动会话（快捷键：`^b s`）：

```bash
# 两种命令等价
$ tmux ls
$ tmux list-sessions
```

## window操作

新建窗口（快捷键：`^b c`）：

```bash
$ tmux new-window
$ tmux new-window -n win2
```

切换窗口（快捷键：`^b w`或`^b <数字键>`）：

```bash
$ tmux select-window -t 0 # 窗口ID
$ tmux select-window -t win2 # 窗口名
```

重命名当前窗口（快捷键：`^b ,`）：

```bash
$ tmux rename-window new_window
```

在同一会话内切换窗口：
- 上一个窗口：`^b p`
- 下一个窗口：`^b n`

## pane操作

划分窗格：

```bash
# 划分上下两个窗格
$ tmux split-window
# 划分左右两个窗格
$ tmux split-window -h
```

移动窗格光标，让其切换到其他窗格：

```bash
# U/D/L/R表示上下左右
$ tmux select-pane -U
$ tmux select-pane -D
$ tmux select-pane -L
$ tmux select-pane -R
```

交换窗格位置：

```bash
$ tmux swap-pane -U
$ tmux swap-pane -D
$ tmux swap-pane -L
$ tmux swap-pane -R
```

窗格操作更多地依赖快捷键而非命令。具体的快捷键操作见快捷键总结小节。

## 其他操作

如果记不住快捷键，可以通过命令查看：

```bash
$ tmux list-keys
```

如果命令也记不住，也可以看：

```bash
$ tmux list-commands
```

列出所有的活动会话：

```bash
$ tmux info
```

重新加载tmux配置：

```bash
$ tmux source-file ~/.tmux.conf
```

## 快捷键总结

快捷键只在tmux会话内可用，且总是以`Ctrl-b`开头（`^b`），带一个其他键。

可以通过`tmux list-keys`查看所有键，但最好还是记忆一些常用组合键：

会话相关：
- `d`：分离当前会话。（detach）
- `s`：列出所有会话。（sessions）
- `$`：重命名当前会话。

窗口相关：
- `c`：创建一个新窗口。（create）
- `p`：上一个窗口。（previous）
- `n`：下一个窗口。（next）
- `<数字键>`：切换到对应数字指定ID的窗口。
- `w`：显示所有窗口。（windows）
- `,`：窗口重命名。

窗格相关：
- 创建窗格：
	- `%`：划分左右窗格
	- `"`：划分上下窗格
- 光标切换：
	- `;`：切换到上一个窗格
	- `o`：切换到下一个窗格
	- `<方向键>`：切换到其他窗格
- 窗格移动：
	- `{`：窗格左移
	- `}`：窗格右移
	- `^o`（`Ctrl-o`）：窗格上移
	- `A-o`（`Alt-o`）：窗格下移
- 其他：
	- `x`：关闭窗格（需要确认）
	- `!`：窗格拆分为独立窗口
	- `z`：当前窗格在全屏和正常模式切换
	- `^<方向键>`（`Ctrl-<方向键>`）：按箭头方向调整窗口大小
	- `q`：显示窗格编号