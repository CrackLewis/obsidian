
参考资料：
- [GNU Bison 手册](https://www.gnu.org/software/bison/manual/bison.pdf)
- [知乎专栏-Lex与YACC详解](https://zhuanlan.zhihu.com/p/143867739)
- [Bison博客](https://blog.csdn.net/weixin_46222091/article/details/105990745)
- tbc.

230110：花一天时间研究了O'Reilly出版的《flex与bison》中的一个可编程计算器示例，收获颇多。

## bison规则与设施

### 声明

- `%token`、`%left`、`%right`、`%nonassoc`、`%precedence`
- `%start`
- `%union`
- `%type`：声明文法符号使用哪个union的成员域、或哪种返回类型
- `%name-prefix`：会改变内置成员前缀，如yylex改为rpcalclex等。
- `%initial-action`：执行一些初始动作。
- `%parse-param`：设置yyparse函数的参数，默认为空。

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
- 语法结构创建函数：动态创建语法结构的函数集，被yacc的生成程序调用。
- 符号表：线性探测散列表，用于维护变量和用户函数两种用户符号。
- 功能函数

```c
#ifndef FB_3_2_H_
#define FB_3_2_H_

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

rpcalc.l是词法分析规则文件，flex会读rpcalc.l并生成rpcalc.lex.c。rpcalc.l标识了各种可被识别的单词种别及它们的识别行为。

本项目的rpcalc.l由于替换了YYSTYPE类型，所以需要手动包含rpcalc.tab.h头文件。

```
%option noyywrap nodefault yylineno
%{
# include "rpcalc.h"
# include "rpcalc.tab.h"
%}

/* 浮点数的指数部分 */
EXP	([Ee][-+]?[0-9]+)

%%
 /* 单字符运算符 */
"+" |
"-" |
"*" |
"/" |
"=" |
"|" |
"," |
";" |
"(" |
")"     { return yytext[0]; }

 /* 比较运算符 */
">"     { yylval.fn = 1; return CMP; }
"<"     { yylval.fn = 2; return CMP; }
"<>"    { yylval.fn = 3; return CMP; }
"=="    { yylval.fn = 4; return CMP; }
">="    { yylval.fn = 5; return CMP; }
"<="    { yylval.fn = 6; return CMP; }

 /* 关键字 */
"if"    { return IF; }
"then"  { return THEN; }
"else"  { return ELSE; }
"while" { return WHILE; }
"do"    { return DO; }
"let"   { return LET;}

 /* 内置函数 */
"sqrt"  { yylval.fn = B_sqrt; return FUNC; }
"exp"   { yylval.fn = B_exp; return FUNC; }
"log"   { yylval.fn = B_log; return FUNC; }
"print" { yylval.fn = B_print; return FUNC; }

 /* 调试开关设置 */
"debug"[0-9]+ { debug = atoi(&yytext[5]); printf("debug set to %d\n", debug); }

 /* 标识符 */
[a-zA-Z][a-zA-Z0-9]*  { yylval.s = lookup(yytext); return NAME; }

[0-9]+"."[0-9]*{EXP}? |
"."?[0-9]+{EXP}? { yylval.d = atof(yytext); return NUMBER; }

"//".*  /* 注释忽略 */
[ \t]   /* 空白字符忽略 */ 
\\\n    printf("c> "); /* 换行忽略 */
"\n"    { return EOL; }

/* 错误处理：注意yyerror调用的是自定义的增强版 */
.	{ yyerror("Mystery character %c\n", *yytext); }
%%

```

### rpcalc.y文件

rpcalc.y文件是语法分析规则文件，bison会根据此文件生成rpcalc.tab.c和rpcalc.tab.h。

文件定义了如下内容：
- `YYSTYPE`的类型为union，以及union有哪些成员。
- 语法分析器接受哪些单词，单词的优先级和结合性属性，这些单词会使用`YYSTYPE`的哪个域（可选）。
- 语法符号会使用`YYSTYPE`的哪个域（可选，见`%type`）。
- 所有语法规则，以及规则对应的例程。

main函数定义不在该文件，在文件rpcalc_funcs.c中。

```
%{
#  include <stdio.h>
#  include <stdlib.h>
#  include "rpcalc.h"
%}

%union {
  struct ast *a;
  double d;
  struct symbol *s;		/* 符号（变量或用户函数） */
  struct symlist *sl;
  int fn;			/* 内置函数标号或比较运算符标号 */
}

/* 单词类别声明 */
%token <d> NUMBER
%token <s> NAME
%token <fn> FUNC
%token EOL

%token IF THEN ELSE WHILE DO LET


%nonassoc <fn> CMP
%right '='
%left '+' '-'
%left '*' '/'
%nonassoc '|' UMINUS

%type <a> exp stmt list explist
%type <sl> symlist

%start calclist

%%

stmt: IF exp THEN list           { $$ = newflow('I', $2, $4, NULL); }
   | IF exp THEN list ELSE list  { $$ = newflow('I', $2, $4, $6); }
   | WHILE exp DO list           { $$ = newflow('W', $2, $4, NULL); }
   | exp
;

list: /* nothing */ { $$ = NULL; }
   | stmt ';' list { if ($3 == NULL)
	                $$ = $1;
                      else
			$$ = newast('L', $1, $3);
                    }
   ;

exp: exp CMP exp          { $$ = newcmp($2, $1, $3); }
   | exp '+' exp          { $$ = newast('+', $1,$3); }
   | exp '-' exp          { $$ = newast('-', $1,$3);}
   | exp '*' exp          { $$ = newast('*', $1,$3); }
   | exp '/' exp          { $$ = newast('/', $1,$3); }
   | '|' exp              { $$ = newast('|', $2, NULL); }
   | '(' exp ')'          { $$ = $2; }
   | '-' exp %prec UMINUS { $$ = newast('M', $2, NULL); }
   | NUMBER               { $$ = newnum($1); }
   | FUNC '(' explist ')' { $$ = newfunc($1, $3); }
   | NAME                 { $$ = newref($1); }
   | NAME '=' exp         { $$ = newasgn($1, $3); }
   | NAME '(' explist ')' { $$ = newcall($1, $3); }
;

explist: exp
 | exp ',' explist  { $$ = newast('L', $1, $3); }
;
symlist: NAME       { $$ = newsymlist($1, NULL); }
 | NAME ',' symlist { $$ = newsymlist($1, $3); }
;

calclist: /* nothing */
  | calclist stmt EOL {
    if(debug) dumpast($2, 0);
     printf("= %4.4g\n> ", eval($2));
     treefree($2);
    }
  | calclist LET NAME '(' symlist ')' '=' list EOL {
                       dodef($3, $5, $8);
                       printf("Defined %s\n> ", $3->name); }

  | calclist error EOL { yyerrok; printf("> "); }
 ;
%%

```

### rpcalc_funcs.c文件

该文件提供了rpcalc.h中函数定义的对应实现和main函数的实现。

```c
#include <math.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "rpcalc.h"

/* 对符号计算散列值 */
static unsigned symhash(char *sym) {
  unsigned int hash = 0;
  unsigned c;
  while (c = *sym++) hash = hash * 9 ^ c;
  return hash;
}

/* 查符号散列表，查不到就尝试新增一个表项 */
struct symbol *lookup(char *sym) {
  struct symbol *sp = &symtab[symhash(sym) % NHASH];
  int scount = NHASH; /* 查找计数 */

  while (--scount >= 0) {
    if (sp->name && !strcmp(sp->name, sym)) {
      return sp;
    }
    if (!sp->name) { /* 当前为空，登记为新表项 */
      sp->name = strdup(sym);
      sp->value = 0;
      sp->func = NULL;
      sp->syms = NULL;
      return sp;
    }
    if (++sp >= symtab + NHASH) sp = symtab; /* 非空且不匹配，跳为下一个表项 */
  }
  yyerror("symbol table overflow\n");
  abort(); /* 查了一轮还没，寄 */
}

struct ast *newast(int nodetype, struct ast *l, struct ast *r) {
  struct ast *a = malloc(sizeof(struct ast));
  if (!a) {
    yyerror("out of space");
    exit(0);
  }
  a->nodetype = nodetype;
  a->l = l;
  a->r = r;
  return a;
}

struct ast *newnum(double d) {
  struct numval *a = malloc(sizeof(struct numval));
  if (!a) {
    yyerror("out of space");
    exit(0);
  }
  a->nodetype = 'K';
  a->number = d;
  return (struct ast *)a;
}

struct ast *newcmp(int cmptype, struct ast *l, struct ast *r) {
  struct ast *a = malloc(sizeof(struct ast));
  if (!a) {
    yyerror("out of space");
    exit(0);
  }
  a->nodetype = '0' + cmptype;
  a->l = l;
  a->r = r;
  return a;
}

struct ast *newfunc(int functype, struct ast *l) {
  struct fncall *a = malloc(sizeof(struct fncall));
  if (!a) {
    yyerror("out of space");
    exit(0);
  }
  a->nodetype = 'F';
  a->l = l;
  a->functype = functype;
  return (struct ast *)a;
}

struct ast *newcall(struct symbol *s, struct ast *l) {
  struct ufncall *a = malloc(sizeof(struct ufncall));
  if (!a) {
    yyerror("out of space");
    exit(0);
  }
  a->nodetype = 'C';
  a->l = l;
  a->s = s;
  return (struct ast *)a;
}

struct ast *newref(struct symbol *s) {
  struct symref *a = malloc(sizeof(struct symref));
  if (!a) {
    yyerror("out of space");
    exit(0);
  }
  a->nodetype = 'N';
  a->s = s;
  return (struct ast *)a;
}

struct ast *newasgn(struct symbol *s, struct ast *v) {
  struct symasgn *a = malloc(sizeof(struct symasgn));
  if (!a) {
    yyerror("out of space");
    exit(0);
  }
  a->nodetype = '=';
  a->s = s;
  a->v = v;
  return (struct ast *)a;
}

struct ast *newflow(int nodetype, struct ast *cond, struct ast *tl,
                    struct ast *el) {
  struct flow *a = malloc(sizeof(struct flow));
  if (!a) {
    yyerror("out of space");
    exit(0);
  }
  a->nodetype = nodetype;
  a->cond = cond;
  a->tl = tl;
  a->el = el;
  return (struct ast *)a;
}

struct symlist *newsymlist(struct symbol *sym, struct symlist *next) {
  struct symlist *sl = malloc(sizeof(struct symlist));
  if (!sl) {
    yyerror("out of space");
    exit(0);
  }
  sl->sym = sym;
  sl->next = next;
  return sl;
}

void symlistfree(struct symlist *sl) {
  struct symlist *nsl;
  while (sl) {
    nsl = sl->next;
    free(sl);
    sl = nsl;
  }
}

/* 用户自定义函数，syms为形参，func为函数体 */
void dodef(struct symbol *name, struct symlist *syms, struct ast *func) {
  if (name->syms) symlistfree(name->syms);
  if (name->func) treefree(name->func);
  name->syms = syms;
  name->func = func;
}

static double callbuiltin(struct fncall *);
static double calluser(struct ufncall *);

double eval(struct ast *a) {
  double v;

  if (!a) {
    yyerror("internal error, null eval");
    return 0.0;
  }

  switch (a->nodetype) {
      /* constant */
    case 'K':
      v = ((struct numval *)a)->number;
      break;

      /* name reference */
    case 'N':
      v = ((struct symref *)a)->s->value;
      break;

      /* assignment */
    case '=':
      v = ((struct symasgn *)a)->s->value = eval(((struct symasgn *)a)->v);
      break;

      /* expressions */
    case '+':
      v = eval(a->l) + eval(a->r);
      break;
    case '-':
      v = eval(a->l) - eval(a->r);
      break;
    case '*':
      v = eval(a->l) * eval(a->r);
      break;
    case '/':
      v = eval(a->l) / eval(a->r);
      break;
    case '|':
      v = fabs(eval(a->l));
      break;
    case 'M':
      v = -eval(a->l);
      break;

      /* comparisons */
    case '1':
      v = (eval(a->l) > eval(a->r)) ? 1 : 0;
      break;
    case '2':
      v = (eval(a->l) < eval(a->r)) ? 1 : 0;
      break;
    case '3':
      v = (eval(a->l) != eval(a->r)) ? 1 : 0;
      break;
    case '4':
      v = (eval(a->l) == eval(a->r)) ? 1 : 0;
      break;
    case '5':
      v = (eval(a->l) >= eval(a->r)) ? 1 : 0;
      break;
    case '6':
      v = (eval(a->l) <= eval(a->r)) ? 1 : 0;
      break;

    /* if语句：else子句和then子句都可以为空，这时取默认值。可以假定子句必是空、赋值、表达式、if、while、语句列表中的一种 */
    case 'I':
      if (eval(((struct flow *)a)->cond) != 0) {
        if (((struct flow *)a)->tl) {
          v = eval(((struct flow *)a)->tl);
        } else
          v = 0.0; /* 默认值 */
      } else {
        if (((struct flow *)a)->el) {
          v = eval(((struct flow *)a)->el);
        } else
          v = 0.0; /* a default value */
      }
      break;

    /* while语句：do子句可以为空，此时取默认值。 */
    case 'W':
      v = 0.0; /* a default value */

      if (((struct flow *)a)->tl) {
        while (eval(((struct flow *)a)->cond) != 0)
          v = eval(((struct flow *)a)->tl);
      }
      break; /* last value is value */

    case 'L':
      eval(a->l);
      v = eval(a->r); // 语句列表的值取最后一个语句的值
      break;

    case 'F':
      v = callbuiltin((struct fncall *)a);
      break;

    case 'C':
      v = calluser((struct ufncall *)a);
      break;

    default:
      printf("internal error: bad node %c\n", a->nodetype);
  }
  return v;
}

static double callbuiltin(struct fncall *f) {
  enum bifs functype = f->functype;
  double v = eval(f->l);

  switch (functype) {
    case B_sqrt:
      return sqrt(v);
    case B_exp:
      return exp(v);
    case B_log:
      return log(v);
    case B_print:
      printf("= %4.4g\n", v);
      return v;
    default:
      yyerror("Unknown built-in function %d", functype);
      return 0.0;
  }
}

// 用户函数调用
static double calluser(struct ufncall *f) {
  struct symbol *fn = f->s; /* 用户函数符号 */
  struct symlist *sl;       /* 形参 */
  struct ast *args = f->l;  /* 实参 */
  double *oldval, *newval;  /* 暂存参数值 */
  double v;
  int nargs;
  int i;

  if (!fn->func) { // 调用未定义函数
    yyerror("call to undefined function", fn->name);
    return 0;
  }

  /* 数参数 */
  sl = fn->syms;
  for (nargs = 0; sl; sl = sl->next) nargs++;

  /* 开辟空间，存储参数值 */
  oldval = (double *)malloc(nargs * sizeof(double));
  newval = (double *)malloc(nargs * sizeof(double));
  if (!oldval || !newval) {
    yyerror("Out of space in %s", fn->name);
    return 0.0;
  }

  /* 对实参进行估值 */
  for (i = 0; i < nargs; i++) {
    if (!args) {
      yyerror("too few args in call to %s", fn->name);
      free(oldval);
      free(newval);
      return 0;
    }

    if (args->nodetype == 'L') { // 根据语法规则，左子树为实参，右子树为列表
      newval[i] = eval(args->l);
      args = args->r;
    } else { // 剩余单个结点则说明，这是最后一个结点
      newval[i] = eval(args);
      args = NULL;
    }
  }

  /* 把旧形参的值暂时存起来（可能是因为外部会修改形参），赋予新值 */
  sl = fn->syms;
  for (i = 0; i < nargs; i++) {
    struct symbol *s = sl->sym;

    oldval[i] = s->value;
    s->value = newval[i];
    sl = sl->next;
  }

  free(newval);

  /* 进行估值 */
  v = eval(fn->func);

  /* 把旧形参的值写回去 */
  sl = fn->syms;
  for (i = 0; i < nargs; i++) {
    struct symbol *s = sl->sym;

    s->value = oldval[i];
    sl = sl->next;
  }

  free(oldval);
  return v;
}

void treefree(struct ast *a) {
  switch (a->nodetype) {
      /* two subtrees */
    case '+':
    case '-':
    case '*':
    case '/':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case 'L':
      treefree(a->r);

      /* one subtree */
    case '|':
    case 'M':
    case 'C':
    case 'F':
      treefree(a->l);

      /* no subtree */
    case 'K':
    case 'N':
      break;

    case '=':
      free(((struct symasgn *)a)->v);
      break;

    case 'I':
    case 'W':
      free(((struct flow *)a)->cond);
      if (((struct flow *)a)->tl) free(((struct flow *)a)->tl);
      if (((struct flow *)a)->el) free(((struct flow *)a)->el);
      break;

    default:
      printf("internal error: free bad node %c\n", a->nodetype);
  }

  free(a); /* always free the node itself */
}

void yyerror(char *s, ...) {
  va_list ap;
  va_start(ap, s);

  fprintf(stderr, "%d: error: ", yylineno);
  vfprintf(stderr, s, ap);
  fprintf(stderr, "\n");
}

int main() {
  printf("> ");
  return yyparse();
}

/* debugging: dump out an AST */
int debug = 0;
void dumpast(struct ast *a, int level) {
  printf("%*s", 2 * level, ""); /* 2L格缩进 */
  level++;

  if (!a) {
    printf("NULL\n");
    return;
  }

  switch (a->nodetype) {
      /* constant */
    case 'K':
      printf("number %4.4g\n", ((struct numval *)a)->number);
      break;

      /* name reference */
    case 'N':
      printf("ref %s\n", ((struct symref *)a)->s->name);
      break;

      /* assignment */
    case '=':
      printf("= %s\n", ((struct symref *)a)->s->name);
      dumpast(((struct symasgn *)a)->v, level);
      return;

      /* expressions */
    case '+':
    case '-':
    case '*':
    case '/':
    case 'L':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
      printf("binop %c\n", a->nodetype);
      dumpast(a->l, level);
      dumpast(a->r, level);
      return;

    case '|':
    case 'M':
      printf("unop %c\n", a->nodetype);
      dumpast(a->l, level);
      return;

    case 'I':
    case 'W':
      printf("flow %c\n", a->nodetype);
      dumpast(((struct flow *)a)->cond, level);
      if (((struct flow *)a)->tl) dumpast(((struct flow *)a)->tl, level);
      if (((struct flow *)a)->el) dumpast(((struct flow *)a)->el, level);
      return;

    case 'F':
      printf("builtin %d\n", ((struct fncall *)a)->functype);
      dumpast(a->l, level);
      return;

    case 'C':
      printf("call %s\n", ((struct ufncall *)a)->s->name);
      dumpast(a->l, level);
      return;

    default:
      printf("bad %c\n", a->nodetype);
      return;
  }
}
```

## SysY

SysY是北京大学编译原理课程的教学用语言。

详情参考：[网页](https://pku-minic.github.io/online-doc/#/lv1-main/lexer-parser?id=cc-%e5%ae%9e%e7%8e%b0)

这个用例提供了一种生成C++语言分析程序的思路，比较前卫。