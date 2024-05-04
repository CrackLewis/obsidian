
源码在`download.qt.io/archive/qt`下。实测挂欧洲梯子下载速度会快一点。

假设下载的是`qt-everywhere-src-5.12.5.tar.xz`，解压后需要先执行`configure`：

```bash
$ ./configure -release -opensource -confirm-license -platform linux-g++ -xplatform linux-arm-gnueabi-g++ -device-option CROSS_COMPILE=arm-linux- -nomake tests -nomake examples -prefix /home/cracklewis/arm-qt5.12.5 -qpa linuxfb
```

如果工具链提示没有`arm-linux-gnueabi-g++`，那么就需要修改源码根目录内`qtbase/mkspecs/linux-arm-gnueabi-g++`下的`qmake.conf`文件。下面是一个修改示例，它将交叉编译器修改为了`arm-linux-g++`，而非原本的`arm-linux-gnueabi-g++`：

```conf
#
# qmake configuration for building with arm-linux-gnueabi-g++
#

MAKEFILE_GENERATOR      = UNIX
CONFIG                 += incremental
QMAKE_INCREMENTAL_STYLE = sublib

include(../common/linux.conf)
include(../common/gcc-base-unix.conf)
include(../common/g++-unix.conf)

# modifications to g++.conf
QMAKE_CC                = arm-linux-gcc
QMAKE_CXX               = arm-linux-g++
QMAKE_LINK              = arm-linux-g++
QMAKE_LINK_SHLIB        = arm-linux-g++

# modifications to linux.conf
QMAKE_AR                = arm-linux-ar cqs
QMAKE_OBJCOPY           = arm-linux-objcopy
QMAKE_NM                = arm-linux-nm -P
QMAKE_STRIP             = arm-linux-strip
load(qt_config)
```