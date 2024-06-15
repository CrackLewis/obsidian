
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

合并2个文本文件，并输出合并结果。

`paste [<options>] <file1> <file2>`

常用选项：
- `-a <文件编号>`：输出特定编号文件中没有参与合并的

## join（WIP）

## wc

## tee

## less

## more

## awk

## sed