
refs:
- [blog: Ubuntu 20.04 安装Cuda 12.2版本踩坑记录](https://blog.csdn.net/shizheng_Li/article/details/145059260)
- 

## CUDA Toolkit

通过nvidia-smi检查CUDA版本，在nvidia官网找安装包（以CUDA 12.3.2为例）：

```
https://developer.nvidia.com/cuda-12-3-2-download-archive
```

博客原文建议通过runfile而非deb包安装。

下载完毕后，执行`sh cuda_12.3.2_545.23.08_linux.run`。在安装选项处，个人暂不勾选NVIDIA driver，因为博客指出可能会安装失败。

安装完毕后的输出：

```
===========
= Summary =
===========

Driver:   Not Selected
Toolkit:  Installed in /usr/local/cuda-12.3/

Please make sure that
 -   PATH includes /usr/local/cuda-12.3/bin
 -   LD_LIBRARY_PATH includes /usr/local/cuda-12.3/lib64, or, add /usr/local/cuda-12.3/lib64 to /etc/ld.so.conf and run ldconfig as root

To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-12.3/bin
***WARNING: Incomplete installation! This installation did not install the CUDA Driver. A driver of version at least 545.00 is required for CUDA 12.3 functionality to work.
To install the driver using this installer, run the following command, replacing <CudaInstaller> with the name of this run file:
    sudo <CudaInstaller>.run --silent --driver

Logfile is /var/log/cuda-installer.log
```

安装完成后，将CUDA 12.3的路径加入到`PATH`和`LD_LIBRARY_PATH`内：

```sh
# Add CUDA 12.3 to PATH and LD_LIBRARY_PATH
export PATH=/usr/local/cuda-12.3/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.3/lib64:$LD_LIBRARY_PATH
```

如果`/usr/local/cuda`或`/usr/local/cuda-12`指向之前安装过的其他CUDA版本，则需要修改对应的软链接：

```sh
$ sudo rm /etc/alternatives/cuda 
$ sudo rm /etc/alternatives/cuda-12
$ sudo ln -s /usr/local/cuda-12.3 /etc/alternatives/cuda
$ sudo ln -s /usr/local/cuda-12.3 /etc/alternatives/cuda-12
```

也可以通过`update-alternatives`工具管理软链接的具体指向。

对于NVIDIA驱动，如果设备没有已安装的，则需要通过apt/yum或者CUDA installer安装一个，要确保不低于系统CUDA版本。

检查安装完整性（可能需要`source ~/.bashrc`或重启终端）：

```sh
$ echo $PATH
$ echo $LD_LIBRARY_PATH
$ nvcc --version
```

## cuDNN

比CUDA略简单，需要通过deb安装。

在[官网](https://developer.nvidia.com/cudnn-downloads)下载deb包后，执行安装命令（可能要求安装GPG keyring）：

```sh
$ sudo dpkg -i cudnn-local-repo-ubuntu2004-9.7.1_1.0-1_amd64.deb
$ sudo cp /var/cudnn-local-repo-ubuntu2004-9.7.1/cudnn-local-30657C6C-keyring.gpg /usr/share/keyrings/
```

随后执行：

```sh
$ sudo apt update
$ sudo apt install cudnn9-cuda-12 -y
```

最后：

```sh

```

## OpenCV

以4.10.0版本为例。

