
cat
grep、ag
sort、uniq
cut、paste、join
wc
tee
awk、sed
less、more

## cat

输出文件内容。

格式：`cat [<options>] [<files>]`

常用选项：
- `-n`：输出行号。
- `-s`：省略重复的空行。（squeeze）
- `-t`：将制表符显示为`^T`。（tab）
- `-e`：行末加美元符号。

## grep

GREP=Globally search a Regular Expression and Print

格式：`grep [<options>] <pattern> [<files>]`
- `pattern`：要查找的字符串或正则表达式。
- `files`：如有则为文件名对应的文件，否则为标准输入流。

常用选项：
- `-i`：忽略大小写
- `-v`：反向查找，只打印不匹配的行
- `-n`：显示行号
- `-r`：递归查找子目录内的文件
- `-l`：只打印匹配的文件名
- `-c`：只打印匹配的行数
- `-o`：只输出匹配的部分，而非输出整行

示例（转义符显示有些诡异，建议拷贝）：

```bash
# 检查并输出有至少3位连续数字的行
$ grep '[0-9]\{3,\}'
```

## ag

ag是一个代码搜索工具。Linux默认不提供，需要通过安装`silversearcher-ag`使用。

格式：`ag <pattern> [<dir>]`，表示在路径`dir`的所有源码文件中搜索符合`pattern`的文件。

## sort

内置排序工具。读取文件并将所有记录排序。

格式：`sort [<options>] [<files>]`。
- 默认行为：读stdin的记录并按*字典序*升序排列。
- `files`：各文件路径。如空则为stdin。

常用选项：
- `-b`：忽略前置空格（ignore leading Blanks）
- `-c`：只检查是否为正序，不排序。（Check）
- `-M`：按月份名称次序排序，如：JAN、FEB、MAR等。
- `-n`：按数字方式排序。
- `-R`：乱序排序。（`sort -R 1.txt`等价于`shuf 1.txt`）
- `-r`：逆序排序。
- `-m`：只归并各个文件的记录，不排序。
- `-k <列号>[.<列内起始位置>]`：指定某一列为关键字，下标为1。
- `-o <输出文件路径>`：写输出到特定文件。

示例：

```bash
# 文件第二列按数字升序排序
$ sort -nk2 file.txt
# 先按第一列顺序排序，对第一列相同的，第二列按数字方式排序
$ sort -k1,1 -k2,2n file.txt
```

## uniq

uniq(ue)：文件按行去重

`uniq [<options>] [<inputs>] [<outputs>]`

opts:
- `-c`：（`--count`）在每行首部显示该行重复次数
- `-d`：（`--repeated`）只显示有重复的行
- `-u`：（`--unique`）只显示不重复的行
- `-i`：（`--ignore-case`）忽略大小写差异
- `-f <字段数>`：（`--skip-fields=<字段数>`）忽略比较每行的前若干个字段
- `-s <字符数>`：（`--skip-chars=<字符数>`）忽略比较每行的前若干个字符
- `-w <字符数>`：（`--check-chars=<字符数>`）只比较每行的前若干个字符

## cut

从文件的每一行提取特定内容输出。

`cut [<options>] [<files>]`

常用选项：
- `-b <提取的字节编号>`：提取每行特定位置的字节，如`-b 1-5,11-15,21-25`。
- `-c <提取的列编号>`：提取每行特定的某几列，如`-c 1-2,4-6`。
- `-d <分隔符>`：自定义源文件分隔符，默认为tab。
- `-f <提取的字段编号>`：和`-d`配合使用，表示提取每行特定的某几个字段。

## paste

合并数个文本文件，并输出合并结果。

`paste [<options>] <files>`

常用选项：
- `-d <分隔符列表>`：（delimiters）指定分隔每一行的所有合法分隔符。默认为只有tab。
- `-s`：（serial）按顺序而非并行合并。类似于*矩阵转置*，每一行代表一个原始文件。
- `-z`：（zero-terminated）指定\\0为行结束符，而非换行符，这样可以处理含换行符的文件。

