
官方示例主页：[QML Extending Examples](https://doc.qt.io/qt-5/qmlextendingexamples.html)

## 太长不读



## 示例一：注册对象类型

在QML中可使用自定义的C++类型作为*对象类型*。

被使用的C++类型需满足如下条件：
- 由`QObject`派生，且包含`Q_OBJECT`声明
- 通过`Q_PROPERTY`声明可以被访问或修改的属性
- （可选）如果需要作为元素，则包括`QML_ELEMENT`属性
	- 在低版本没有这个宏，则需要借助`qmlRegisterType`方法
- （可选）声明信号
- （可选）如果需要访问C++方法，则通过`public slots`或`Q_INVOKABLE`声明
- （可选）如果对象需要在JavaScript中被访问，或在`QVariant`中存储，或作为信号或槽参数，或在`QSettings`中存储，或用于QML模型/视图框架，则需要通过`Q_DECLARE_METATYPE`声明为*元类型*

例如：在QML中欲使用C++中定义的`Person`类型：

```q
import People 1.0

Person {
    name: "Bob Jones"
    shoeSize: 12
}
```

`Person`类型定义：

```cpp
// Person.h
class Person : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString name READ name WRITE setName)
    Q_PROPERTY(int shoeSize READ shoeSize WRITE setShoeSize)
    QML_ELEMENT
public:
    Person(QObject *parent = nullptr);

    QString name() const;
    void setName(const QString &);

    int shoeSize() const;
    void setShoeSize(int);

private:
    QString m_name;
    int m_shoeSize;
};

// Person.cpp
Person::Person(QObject *parent)
: QObject(parent), m_shoeSize(0)
{
}

QString Person::name() const
{
    return m_name;
}

void Person::setName(const QString &n)
{
    m_name = n;
}

int Person::shoeSize() const
{
    return m_shoeSize;
}

void Person::setShoeSize(int s)
{
    m_shoeSize = s;
}
```

## 示例二：在对象类型中添加列表和对象属性

示例一讲解了可用于创建QML对象的C++类型的必要特征：
- `QObject`派生
- `Q_PROPERTY`、`Q_OBJECT`、`Q_INVOKABLE`、`Q_DECLARE_METATYPE`等声明

大部分C++基本类型、Qt基本类型可以*自动转换*为QML的对应类型：

| Qt Type                                                                                                                                                    | QML Value Type                                                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| bool                                                                                                                                                       | [bool](https://doc.qt.io/qt-6/qml-bool.html)                                                                                                                     |
| unsigned int, int                                                                                                                                          | [int](https://doc.qt.io/qt-6/qml-int.html)                                                                                                                       |
| double                                                                                                                                                     | [double](https://doc.qt.io/qt-6/qml-double.html)                                                                                                                 |
| float, qreal                                                                                                                                               | [real](https://doc.qt.io/qt-6/qml-real.html)                                                                                                                     |
| [QString](https://doc.qt.io/qt-6/qstring.html)                                                                                                             | [string](https://doc.qt.io/qt-6/qml-string.html)                                                                                                                 |
| [QUrl](https://doc.qt.io/qt-6/qurl.html)                                                                                                                   | [url](https://doc.qt.io/qt-6/qml-url.html)                                                                                                                       |
| [QColor](https://doc.qt.io/qt-6/qcolor.html)                                                                                                               | [color](https://doc.qt.io/qt-6/qml-color.html)                                                                                                                   |
| [QFont](https://doc.qt.io/qt-6/qfont.html)                                                                                                                 | [font](https://doc.qt.io/qt-6/qml-font.html)                                                                                                                     |
| [QDateTime](https://doc.qt.io/qt-6/qdatetime.html)                                                                                                         | [date](https://doc.qt.io/qt-6/qml-date.html)                                                                                                                     |
| [QPoint](https://doc.qt.io/qt-6/qpoint.html), [QPointF](https://doc.qt.io/qt-6/qpointf.html)                                                               | [point](https://doc.qt.io/qt-6/qml-point.html)                                                                                                                   |
| [QSize](https://doc.qt.io/qt-6/qsize.html), [QSizeF](https://doc.qt.io/qt-6/qsizef.html)                                                                   | [size](https://doc.qt.io/qt-6/qml-size.html)                                                                                                                     |
| [QRect](https://doc.qt.io/qt-6/qrect.html), [QRectF](https://doc.qt.io/qt-6/qrectf.html)                                                                   | [rect](https://doc.qt.io/qt-6/qml-rect.html)                                                                                                                     |
| [QMatrix4x4](https://doc.qt.io/qt-6/qmatrix4x4.html)                                                                                                       | [matrix4x4](https://doc.qt.io/qt-6/qml-matrix4x4.html)                                                                                                           |
| [QQuaternion](https://doc.qt.io/qt-6/qquaternion.html)                                                                                                     | [quaternion](https://doc.qt.io/qt-6/qml-quaternion.html)                                                                                                         |
| [QVector2D](https://doc.qt.io/qt-6/qvector2d.html), [QVector3D](https://doc.qt.io/qt-6/qvector3d.html), [QVector4D](https://doc.qt.io/qt-6/qvector4d.html) | [vector2d](https://doc.qt.io/qt-6/qml-vector2d.html), [vector3d](https://doc.qt.io/qt-6/qml-vector3d.html), [vector4d](https://doc.qt.io/qt-6/qml-vector4d.html) |
| Enums declared with [Q_ENUM](https://doc.qt.io/qt-6/qobject.html#Q_ENUM)()                                                                                 | [enumeration](https://doc.qt.io/qt-6/qml-enumeration.html)                                                                                                       |

Qt对象及其派生类型如果正确地声明为了*QML对象类型*，可以完成自动转换，目标类型是JS的*Object类型*。

以前表所列简单类型为元素的`QList`、`QVector`和`std::vector`也可以完成自动转换，目标类型是*JS数组*。

但相对复杂的类型，诸如以Qt对象为元素的列表等，则不能完成自动转换，而必须借助QML引擎提供的C++设施完成。

以列表属性为例，列表属性使用`QQmlListProperty<T>`类型。该类型封装了一系列成员函数指针，当QML需要对列表属性执行对应操作时，回调执行这些函数。

示例：基于上个示例的`Person`类型，假如需要定义一个`BirthdayParty`类型，包括`host`属性（`Person`类型）和`guest`属性（`Person`列表类型）。那么对应的定义实现如下：

```cpp
// BirthdayParty.h
#ifndef BIRTHDAYPARTY_H
#define BIRTHDAYPARTY_H

#include <QObject>
#include <QVector>
#include <QQmlListProperty>
#include "person.h"

class BirthdayParty : public QObject
{
    Q_OBJECT
    Q_PROPERTY(Person *host READ host WRITE setHost)
    Q_PROPERTY(QQmlListProperty<Person> guests READ guests)
    QML_ELEMENT
public:
    BirthdayParty(QObject *parent = nullptr);

    Person *host() const;
    void setHost(Person *);

    QQmlListProperty<Person> guests();
    void appendGuest(Person*);
    int guestCount() const;
    Person *guest(int) const;
    void clearGuests();
    void replaceGuest(int, Person*);
    void removeLastGuest();

private:
    static void appendGuest(QQmlListProperty<Person>*, Person*);
    static int guestCount(QQmlListProperty<Person>*);
    static Person* guest(QQmlListProperty<Person>*, int);
    static void clearGuests(QQmlListProperty<Person>*);
    static void replaceGuest(QQmlListProperty<Person>*, int, Person*);
    static void removeLastGuest(QQmlListProperty<Person>*);

    Person *m_host;
    QVector<Person *> m_guests;
};

#endif // BIRTHDAYPARTY_H

// BirthdayParty.cpp
#include "BirthdayParty.h"

BirthdayParty::BirthdayParty(QObject *parent)
: QObject(parent), m_host(nullptr)
{
}

Person *BirthdayParty::host() const
{
    return m_host;
}

void BirthdayParty::setHost(Person *c)
{
    m_host = c;
}

QQmlListProperty<Person> BirthdayParty::guests()
{
    return {this, this,
             &BirthdayParty::appendGuest,
             &BirthdayParty::guestCount,
             &BirthdayParty::guest,
             &BirthdayParty::clearGuests,
             &BirthdayParty::replaceGuest,
             &BirthdayParty::removeLastGuest};
}

void BirthdayParty::appendGuest(Person* p) {
    m_guests.append(p);
}

int BirthdayParty::guestCount() const
{
    return m_guests.count();
}

Person *BirthdayParty::guest(int index) const
{
    return m_guests.at(index);
}

void BirthdayParty::clearGuests() {
    m_guests.clear();
}

void BirthdayParty::replaceGuest(int index, Person *p)
{
    m_guests[index] = p;
}

void BirthdayParty::removeLastGuest()
{
    m_guests.removeLast();
}

void BirthdayParty::appendGuest(QQmlListProperty<Person>* list, Person* p) {
    reinterpret_cast< BirthdayParty* >(list->data)->appendGuest(p);
}

void BirthdayParty::clearGuests(QQmlListProperty<Person>* list) {
    reinterpret_cast< BirthdayParty* >(list->data)->clearGuests();
}

void BirthdayParty::replaceGuest(QQmlListProperty<Person> *list, int i, Person *p)
{
    reinterpret_cast< BirthdayParty* >(list->data)->replaceGuest(i, p);
}

void BirthdayParty::removeLastGuest(QQmlListProperty<Person> *list)
{
    reinterpret_cast< BirthdayParty* >(list->data)->removeLastGuest();
}

Person* BirthdayParty::guest(QQmlListProperty<Person>* list, int i) {
    return reinterpret_cast< BirthdayParty* >(list->data)->guest(i);
}

int BirthdayParty::guestCount(QQmlListProperty<Person>* list) {
    return reinterpret_cast< BirthdayParty* >(list->data)->guestCount();
}
```

*特别地*，如果列表的上述逻辑（追加元素、计数、随机访问、清空、随机替换、移除末尾元素）与`QList`完全一致，则不必定义上面那12个函数，而直接将`guests`替换为这种写法：

```cpp
QQmlListProperty<Person> BirthdayParty::guests() {
	return QQmlListProperty<Person>(this, m_guests);
}
```

两种写法是完全等价的。

*注意*：
- 在Qt 5.12版本中没有要求随机替换和移除末尾元素的回调函数，该版本要求4个而非6个回调函数。
- 元素类型`T`必须是`QObject`的派生类型。
- 如果使用了上面所用的简便写法，则容器类型必须是`QList<T*>`。
- 注意上面的回调函数中，涉及`T`类型的参数均为`T*`，均不为`T`。
- 虽然文档未明确规定，但从个人实操来看，回调函数似乎必须是外部函数或静态成员函数。

## 示例三：注册扩展类型

`QML_EXTENDED`宏可用于注册一个扩展类型。

扩展类型在5.15版本开始出现，它允许QML引擎在用户不修改`QObject`类型源码的情形下，加载这个原本不可加载的类型。

WIP

## 示例四：继承和强制示例

基于前面的[[#示例二：在对象类型中添加列表和对象属性]]。

假如我们需要把`Person`派生为`Boy`和`Girl`类型，并为它们添加一些自定义的行为，但我们不希望存在不为`Boy`或`Girl`类型的`Person`对象。

这个时候我们不能将`Person`变为虚类，而是需要使用`QML_UNCREATABLE(reason)`宏。该宏的作用是：声明一个QML类型不能用自己的构造器实例化，但允许该类的派生类型转换为该类对象，以便使用该类成员。

WIP

## 示例五：为对象类型添加方法

基于前面的示例四。

对象类型可以添加可被QML访问的成员方法，做法是：
- 声明前加`Q_INVOKABLE`。
- 参数类型为合法的*对象类型*或*值类型*。

示例：

```cpp
// birthdayparty.h
#ifndef BIRTHDAYPARTY_H
#define BIRTHDAYPARTY_H

// 未变部分
class BirthdayParty : public QObject
{
    // 未变部分
    Q_INVOKABLE void invite(const QString &name);
	// 未变部分
};

#endif // BIRTHDAYPARTY_H

// birthdayparty.cpp
void BirthdayParty::invite(const QString &name)
{
    auto *person = new Person(this);
    person->setName(name);
    m_guests.append(person);
}
```

## 示例六：绑定属性

WIP

## 示例七：信号与槽支持

WIP

## 示例八：