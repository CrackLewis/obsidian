
## intro

QML与C++聚合引入的一些可能：
- 分离UI和底层逻辑：QML做UI，C++做逻辑
- 从QML调用更复杂的C++代码
- 调用QtQuick或QtQml的C++ API（如[[02-QML ImageProvider|ImageProvider]]）
- 从C++实现可供QML直接访问的QML类型

C++类可通过下列三种方式暴露给QML：
- 注册为一个可实例化的QML对象类型（`QML_ELEMENT`或`qmlRegisterType<T>`）
- 注册为一个QML Singleton类型（`QML_SINGLETON`）
- 将一个实例化的C++对象嵌入为某个QML对象的特征属性

这是Qt官网给的一个决定采用何种嵌入方式的流程图：
![](https://doc.qt.io/qt-6.2/images/cpp-qml-integration-flowchart.png)

## 将C++类的属性暴露给QML

QML引擎可以访问`QObject`任意派生类的下列成员：
- 特征（property）
- 注册的方法（公有槽函数或`Q_INVOKABLE`）
- 信号
- 枚举（`Q_ENUMS`）

### 直接暴露

被QML引擎直接支持的C++类型有：
- 部分Qt基本类型，见下表
- `QObject`的派生类型
- 以`int/qreal/bool/QString/QUrl`等基本类型为元素类型的`QList`、`QVector`、`std::vector`、`std::list`、`QQueue`、`QSet`、`QStack`
- 以下表基本类型为键、值类型的`QMap`和`std::map`（待测）
- 元素类型可变的数组或映射：`QVariantList`、`QVariantMap`
- `QByteArray`可以转换为JS的`ArrayBuffer`类型
- 通过`Q_DECLARE_METATYPE`注册的值类型

| Qt Type                                                                                                                                                          | QML Basic Type                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| bool                                                                                                                                                             | [bool](https://doc.qt.io/qt-6.2/qml-bool.html)                                                                                                                         |
| unsigned int, int                                                                                                                                                | [int](https://doc.qt.io/qt-6.2/qml-int.html)                                                                                                                           |
| double                                                                                                                                                           | [double](https://doc.qt.io/qt-6.2/qml-double.html)                                                                                                                     |
| float, qreal                                                                                                                                                     | [real](https://doc.qt.io/qt-6.2/qml-real.html)                                                                                                                         |
| [QString](https://doc.qt.io/qt-6.2/qstring.html)                                                                                                                 | [string](https://doc.qt.io/qt-6.2/qml-string.html)                                                                                                                     |
| [QUrl](https://doc.qt.io/qt-6.2/qurl.html)                                                                                                                       | [url](https://doc.qt.io/qt-6.2/qml-url.html)                                                                                                                           |
| [QColor](https://doc.qt.io/qt-6.2/qcolor.html)                                                                                                                   | [color](https://doc.qt.io/qt-6.2/qml-color.html)                                                                                                                       |
| [QFont](https://doc.qt.io/qt-6.2/qfont.html)                                                                                                                     | [font](https://doc.qt.io/qt-6.2/qml-font.html)                                                                                                                         |
| [QDateTime](https://doc.qt.io/qt-6.2/qdatetime.html)                                                                                                             | [date](https://doc.qt.io/qt-6.2/qml-date.html)                                                                                                                         |
| [QPoint](https://doc.qt.io/qt-6.2/qpoint.html), [QPointF](https://doc.qt.io/qt-6.2/qpointf.html)                                                                 | [point](https://doc.qt.io/qt-6.2/qml-point.html)                                                                                                                       |
| [QSize](https://doc.qt.io/qt-6.2/qsize.html), [QSizeF](https://doc.qt.io/qt-6.2/qsizef.html)                                                                     | [size](https://doc.qt.io/qt-6.2/qml-size.html)                                                                                                                         |
| [QRect](https://doc.qt.io/qt-6.2/qrect.html), [QRectF](https://doc.qt.io/qt-6.2/qrectf.html)                                                                     | [rect](https://doc.qt.io/qt-6.2/qml-rect.html)                                                                                                                         |
| [QMatrix4x4](https://doc.qt.io/qt-6.2/qmatrix4x4.html)                                                                                                           | [matrix4x4](https://doc.qt.io/qt-6.2/qml-matrix4x4.html)                                                                                                               |
| [QQuaternion](https://doc.qt.io/qt-6.2/qquaternion.html)                                                                                                         | [quaternion](https://doc.qt.io/qt-6.2/qml-quaternion.html)                                                                                                             |
| [QVector2D](https://doc.qt.io/qt-6.2/qvector2d.html), [QVector3D](https://doc.qt.io/qt-6.2/qvector3d.html), [QVector4D](https://doc.qt.io/qt-6.2/qvector4d.html) | [vector2d](https://doc.qt.io/qt-6.2/qml-vector2d.html), [vector3d](https://doc.qt.io/qt-6.2/qml-vector3d.html), [vector4d](https://doc.qt.io/qt-6.2/qml-vector4d.html) |
| Enums declared with [Q_ENUM](https://doc.qt.io/qt-6.2/qobject.html#Q_ENUM)() or Q_ENUMS()                                                                        | [enumeration](https://doc.qt.io/qt-6.2/qml-enumeration.html)                                                                                                           |

### 对象列表

以`QObject`派生对象为元素类型的列表必须通过`QQmlListProperty`暴露给QML。

详见[[E01-QML官方示例学习#示例二：在对象类型中添加列表和对象属性]]。

### 组特征

如果C++类有`QObject`派生类指针作为成员，则该成员作为C++类型的一个*组属性*供QML访问。访问组属性的成员属性用`groupProperty.member`的形式。

### 暴露方法

需要将被暴露的方法声明为`Q_INVOKABLE`或公用槽函数（public slots）。

### 暴露信号

需要将被暴露的信号声明为signals。信号主体必须是`QObject`的派生类。

## 在QML类型系统中注册C++类型

**注意**：Qt5的早期版本没有下面这些宏，需要使用`qmlRegister***`方法。

*可实例化*的类型：`QML_ELEMENT`

*不可实例化*的类型：
- `QML_ANONYMOUS`：注册一个不可被QML访问、也不能实例化的类型
- `QML_INTERFACE`：注册一个Qt接口类型。接口类型不可自行实例化，但实现该接口的C++类型可以被转换为该类型。
- `QML_UNCREATABLE(reason)`：注册一个属于QML类型但不可实例化的C++类型。
- `QML_SINGLETON`：注册一个可被QML访问的单体类型。

`QML_EXTENDED(ext_type)`用于注册*扩展类型*。

[Registering Extension Objects](https://doc.qt.io/qt-6.2/qtqml-cppintegration-definetypes.html#registering-extension-objects)

如果欲引入QML的C++类型不便修改，则可以通过`QML_FOREIGN(type)`注册*外部类型*，使该类型挂载被引入的`type`类型。

如果需要编写一个*属性修改器*（property modifier），需要顺带`QQmlPropertyValueSource`，详情见[doc](https://doc.qt.io/qt-6.2/qtqml-cppintegration-definetypes.html#property-modifier-types)。

如果C++类型需要是可视对象，则需要继承`QQuickItem`及其派生类型。

## 将C++对象作为属性嵌入QML

例如：

```cpp
QQuickView view;
view.rootContext()->setContextProperty("currentDateTime", QDateTime::currentDateTime());
view.setSource(QUrl::fromLocalFile("MyItem.qml"));
view.show();
```

这种写法常用于：
- 在`root`对象下绑定全局属性
- 将C++数据结构绑定到QML ListModel或其他数据模型

## 与C++定义的QML对象交互

主要有3种方法：
- 从C++接口访问QML对象
- 指名访问加载完毕的QML对象
- 从C++访问QML对象的成员

文档：[doc](https://doc.qt.io/qt-6.2/qtqml-cppintegration-interactqmlfromcpp.html)

## C++与QML类型转换

[[#直接暴露]]小节已经详细讲述，这里不再赘述。