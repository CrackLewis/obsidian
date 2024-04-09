
![[Pasted image 20231227203132.png]]

**QML是什么？**

一种用于描述应用程序用户界面的声明式编程语言。

> QML is a declarative language that allows user interfaces to be described in terms of their visual components and how they interact and relate with one another.

**Qt Quick 是什么？**

QML 类型和功能的标准库，包括可视化类型、交互式类型、动画功能、模型和视图，特效等。

> Qt Quick is the standard library of types and functionality for QML. It includes visual types, interactive types, animations, models and views, particle effects and shader effects.  

简单地理解，Qt Quick 是用于编写 QML 应用的标准库。

## 创建QML项目

建立QtQuick项目即可

示例代码：

main.cpp：
```cpp
int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;
    const QUrl url(QStringLiteral("qrc:/main.qml"));

    QObject::connect(&engine,
        &QQmlApplicationEngine::objectCreated,
        &app, 
        [url](QObject *obj, const QUrl &objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
            },
        Qt::QueuedConnection);

    engine.load(url);
    return app.exec();
}
```

main.qml：
```qml
import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    visible: true
    width: 320
    height: 240
    title: qsTr("es-hacker: QML demo")

    Rectangle {
        width: parent.width
        height: parent.height
        color: "Green"

        Text {
            anchors.centerIn: parent
            font.pixelSize: Qt.application.font.pixelSize * 2
            text: "Hello, World!"
        }
    }
}
```

## QML Window

QML窗口元素。

常用属性：
- `x`、`y`：左坐标、上坐标
- `width`、`height`：宽度、高度
- `title`：窗口标题
- `maximumHeight`、`minimumHeight`、`maximumWidth`、`minimumWidth`：宽高的限定范围
- `visible`：是否可见
- `opacity`：透明度

定义信号和槽：
```
Window {
	signal mySig()

	onMySig: {
		// implement
	}
}
```

## QML Item

- `id`（元素唯一标识）、`objectName`（元素字面名称）
- `x`、`y`、`z`：左上坐标、层叠坐标
- `width`、`height`
- `opacity`（不透明度）、`visible`（可见性，bool）
- `rotation`（旋转角度）、`rotationOrigin`（旋转中心）
- `scale`：缩放比
- `clip`：是否剪裁越界内容
- `anchors`：定义元素相对其父项或其他项的布局约束，包括水平和垂直的边界约束
- `transformOrigin`：缩放和变换中心
- `border`（边框宽度和颜色）、`radius`（圆角半径）
- `smooth`（渲染质量，`true`为平滑，`false`为快速）
- `enabled`：元素是否启用

### anchor的简单用法

[[03-QML布局#anchors]]

相对其他元素定位：
```qml
Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    Rectangle {
        id: rect1
        x: 0; y: 0
        width: 100; height: 50; color: "red"
    }

    Rectangle {
        id: rect2
        // 相对rect1向右20
        anchors.left: rect1.right; anchors.leftMargin: 20
        width: 100; height: 50; color: "green"
    }

    Rectangle {
        id: rect3
        // 相对rect1向下20
        anchors.top: rect1.bottom; anchors.topMargin: 20
        width: 100; height: 50; color: "blue"
    }
}
```

![[Pasted image 20231227223652.png]]

在父元素内部的排列形式：

填充：
```qml
Window {
	// ...
    Rectangle {
        id: rect1
        // 窗口是200x100，但元素仍然填充了整个窗口
        anchors.fill: parent
        width: 100; height: 50; color: "cyan"
    }
}
```
![[Pasted image 20231227224019.png]]

双向居中：
```qml
Window {
	// ...
    Rectangle {
        id: rect1
        // 由于窗口更大，所以只是居中排布
        anchors.centerIn: parent
        width: 100; height: 50; color: "cyan"
    }
}
```
![[Pasted image 20231227224240.png]]

## QML Rectangle

继承Item

常用属性
- `color`：填充颜色