示例：

```bash
# 以逗号为分隔符合并1.csv和2.csv，并输出结果
$ paste -d "," 1.csv 2.csv
```

## join

连接2个文本文件，并输出合并结果。注意和`paste`的区别。

`join [<options>] <file1> <file2>`

常用选项：
- `-a <文件编号>`：输出特定编号文件中没有匹配字段的行，类似数据库的左右连接。
- `-e <缺省值>`：如果输出没有匹配字段的行，使用什么缺省值。
- `-i`：忽略大小写差异。
- `-j <字段号>`：相当于`-1 <字段号> -2 <字段号>`，指定两个文件使用哪个字段连接。
- `-o <格式>`：根据指定格式输出。
- `-t <字符>`：使用字符作为输入和输出的分隔符，默认为空格。
- `-v <文件编号>`：只输出特定编号文件中没有匹配字段的行。
	- 注意和`-a`相比，它不输出有匹配字段的行。
- `-1 <字段号>`：指定文件1使用哪些字段连接
- `-2 <字段号>`：指定文件2使用哪些字段连接

示例：例如文件1为如下内容：

```
2050001 MaoZedong M Marxism
2050789 ChiangKaiShek M Finance
2051111 JosephStalin M Shoemaking
2051234 DeGaulle M Mathematics
2052222 FranklinRoosevelt M Law
2053333 WinstonChurchill M Military
2054321 AdolfHitler F Arts
2057777 Hirohito F Economics
2058888 Missuolini F Bakery
```

文件2为如下内容（为测试连接正确性，数据中加入了无关项，并删除了第7行的一个字段）：

```
2050001 China
2050987 India
2051111 SovietUnion
2051234 France
2052222 USA
2053333 UK
2054321 
2057777 Japan
2058888 Italy
```

`join 1.txt 2.txt`输出了8行，可以看出洗头佬没国籍：

```
2050001 MaoZedong M Marxism China
2051111 JosephStalin M Shoemaking SovietUnion
2051234 DeGaulle M Mathematics France
2052222 FranklinRoosevelt M Law USA
2053333 WinstonChurchill M Military UK
2054321 AdolfHitler F Arts
2057777 Hirohito F Economics Japan
2058888 Missuolini F Bakery Italy
```

`join -e ??? 1.txt 2.txt`输出了8行，这时洗头佬国籍变成问号了：

```
2050001 MaoZedong M Marxism China
2051111 JosephStalin M Shoemaking SovietUnion
2051234 DeGaulle M Mathematics France
2052222 FranklinRoosevelt M Law USA
2053333 WinstonChurchill M Military UK
2054321 AdolfHitler F Arts ???
2057777 Hirohito F Economics Japan
2058888 Missuolini F Bakery Italy
```

`join -a 2 -e ??? 1.txt 2.txt`的输出结果则略显诡异。输出共9行，但第二行没有补充未匹配字段。这是因为，如果整个匹配记录缺失，则是不会补项的，只有匹配且残缺才会补上缺省值：

```
2050001 MaoZedong M Marxism China
2050987 India
2051111 JosephStalin M Shoemaking SovietUnion
2051234 DeGaulle M Mathematics France
2052222 FranklinRoosevelt M Law USA
2053333 WinstonChurchill M Military UK
2054321 AdolfHitler F Arts ???
2057777 Hirohito F Economics Japan
2058888 Missuolini F Bakery Italy
```

## split(WIP)

## comm(WIP)

## head(WIP)

## wc

文件统计工具，可统计一个文本文件的行数、单词数和字符数。

`wc [<options>] [<files>]`

常用参数：
- `-c`（`--bytes`、`--chars`）：只显示字符数。
- `-l`（`--lines`）：只显示行数。
- `-w`（`--words`）：只显示单词数。

默认参数下，会在文件名前显示3个数，依次为行数、单词数、字符数。

