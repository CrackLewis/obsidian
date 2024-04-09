
做毕设时遇到了一些玄学问题，感觉有必要认真研究一下QML布局问题。

## Layout

`import QtQuick.Layouts 1.xx`

是QML内置的一类布局对象，为子成员提供布局相关的属性。

在1.12中，Layout对象有三类：`GridLayout`、`RowLayout`、`ColumnLayout`。

Layout对象为其所有子孙成员提供如下属性：
- `Layout.alignment`：成员在Layout内的对齐方式
- `Layout.<minimum|preferred|maximum>Width`：最小、推荐和最大宽度
- `Layout.<minimum|preferred|maximum>Height`：最小、推荐和最大高度
- `Layout.<top|bottom|left|right>Margin`：上下左右的外边界宽度
- `Layout.margins`：
- `Layout.row`：（限GridLayout）指定在网格中的行号，从0开始
- `Layout.column`：（限GridLayout）指定在网格中的列号，从0开始
- `Layout.rowSpan`：（限GridLayout）行间距
- `Layout.columnSpan`：（限GridLayout）列间距
- `Layout.fillWidth`：是否
- `Layout.fillHeight`：是否