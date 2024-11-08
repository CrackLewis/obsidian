
WSL2是臭名昭著的吃C盘大户，迁移到其他盘有时非常必要。

假设要迁移的分发版为`Ubuntu-24.04`。迁移前首先要将对应分发版关机：

```
wsl --terminate Ubuntu-24.04
```

可通过`wsl -l -v`检查其是否关机。确保关机后，假设要导出到`G:\MyLoc`，则导出命令为：

```
wsl --export Ubuntu-24.04 G:\MyLoc\wsl2_241108.tar
```

确保分发版正确导出后，将原先的`Ubuntu-24.04`注销：

```
wsl --unregister Ubuntu-24.04
```

此时在C盘的根文件系统被删除。假设需要迁移到`G:\WSL`下，则需要通过如下命令将其重新导入：

```
wsl --import Ubuntu-24.04 G:\WSL G:\MyLoc\wsl2_241108.tar
```

启动后，如果发现用户变成了`root`，则需要将默认用户切换为自己安装时指定的用户：

```
Ubuntu2404 config --default-user CrackLewis
```

利用WSL2可进行全盘备份的机制，可以实施有计划的备份，并在必要时还原。思路如下：
- 利用`wsl --export`命令定期生成导出文件。
- 将导出文件高度压缩（如7z格式）。实测2GB的WSL2压缩后剩余约400MB。
- 压缩后的导出文件存储在其他介质，如果WSL2发生不可逆损坏，则通过这些导出文件还原WSL2。