```
lewislee@CrackLewis:~/lol$ wc 1.txt
  9  36 277 1.txt
```

## tee

捕获标准输入，并写入到标准输出和（0或多个）文件中。

`tee [<options>] [<files>]`

常用参数：
- `-a`（`--append`）：附加到既有文件的后面，而非覆盖，类似`>>`。
- `-i`（`--ignore-interrupts`）：忽略中断信号。

## awk

参考资料：
- [awk官方手册](https://www.gnu.org/software/gawk/manual/gawk.html)
- [blog1](https://bashcommandnotfound.cn/article/linux-awk-command)
- [blog2](https://blog.csdn.net/Lucien010230/article/details/114854014)
- [runoob awk](https://www.runoob.com/linux/linux-comm-awk.html)

From blog：awk是一种强大的文本处理工具，它可以对文本文件或标准输入进行分析和处理，按照指定的规则或模式进行匹配、过滤、替换、计算等操作，生成格式化的文本或报表。

`awk [<options>] <command> [<file>]`
- `options`：控制awk行为的参数选项
- `command`：awk指令，格式为`'[<condition>] { <action> }'`
	- `condition`：可选。可以是一个regex、关系表达式或一个逻辑表达式，用于匹配输入文本的某些行或字段。
	- `action`：awk脚本，可以是打印、赋值、分支、循环、计算等语句。默认行为为打印匹配行。
- `file`：输入awk的文件，默认为stdin。

流程：逐行读取文件，对文件每一行的每一字段执行一次指令。指令包含匹配模式和动作，如果模式匹配成功则执行对应动作。

常用选项：
- `-F <分隔符>`：指定输入文件分隔符，默认为空格或tab。
- `-v <变量>=<初始值>`：自定义用户变量。
- `-f <文件>`：从文件中读取awk脚本。
- `-m[fr] <阈值>`：设置awk脚本使用的程序内存阈值。
	- `-mf <阈值>`：设置记录数上限。
	- `-mr <阈值>`：设置记录大小上限。
- `-W <选项>`：指定兼容模式或警告级别，选项包括posix、gnu、traditional、old、warn、nowarn等。

### awk内建变量

内建变量是一类可以直接使用的变量，有特殊的含义。

常用内建变量：
- `FS`：列分隔符。作用与`-F`相同。
- `NF`：当前处理的行的字段个数。
- `NR`：当前处理的行的行号。
- `$0`：当前处理行的整行内容
- `$1`、`$2`、...、`$n`：当前处理行的第n个字段
- `FILENAME`：当前处理文件的文件名
- `RS`：行分隔符。默认为LF。

### awk基本语法

具体的细节参考官方手册。

跳过一行的指令为`getline`，输出的指令为`print`。

在所有匹配行为之前执行的指令需要置于`BEGIN`内，所有匹配之后执行的指令需要置于`END`内。

`if-else`、`for`、`while`语句和JavaScript、C中的对应语句比较类似。

变量无须定义，直接赋值即可。

基本运算符规则相似，`^`表示幂运算。

awk数组与其它语言的字典比较相似，也不需要定义：
- 可以用`array_name[idx]=val`的方式插入或修改项。
- 可以用`delete array_name[idx]`的方式删除项。
- awk不直接支持嵌套数组，但可以用间接嵌套等方式模拟。
- 可以通过`for(ele in array_name)`的方式遍历。

awk允许自定义函数：

```awk
function find_max(num1, num2) {
	if(num1>num2) return num1
	return num2
}
```

awk自身也提供一些[内建函数](https://www.runoob.com/w3cnote/awk-built-in-functions.html)：
- 数学函数：三角函数、指数、对数等
- 浮点数处理：`int`取整、`rand`随机、`srand`设置随机种子，等等
- 字符串处理：`gsub`全局替换、`sub`单次替换、`length`、`substr`等

如果一个awk脚本需要使用多次，可以考虑存储到本地文件，通过`-f`参数复用。

### awk用例

打印`/etc/passwd`文件的倒数第三列和倒数第一列：

```bash
$ awk -F ':' '{print $(NF-2),$NF}' /etc/passwd
```

统计`/etc/passwd`文件中ID大于666的用户数量：

```bash
$ awk -F ':' '$3>666 {count++} END {print count}' /etc/passwd
```

从`file.txt`文件中提取IP地址并去重：

```bash
$ awk '{for(i=1;i<=NF;i++) if($i~/^[0-9.]+$/) a[$i]++} END {for(i in a) print i}' file.txt
```

格式化输出：

```bash
$ awk '{printf "%-10s %-10s\n", $1, $2}' file
```

### awk注意事项

awk更倾向于对每一行的每个字段进行处理，而后面介绍的sed则倾向于对整行进行处理。

WIP

## sed

sed=Stream EDitor，流编辑器

sed vs vim：sed没有图形界面。

sed vs awk：sed可以较方便地进行实际的文本编辑。

`sed [<options>] [<script>] [<file>]`

常用选项：
- `-e <脚本>`：在命令行中指定一个或多个指令
- `-f <脚本文件>`：指定一个包含指令的脚本文件
- `-i`：修改并保存文件
- `-n`：不输出模式空间的内容
- `-r`：使用扩展正则表达式
- `-s`：将多个文件视为一个文件处理

### sed指令

sed指令一般作用于一行：

```
a\text : 在当前行后追加文本text
c\text : 用text替换当前行
d : 删除当前行
i\text : 在当前行开头插入文本text
p : 打印当前行
q : 退出sed
r file : 读取文件并将内容插入到当前行后面
s/old/new/ : 将行内的old替换为new
w file : 将当前行写入文件
y/src/dest/ : 将源字符集中的字符替换为目标字符集中的字符
```

sed快捷键：
- `&`：代表上一个替换指令中匹配到的字符串   
- \\\\1,\\2,...：代表上一个替换指令中匹配到的第一个、第二个...子表达式  
- `g`：在替换指令中表示对所有匹配项进行替换，而不是只替换第一个  
- `i,I`：在替换指令中表示忽略大小写  
- `w,W`：在替换指令中表示只匹配单词

### sed用例

将文件的第一处`debug`替换为`release`，并保存文件：

```bash
$ sed -i 's/debug/release/' main.cpp
```

在后加`g`表示全文替换：

```bash
$ sed -i 's/debug/release/g' main.cpp
```

按顺序执行多个sed指令：

```bash
$ sed -i -e 's/hello/world/g' -e 's/ell/lle/g' main.cpp
```

sed指令前可以放一个模式，表示只有在整行匹配某种模式时，才执行指令。模式可以是数字，表示行号；或者是正则表达式。例如这条指令用于删除空行：

```bash
$ sed '/^$/d' input.txt > input_stripped_empty_lines.txt
```

sed模式也可以是扩展正则表达式。扩展正则表达式允许用 \\\<数字\>的方式顺序访问被匹配的子表达式：

```bash
$ sed -r 's/([0-9]+) ([a-z]+)/\2 \1/' input.txt > output.txt
```

通过数个sed命令管道结合，可以实现一些高级功能，例如给文件加行号：

```bash
$ sed '=' input.txt | sed 'N;s/\n/ /' > output.txt
```

字符集替换最常用于替换大小写字母：

```bash
$ sed 'y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/' input.txt > output.txt
```

如果需要复用sed指令，可以考虑存储在文件中：

```bash
$ sed -e my_sed_comm.sed 1.txt
```

### awk注意事项

- sed命令有很多指令和选项，如果不熟悉，可以使用man sed或info sed来查看帮助信息。
- sed命令支持基本正则表达式（BRE）和扩展正则表达式（ERE），可以用-r选项来切换。
- sed命令可以使用地址来选择要处理的行，地址可以是数字、正则表达式或范围。
- sed命令可以使用模式空间和保持空间来存储和操作文本，可以使用n,N,d,D,g,G,h,H,p,P等指令来控制它们。