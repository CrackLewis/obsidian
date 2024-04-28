
如果ISO在宿主机，可以：
- 通过VMWare虚拟光驱提供给虚拟机
- 放到共享文件夹，在Linux内部挂载

假设ISO在虚拟机路径为`/path/to/myiso.iso`。

首先创建挂载目录：

```bash
$ sudo mkdir /mnt/myiso
```

随后通过`mount`命令挂载：

```bash
$ sudo mount -t iso9660 -o loop /path/to/myiso.iso /mnt/myiso
```

其中：
- `-t iso9660`：指示文件系统类型，iso9660为默认的ISO文件系统结构。
- `-o loop`：指示设备类型为循环设备。

卸载相对简单：

```bash
$ sudo umount /mnt/myiso
$ sudo rmdir /mnt/myiso
```