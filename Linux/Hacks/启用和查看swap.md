
场景：系统内存较低，不足以支撑高负载任务

定义：
- swap：Linux内存交换空间
- swap文件：被用作内存交换的特殊文件。内部采用swap格式，用前需要格式化+挂载
- swap分区：格式化为swap的物理/虚拟分区，可以来自物理介质或其他分区上的文件

## 检查swap状态

查看主存和swap的占用情况：`free -h`
- `Swap`不显示或`total`为0时，表示系统未启用swap

swap操纵：`swapon`
- `swapon --show`：展示哪些分区或文件被启用为swap分区
	- 和`cat /proc/swaps`类似

查看是否存在类型为swap的分区：`lsblk -f | grep swap`

查看是否存在永久的swap配置：`cat /etc/fstab | grep swap`

## 启用swap文件为swap

首先分配一个指定大小的空文件：

```sh
$ sudo fallocate -l 4G /swapfile
```

然后设置只有管理员有读写权限：

```sh
$ sudo chmod 600 /swapfile
```

格式化为swap：

```sh
$ sudo mkswap /swapfile
```

启用swap文件：

```sh
$ sudo swapon /swapfile
```

## 启用swap分区为swap

启用之：

```sh
$ sudo swapon /dev/sdb1
```

如果是物理介质swap分区，建议使用uuid而非设备名（`/dev/sdb1`之类）标识

## 使swap设置长期生效

修改`/etc/fstab`，在表尾添加一行：

```
/your-swap-file-or-partition none swap sw 0 0
```

