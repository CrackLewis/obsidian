
## entry-hacks

Windows下安装Docker Desktop到非C盘：

```sh
$ "Docker Desktop Installer.exe" install --quiet --accept-license --backend=hyper-v --always-run-service --installation-dir=G:\DockerDesktop\installer --hyper-v-default-data-root=G:\DockerDesktop\hyper-v-data 
```

Docker换源：
- 全局修改：在Settings-Docker Engine中修改：

```json
{
  "registry": {
    ...
  }
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false
}
```

- 单镜像换源：假如原pull命令是`docker pull lewis/xv6:1.0`，换源`abc.xyz`后的pull命令变更为`docker pull abc.xyz/lewis/xv6:1.0`。

活跃的换源列表：
- [list1](https://xuanyuan.me/blog/archives/1154)：240920-
- 

