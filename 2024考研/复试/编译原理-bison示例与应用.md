
230110：花一天时间研究了O'Reilly出版的《flex与bison》中的一个可编程计算器示例，收获颇多。

## 可编程计算器实例

预期功能：
- 四则运算、取反、绝对值
- 变量赋值
- 用户函数声明、if语句、while语句
- 内置函数和用户函数调用

flex回顾：
- 语法分析过程会不断调用`int yylex(void)`获取下一个单词。这个函数只会返回种别代码，如果要附加信息，则要写`yylval`值。单词识别可附加例程，可使用单词文本（`yytext`）、行号（`yylineno`）、列号（`column`）、词长（`yyleng`）等外部变量。
- `%option`可放在lex开头，`noyywrap`表示为单文件分析，`c++`表示生成c++语言的分析程序，`yylineno`表示使用行号。
- yylval是YYSTYPE类型的，默认为int，如果在yacc里特别声明，可以变为union类型。详见bison细节。

bison的一些实践特性：
- `YYSTYPE`是文法符号的统一属性值，默认为int，这显然不符合实践要求，所以yacc支持通过`%union { ... }`的形式将其设置为多个成员域的union。成员名可用于在`%type`中指明特定文法符号的值赋给哪个域。
- `%token <xx> TOK`声明识别单词TOK后会使用其xx域的值，如不指定则不使用。`%left`、`%right`指定单词的左右结合性，`%nonassoc`则指定单词的相邻（隔不超过一个非终结符）是一种语法错误。单词声明越往后，优先级越高。
- 在文法符号归约例程中，`$$`表示该符号的目标值，`$k`表示产生式右侧第k个文法符号的值。

### rpcalc.h文件

rpcalc.h文件是项目的公共头文件，会被其他所有源文件包含。定义了如下内容：
- 语法结构体：ast、fncall、ufncall、flow、numval、symref、symasgn等，用于构建语法树实体。
- 符号表：这是一个

```c
#ifndef FB_3_2_H_
#define FB_3_2_H_

/* Companion source code for "flex & bison", published by O'Reilly
 * Media, ISBN 978-0-596-15597-1
 * Copyright (c) 2009, Taughannock Networks. All rights reserved.
 * See the README file for license conditions and contact info.
 * $Header: /home/johnl/flnb/code/RCS/fb3-2.h,v 2.1 2009/11/08 02:53:18 johnl
 * Exp $
 */
/*
 * Declarations for a calculator fb3-1
 */

// 符号表项：标识一个变量或用户函数名
struct symbol {
  // 符号的字面名称
  char *name;
  // 若符号为变量，则为其数值
  double value;
  // 若符号为函数，则为其函数表达式
  struct ast *func;
  // 若符号为函数，则为其形参列表
  struct symlist *syms;
};

// 定长的符号哈希表
#define NHASH 9997
struct symbol symtab[NHASH];

// 线性探测法查符号表
struct symbol *lookup(char *);

// 符号列表，作为参数列表（在symbol中作为形参，）
struct symlist {
  struct symbol *sym;
  struct symlist *next;
};

// 在当前符号表之前新增一个符号
struct symlist *newsymlist(struct symbol *sym, struct symlist *next);

// 释放整个符号表
void symlistfree(struct symlist *sl);

/* 结点类型
 *  + - * / | 四则运算、绝对值
 *  '0'-'7' 比较运算符
 *      1:大于 2:小于 3:不等于 4:等于 5:不小于 6:不大于
 *  'M' 取负
 *  'L' 声明列表
 *  'I' if语句
 *  'W' while语句
 *  'N' 符号（变量）引用
 *  '=' 赋值
 *  'S' 符号列表
 *  'F' 内置函数调用
 *  'C' 用户函数调用
 */

// 内置函数，调用math.h库函数
enum bifs { B_sqrt = 1, B_exp, B_log, B_print };

// AST通用模型，12字节（x86）
struct ast {
  int nodetype;
  struct ast *l;
  struct ast *r;
};

// 内置函数调用（Function call）
struct fncall {
  int nodetype;        // 'F'
  struct ast *l;       // 参数列表
  enum bifs functype;  // 内置函数类型
};

// 用户函数调用（function Call）
struct ufncall {
  int nodetype;      // 'C'
  struct ast *l;     // 参数列表
  struct symbol *s;  // 被调用的符号
};

// 过程语句：I（if语句）或W（while语句）
struct flow {
  int nodetype;
  struct ast *cond;  // if或while的条件表达式
  struct ast *tl;    // if:then while:do
  struct ast *el;    // if:else while:null
};

// 字面量结点（K(c)onstant）
struct numval {
  int nodetype;
  double number;
};

// 变量引用（Number reference）
struct symref {
  int nodetype;
  struct symbol *s;
};

// 赋值（=）
struct symasgn {
  int nodetype;
  struct symbol *s;  // 目标变量
  struct ast *v;     // 数值
};

// AST构造函数
struct ast *newast(int nodetype, struct ast *l, struct ast *r);
struct ast *newcmp(int cmptype, struct ast *l, struct ast *r);
struct ast *newfunc(int functype, struct ast *l);
struct ast *newcall(struct symbol *s, struct ast *l);
struct ast *newref(struct symbol *s);
struct ast *newasgn(struct symbol *s, struct ast *v);
struct ast *newnum(double d);
struct ast *newflow(int nodetype, struct ast *cond, struct ast *tl,
                    struct ast *tr);

/* 定义一个用户函数 */
void dodef(struct symbol *name, struct symlist *syms, struct ast *stmts);

// 对AST进行估值
double eval(struct ast *);

// 释放一个语法分析树
void treefree(struct ast *);

// 自定义错误输出
extern int yylineno; /* from lexer */
void yyerror(char *s, ...);

// 打印语法分析树
extern int debug;
void dumpast(struct ast *a, int level);

#endif

```

### rpcalc.l文件

rpcalc.l是词法分析规则文件。