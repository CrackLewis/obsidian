
需要先拉取Ubuntu镜像：

```bash
$ docker pull ubuntu:latest
```

如果遇到这种错误，说明你没开Docker Desktop，需要先打开Docker Desktop。
![[Pasted image 20230802131409.png]]

可以通过下列命令创建一个容器，并立即在交互式终端内访问它：
```bash
$ docker run -it ubuntu:latest /bin/bash
```
终端关闭，容器也会停止运行。

也可以将`-it`改成`-d`，使其在后台运行。后台容器需要手动停止。
