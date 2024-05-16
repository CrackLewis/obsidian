
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

随后启动构建：

```bash
$ make -j8
$ make install
```

在我构建Qt 5.12.5版本源码时，曾出现如下错误：

```
socketcanbackend.cpp:220:48: error: 'CAN RAW_ FD_ FRAMES' was not declared in this scope
```

这是因为低版本的`plugins/canbus/socketcan/socketcanbackend.h`编写有误，没有将`socketcanbackend.cpp`中的如下片段放入`socketcanbackend.h`的最开头部分：

```cpp
#ifndef CANFD_MTU
// CAN FD support was added by Linux kernel 3.6
// For prior kernels we redefine the missing defines here
// they are taken from linux/can/raw.h & linux/can.h

enum {
    CAN_RAW_FD_FRAMES = 5
};

#define CAN_MAX_DLEN 8
#define CANFD_MAX_DLEN 64
struct canfd_frame {
    canid_t can_id;  /* 32 bit CAN_ID + EFF/RTR/ERR flags */
    __u8    len;     /* frame payload length in byte */
    __u8    flags;   /* additional flags for CAN FD */
    __u8    __res0;  /* reserved / padding */
    __u8    __res1;  /* reserved / padding */
    __u8    data[CANFD_MAX_DLEN] __attribute__((aligned(8)));
};
#define CAN_MTU     (sizeof(struct can_frame))
#define CANFD_MTU   (sizeof(struct canfd_frame))

#endif
```

做出上述修改后保存，重新编译，成功。