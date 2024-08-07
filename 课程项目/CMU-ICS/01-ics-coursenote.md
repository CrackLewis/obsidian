
## ch2-信息的表示和处理

略

## ch3-程序的机器级表示

- 历史观点
- 程序编码
- 数据格式
- 访问信息
- 算术和逻辑操作
- 控制
- 过程
- 数组分配和访问
- 异质的数据结构
- 在机器级程序中将控制与数据结合起来

数据传送指令：`mov[_|z|s][_|b|w|l|q][_|b|w|l|q]`
- `z|s`：零扩展、符号扩展
- `b|w|l|q`：字节、双字节、四字节、八字节
- 源数据长度不能大于目标数据长度

间接传址：`offset(r1, r2, step) = r1 + r2 * step + offset`。

`leaq`：加载一个内存上的有效地址，并将地址结果存储到寄存器。

```
leaq 4(%rax), %rbx
```

`cmp[b|w|l|q]`：右减左，结果用于设置FLAGS

`test[b|w|l|q]`：左右逻辑与，结果用于设置FLAGS

3.10.3 缓冲区溢出漏洞：
- 成因：程序写入的内容可能超出缓冲区的实际容量，导致`ret`指令返回到一个意想不到的地址。攻击者有可能通过刻意构造输入，实现到自定义地址的跳转，执行一些恶意代码。
- 防范措施：
	- 栈地址随机化
	- 栈破坏检测：高版本GCC的做法是，在栈帧中加入一个金丝雀值（canary value），如果函数返回时金丝雀值与原来不同，则认为发生了缓冲区溢出
	- 限制可执行代码区域：非代码段的内容不可执行

3.11 浮点数相关指令：
- 浮点数保存在XMM和YMM寄存器中，其中`%xmm0`和`%ymm0`特别用于存储返回值。
- 大部分的浮点数指令前面都带一个`v`，如`vmovss`、`vmulsd`等。其中最后一位`s`表示单精度，`d`表示双精度。

## ch4-处理器体系结构

4.1、4.2 Y86-64指令集体系结构：参考[[02-ics-labs#Y86-64指令集|这一部分]]的笔记。

### 4.3-处理器顺序实现

指令五阶段：

| 阶段   | 操作                           |     |
| ---- | ---------------------------- | --- |
| 取指   | 根据PC取指令字节，从指令取出指令代码、指令功能和操作数 |     |
| 译码   | 从寄存器文件读取实际的操作数               |     |
| 执行   | ALU进行数值计算、地址计算或栈操作中的一种       |     |
| 访存   | 数据写入或读出内存                    |     |
| 写回   | 数据写入寄存器文件                    |     |
| 更新PC | PC更新为下一条指令地址                 |     |

HCL可能涉及的量：
- `icode`：指令代码
- `ifun`：指令功能
- `rA`、`rB`、`valP`：寄存器编号、PC的新值
- `valA`、`valB`：寄存器的原始值
- `valE`：指令的执行结果

### pipe-full.hcl解读

该文件描述了Y86-64顺序处理器的硬件细节。

指令码的符号表示：

```
wordsig INOP 	'I_NOP'
wordsig IHALT	'I_HALT'
wordsig IRRMOVQ	'I_RRMOVQ'
wordsig IIRMOVQ	'I_IRMOVQ'
wordsig IRMMOVQ	'I_RMMOVQ'
wordsig IMRMOVQ	'I_MRMOVQ'
wordsig IOPQ	'I_ALU'
wordsig IJXX	'I_JMP'
wordsig ICALL	'I_CALL'
wordsig IRET	'I_RET'
wordsig IPUSHQ	'I_PUSHQ'
wordsig IPOPQ	'I_POPQ'
# Instruction code for iaddq instruction
wordsig IIADDQ	'I_IADDQ'
```

处理器状态的符号表示：

```
wordsig SBUB	'STAT_BUB'	# Bubble in stage
wordsig SAOK	'STAT_AOK'	# Normal execution
wordsig SADR	'STAT_ADR'	# Invalid memory address
wordsig SINS	'STAT_INS'	# Invalid instruction
wordsig SHLT	'STAT_HLT'	# Halt instruction encountered
```

根据`stages.h`，程序计数器记录两个属性