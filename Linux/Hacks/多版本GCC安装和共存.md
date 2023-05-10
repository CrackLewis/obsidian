
GCC安装方法：
- 手动编译：不推荐。编译耗时长，出错率高，即使编译成功也不太容易解决运行时依赖。
- 官方apt仓库：不太推荐。默认版本比较老旧（gcc-9），更新或者更旧的都不支持。
- 第三方apt仓库：推荐。虽然第三方质量不一定有保证，但更新绝对比官方的快。

## 230424：GCC-5安装

阿里云Ubuntu Xenial仓库实测仍然支持GCC-5。目前没有发现稳定支持GCC-4的apt仓库。

```
deb http://mirrors.aliyun.com/ubuntu/ xenial main
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main
deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb-src http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main
deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security universe
```

使用该仓库需要添加公钥，使系统信任此仓库：
```bash
$ gpg --keyserver keyserver.ubuntu.com --recv-keys 437D05B5
$ gpg --export --armor 437D05B5 | sudo apt-key add -
```

更新apt源：
```bash
$ sudo apt-get update
```

通过`apt-cache`检索GCC-5的包信息：
```bash
$ apt-cache policy gcc-5
```

安装GCC-5：
```bash
$ sudo apt-get install gcc-5
```

由于Ubuntu 22.04的默认编译器为GCC-11，所以需要通过`update-alternatives`使GCC-5与GCC-11共存。
```bash
$ sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 120
```

如果需要调整当前`/usr/bin/gcc`指代哪个编译器，则执行：
```bash
$ sudo update-alternatives --config gcc
```