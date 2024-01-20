
之前做毕业实训时了解到，QML中的`ImageProvider`用于向QML组件提供图像数据。这里做一个备忘。

参考：
- [blog](https://blog.csdn.net/paulorwys/article/details/131060178)
- 

## 原理

QML可理解为一种受C++控制的标记语言，与HTML类似。QML显示图像通过`Image`元素实现：

```qml
import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    id: root
    width: 640
    height: 480
    visible: true
    title: qsTr("QML Image Provider")

    Image {
        id: image
        anchors.fill: parent
        source: "qrc:/image/1.png"
    }
}
```

这种方法可用于演示资源目录（`qrc:///`）下的图像，或者本地的绝对路径（`file:///...`）下的图像。但如果图像的来源是网络、内存或是其他本地程序，则上述方法失效。

`ImageProvider`是为QML应用提供的一种图像动态加载方式，有如下特点：
- 加载方式不同于静态目录：路径格式为`image://<image_provider_id>/<image_id>`
- 异步加载（不会阻塞UI线程）、可加载内存图像
- 不适用于QWidget和QWebEngine中的html

## 用法

下面的用例代码是从这个项目摘抄的：[github-repo](https://github.com/Daguerreo/QML-ImageProvider)。这是一个通过ImageProvider实现组帧动画的示例。

### C++派生QQuickImageProvider

`QQuickImageProvider`是ImageProvider的虚基类，必须定义其派生类并实现`requestImage`或`requestPixmap`方法。这两个方法用于在QML应用向ImageProvider发起图像请求时，根据请求的图片ID`id`和请求的图片大小`requestedSize`，正确返回其需要的图像。

```cpp
#include <QObject>
#include <QQuickImageProvider>

class MyImageProvider : public QObject, public QQuickImageProvider
{
   Q_OBJECT
public:
   ImageProvider(QObject* parent = nullptr);
   QImage requestImage(const QString& id, QSize* size, const QSize& requestedSize) override;
   // 其他公开成员方法
signals:
   // 信号
   void imageUpdated();
private:
   // 私有成员
};
```

实现细节方面，`requestImage`一般用于载入内存中的图像，所以可以添加一些配置图像的方法，如`setImage(const QImage&)`等。

### 附加到QML应用

ImageProvider必须附加到QML应用上才能生效。可以考虑在`main`函数内进行操作，或适当修改：

```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

#include "MyImageProvider.h"

int main(int argc, char *argv[])
{
   QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
   QGuiApplication app(argc, argv);
   
   // ...
   ImageProvider* provider = new ImageProvider;
   // ...

   // 把provider附加到QML应用上
   QQmlApplicationEngine engine;
   // 这个property名字一般用于设置信号槽，或者其他用途
   engine.rootContext()->setContextProperty("imageProvider", provider);
   // 这个名字很重要，必须和QML Image/Pixmap的source保持一致
   engine.addImageProvider("stream", provider);

   // 下面一般是一些加载QML应用的套话
   const QUrl url(QStringLiteral("qrc:/main.qml"));
   QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
      &app, [url](QObject *obj, const QUrl &objUrl) {
         if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
      }, Qt::QueuedConnection);
   engine.load(url);

   return app.exec();
}

```

### QML中引用

完成上面两步后，QML中应当可以通过设置`source`引用对应图像。

```qml
import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    id: root
    width: 640
    height: 480
    visible: true
    title: qsTr("QML Image Provider")

    // 此元素的作用是将imageProvider自定义的更新信号与图像重新加载方法连接起来。不是必需的。
    Connections {
        target: imageProvider
        function onImageUpdated() { image.reload() }
    }

    Image {
        id: image
        source: "image://stream/1";
        anchors.fill: parent
        fillMode: Image.PreserveAspectFit
        asynchronous: false // 是否异步加载图像，默认true
        cache: false // 是否缓存图像，默认true

        // 一般重新加载图像的比较巧的方法是重设source。
		function reload() {
		    var oldsource = source;
		    source = "";
		    source = oldsource;
		}
    }
}
```