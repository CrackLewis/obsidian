
`const path = require("path");`

path是Node.js官方提供的用于处理路径的模块。

## 路径拼接

`path.join(路径, 路径段1, 路径段2, 路径段3, ...)`

路径段应当是一个完整路径，后面的路径段应当是一个相对路径。
例如：`path.join("/usr/bin", "./libcxx", "../cmake")`的结果为`"/usr/bin/cmake"`。

在Windows下，所有正下环线会转换为反下划线。

路径拼接应尽可能使用`path.join`方法，而不是使用字符串拼接的方法。

## 获取路径中的文件名

`path.basename(路径字符串)`
可以输出一个文件路径中，属于文件名的部分。

`path.basename(路径字符串, 扩展名串)`
可以输出一个文件路径中，属于文件名的部分，区别在于无指定的扩展名。

## 获取路径中的文件扩展名

`path.extname(路径字符串)`
可以获取文件路径中的文件扩展名部分。

## 案例：提取HTML文件中的内联样式和脚本

步骤：
- 利用`path.dirname`获取HTML文件的目录，进一步确定输出样式和JS脚本的位置。
- 用`fs.readFile`方法读取全文
- 用正则表达式匹配HTML全文中的`<script>`和`<style>`块
- 将被匹配的内容的标签去除，将其余内容写到输出样式文件和JS文件中

注意点：
- `fs.writeFile`方法只能用来创建文件，不能用来创建路径
- `fs.writeFile`会覆盖旧文件中的内容

## 其他方法

`path.parse(路径)`：会解析一个路径，结果以对象`pathObject`的形式返回

`path.delimiter`：当前环境所用的地址间分隔符，Windows为`;`，POSIX为`:`。

`path.sep`：当前环境所用的路径级别分隔符，Windows为`\`，POSIX为`/`。

`path.dirname(路径)`：会返回一个文件路径的路径名

`path.format(pathObject)`：将一个`pathObject`转换为路径串

`path.isAbsolute(路径)`：一个路径是否为绝对路径

`path.relative(路径A, 路径B)`：返回B相对于A的相对地址

其他参考[Path](https://nodejs.org/dist/latest-v18.x/docs/api/path.html) 。