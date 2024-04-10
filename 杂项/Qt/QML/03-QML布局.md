
做毕设时遇到了一些玄学问题，感觉有必要认真研究一下QML布局。

## 硬编码布局

通过设置`x,y,width,height`实现定点布局，类似于QObject的geometry。

## Layout

`import QtQuick.Layouts 1.xx`

是QML内置的一类布局对象，为子成员提供布局相关的属性。

在1.12中，Layout对象有三类：`GridLayout`、`RowLayout`、`ColumnLayout`。

Layout对象为其所有子孙成员提供如下属性：
- `Layout.alignment`：成员在Layout内的对齐方式
- `Layout.<minimum|preferred|maximum>Width`：最小、推荐和最大宽度
- `Layout.<minimum|preferred|maximum>Height`：最小、推荐和最大高度
- `Layout.<top|bottom|left|right>Margin`：上下左右的外边界宽度
- `Layout.margins`：为元素指定相同的外边界宽度
- `Layout.row`：（限GridLayout）指定在网格中的行号，从0开始
- `Layout.column`：（限GridLayout）指定在网格中的列号，从0开始
- `Layout.rowSpan`：（限GridLayout）行间距
- `Layout.columnSpan`：（限GridLayout）列间距
- `Layout.fillWidth`：是否采用允许的最大宽度
- `Layout.fillHeight`：是否采用允许的最大高度

### 宽高设定机制

Layout内元素的宽高属性值如下确定：
- 宽高的上下限：
	- 如无指定上下限（*隐式*）：
		- 如果元素是Layout对象：上限为所有组件采用最大或最小宽高情形下的宽高
		- 如果不是：上限为`Number.POSITIVE_INFINITY`，下限为0
	- 如指定了上下限（*显式*）：采用指定的上下限
- 宽高的推荐值：只能自行指定

宽高的最终值由其所在Layout最终确定：
- 若`Layout.fillWidth`或`Layout.fillHeight`为真：元素宽高将在上下限之间确定。
- 否则：尽量设定为`preferredHeight`和`preferredWidth`

**注意**：不要对Layout子元素设置`x,y,width,height`属性，它们会和Layout冲突。

例如：下面的窗口按水平方向交替显示红绿矩形：

```
import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12
import QtQuick.Layouts 1.12

Window {
    id: root
    width: 1920
    height: 360
    visible: true

    RowLayout {
        anchors.fill: parent

        Repeater {
            model: ["apples", "banana", "pineapple", "lemon", "mango"]
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: root.height
                color: index % 2 ? "red" : "green"

                Text {
                    anchors.centerIn: parent
                    text: modelData
                }
            }
        }
    }
}
```

### 对齐

`Layout.alignment`有7个合法值：
- `Qt.AlignLeft`、`Qt.AlignRight`、`Qt.AlignTop`、`Qt.AlignBottom`：顾名思义
- `Qt.AlignHCenter`、`Qt.AlignVCenter`：水平和垂直居中
- `Qt.AlignBaseLine`：与基线对齐

如果需要采用多个值，用`|`，如`Qt.AlignLeft | Qt.AlignVCenter`表示水平靠左、垂直居中。

### 外边距

外边距包括`Layout.margins`和`Layout.<top|bottom|left|right>Margin`五个属性，后四个属性如果设置了，会覆盖`margins`属性。

在布局中，只有Layout会实际计算子元素的外边距属性，如果元素的父元素不是Layout，则外边距不纳入布局计算。

### GridLayout

WIP

## anchors

锚点布局，比Layout古早一些，基于`Item`的QML对象都支持。

anchors有四部分内容：
- 锚线（anchor line）：七条布局线
- 边距：anchors也有一套类似的边距系统
- 偏移
- 便捷用法

### 锚线

锚线总共7条，横向4条，纵向3条：

![[Pasted image 20240409144806.png]]

锚线`baseline`没有画出，官方文档说是标示文本方向的基线。

通过元素锚线与其他锚线的绑定，可以实现相对布局：

```
Rectangle {
	...
	Rectangle {
		id: rect1
		anchors.left: parent.left
		...
	}
	Rectangle {
		id: rect2
		anchors.left: rect1.right
		...
	}
}
```

![[Pasted image 20240409145947.png]]

特别地：`anchors.centerIn`表示完全居中，此时目标必须设定为其他元素（而非锚线）。

### 边距

- `anchors.margins`：边距默认值，默认为`0`
- `anchors.topMargin`：上边距
- `anchors.bottomMargin`：下边距
- `anchors.leftMargin`：左边距
- `anchors.rightMargin`：右边距

与Layout边距类似，单向边距的设定会覆盖默认值。

### 偏移值

在锚定的基础上设置偏移，使得元素距离原布局位置偏移特定距离。

- `anchors.horizontalCenterOffset`：水平中心偏移
- `anchors.verticalCenterOffset`：垂直中心偏移
- `anchors.baselineOffset`：基线偏移

### 其他设置

- `anchors.fill`：填充整个元素
- `anchors.centerIn`：中心对准被指定的元素中心
- `anchors.alignWhenCentered`：在对齐时其他锚点位置是否不变，默认为`false`
