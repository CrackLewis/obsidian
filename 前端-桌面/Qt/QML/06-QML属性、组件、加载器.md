
## 经验：QML引入外部目录

在`qrc:/`目录很大的情况下，QtQuick项目很难或几乎不能完成编译，因为项目的整个资源目录都会写入一个叫`qrc_qml.cpp`的中间文件，这个文件有可能达到数百MB甚至上GB，从而使编译变得困难。

一种解决方案是：将资源目录的非必要部分外提，放到程序的本地*可执行文件目录*下。

QML引入外部模块遵循如下优先级：
- 官方QtQuick模块
- 项目资源目录
- 本地文件目录
- 远程文件目录

远程文件目录只能引入QML和JS文件，如果需要图片、图标、字体文件之类就不行了；资源目录的容量也十分有限（虚拟机实测20MB就炸）。因此只能用本地文件目录救急。

假设项目目录为`/path/to/project`，项目的生成目录为`/path/to/build`。在不额外添加QML引入目录的情况下，默认引入目录有如下成员：

```
qrc:/qt-project.org/imports
/path/to/qt/5.12.5/gcc_64/qml
qrc:/
/path/to/build
```

如果要额外添加引入目录：

```cpp
QQmlApplicationEngine engine;
engine.addImportPath("/path/to/extrafiles");
```

假如需要被引入的外部模块为`MetroMap`，则该外部模块放置于`/path/to/build`下：

```
+- /path/to/build
	+ ...
	+ MetroMap
		+ qmldir
		+ MapMain.qml
		+ MapSub.qml
		+ ...
	+ ...
```

其中，`qmldir`为模块索引文件，包含如下内容：

```
module MetroMap
MapMain 1.0 MapMain.qml
internal MapSub 1.0 MapSub.qml
```

详细的编写规则见：[doc](https://doc.qt.io/qt-6/qtqml-modules-qmldir.html)

上述`qmldir`文件定义了`/path/to/build/MetroMap`目录为一个名为`MetroMap`的QML模块，其内对外暴露`MapMain`类型。

在`/path/to/project/main.qml`中使用`MapMain`类型：

```
import QtQuick 2.12;

import MetroMap 1.0;

Window {
	...

	MapMain {
		id: mapMain
		...
	}

	...
}
```

