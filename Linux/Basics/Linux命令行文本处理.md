
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
2051111 JosephStalin M Shoemaking
2052222 FranklinRoosevelt M Law
2053333 WinstonChurchill M Military
2051234 DeGaulle M Mathematics
2054321 AdolfHitler F Arts
2057777 Hirohito F Economics
2058888 Missuolini F Bakery
```

文件2为如下内容（为测试连接正确性，数据被打乱了）：

```
2051234 France
2054321 Germany
2050001 China
2058888 Italy
2057777 Japan
2051111 SovietUnion
2053333 UK
2052222 USA
```

`join`并不能直接连接这两个文件，因为它们的首个字段是乱序。

## wc

## tee

## less

## more

## awk

## sed