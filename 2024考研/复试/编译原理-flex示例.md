
flex安装：
```bash
$ sudo apt install flex
```

ansic提供的lex要和yacc配合使用。详见bison示例。

下面是一个可供演示的flex用例，命名为`c.lex`：
（转载自[csdn博客](https://blog.csdn.net/NKU_Yang/article/details/109549514)）

```lex
%top{
#include<math.h>
#include<string.h>
}

%{
#define VOID 1
#define CHAR 2
#define INT  3
#define SIZEOF 4
#define CONST 5
#define RETURN 6
#define CONTINUE 7
#define BREAK 8
#define WHILE 9
#define IF 10
#define ELSE 11
#define SWITCH 12
#define CASE 13
#define FOR 14
#define DO 15
#define SCANF 16
#define PRINTF 17
#define LC 35 //{
#define RC 36 //}
#define LB 37 //[
#define RB 38 //]
#define LP 39 //(
#define RP 40 //)
#define LOGRE 41//~
#define INPLUS 42//++
#define INMINUS 43//--
#define LOCRE 44//!
#define AND 45//&
#define STAR 46//*
#define DIVOP 47// /
#define COMOP 71// %
#define PLUS  48//+
#define MINUS 49//-
#define RELG 50//>
#define RELGEQ 51//>=
#define RELL 52//<
#define RELLEQ 53//<=
#define EQUOP 54//==
#define UEQUOP 55//!=
#define ANDAND 56//&&
#define OROR 57// ||
#define EQUAL 58// =
#define ASSIGNDIV 59// /=
#define ASSIGNSTAR 60 //*=
#define ASSIGNCOM 61 //%=
#define ASSIGNPLUS 62 //+=
#define ASSIGNMINUS 63 //-=
#define COMMA 64 //,
#define SHA 65 //#
#define SEMI 66//;
#define COLON 67//:
#define ID 70 //identifyer
#define NUMBER 69 //number
#define DEFAULT 68//default
int IDcount=0;//IDcount
char map[100][100];//符号表
int l_scope=0;//左括号数量
int r_scope=0;//右括号数量
int new_scope=1;//作用域标记符
%}
white [\t\n ]
digit [0-9]
letter [A-Za-z]
id ({letter}|_)({letter}|{digit}|_)*
number [1-9]{digit}*|0
commentbegin "/*"
commentelement .|\n
commentend "*/"
%x COMMENT
%%
{commentbegin} {BEGIN COMMENT; fprintf(yyout,"Begin a comment:\n");}
<COMMENT>{commentelement} {fprintf(yyout,"%s",yytext);}
<COMMENT>{commentend} {BEGIN INITIAL; fprintf(yyout,"\nthis comment End!\n");}
{white}+ ;
{number} {fprintf(yyout,"NUMBER %d %s\n",NUMBER,yytext);}
"void" {fprintf(yyout,"VOID %d %s\n",VOID,yytext);}
"char" {fprintf(yyout,"CHAR %d %s\n",CHAR,yytext);}
"int"  {fprintf(yyout,"INT %d %s\n",INT,yytext);}
"sizeof" {fprintf(yyout,"SIZEOF %d %s\n",SIZEOF,yytext);}
"const" {fprintf(yyout,"CONST %d %s\n",CONST,yytext);}
"return" {fprintf(yyout,"RETURN %d %s\n",RETURN,yytext);}
"continue" {fprintf(yyout,"CONTINUE %d %s\n",CONTINUE,yytext);}
"break" {fprintf(yyout,"BREAK %d %s\n",BREAK,yytext);}
"if" {fprintf(yyout,"IF %d %s\n",IF,yytext);}
"else" {fprintf(yyout,"ELSE %d %s\n",ELSE,yytext);}
"switch" {fprintf(yyout,"SWITCH	%d %s\n",SWITCH,yytext);}
"case" {fprintf(yyout,"CASE %d %s\n",CASE,yytext);}
"default" {fprintf(yyout,"DEFAULT %d %s\n",DEFAULT,yytext);}
"for" {fprintf(yyout,"FOR %d %s\n",FOR,yytext);}
"do" {fprintf(yyout,"DO	%d %s\n",DO,yytext);}
"while" {fprintf(yyout,"WHILE %d %s\n",WHILE,yytext);}
"scanf" {fprintf(yyout,"SCANF %d %s\n",SCANF,yytext);}
"printf" {fprintf(yyout,"PRINTF %d %s\n",PRINTF,yytext);}
{id} {
        int flag = 0;
        int i = 0;
        for(i=IDcount-1;i>0;i--)
        {
           if(strcmp(yytext,map[i])==0)
           {
               flag=1;break;
           }
        }
        if(flag==1&&new_scope!=0)//匹配到已有字符但仍处在旧的作用域
        {
           fprintf(yyout,"ID %d %s\n",i+70,yytext);
        }
        else//没有匹配到已有字符或者来到了新的作用域
        {
             IDcount++;
             strcpy(map[IDcount-1],yytext);
             new_scope=1;//每次插入一个新字符后需要将作用域标记符重新置1
             fprintf(yyout,"ID %d %s\n",IDcount-1+70,yytext);
        }
}

"{" {if(l_scope-r_scope==0)
//如果之前左右括号数量一样意味着这个左括号开启了一个新的作用域
                       new_scope=0;
               else
                       new_scope=1;
      l_scope++;
           fprintf(yyout,"LC %d %s\n",LC,yytext);}

"}" {r_scope++;
          fprintf(yyout,"RC %d %s\n",RC,yytext);}

"[" {fprintf(yyout,"LB %d %s\n",LB,yytext);}
"]" {fprintf(yyout,"RB %d %s\n",RB,yytext);}
"(" {fprintf(yyout,"LP %d %s\n",LP,yytext);}
")" {fprintf(yyout,"RP %d %s\n",RP,yytext);}
"~" {fprintf(yyout,"LOGRE %d %s\n",LOGRE,yytext);}
"++" {fprintf(yyout,"INPLUS %d %s\n",INPLUS,yytext);}
"--" {fprintf(yyout,"INMINUS %d %s\n",INMINUS,yytext);}
"!" {fprintf(yyout,"LOCRE %d %s\n",LOCRE,yytext);}
"*" {fprintf(yyout,"STAR %d %s\n",STAR,yytext);}
"/" {fprintf(yyout,"DIVOP %d %s\n",DIVOP,yytext);}
"%" {fprintf(yyout,"COMOP %d %s\n",COMOP,yytext);}
"+" {fprintf(yyout,"PLUS %d %s\n",PLUS,yytext);}
"-" {fprintf(yyout,"MINUS %d %s\n",MINUS,yytext);}
">" {fprintf(yyout,"RELG %d %s\n",RELG,yytext);}
"<" {fprintf(yyout,"RELL %d %s\n",RELL,yytext);}
">=" {fprintf(yyout,"RELGEQ %d %s\n",RELGEQ,yytext);}
"<=" {fprintf(yyout,"RELLEQ %d %s\n",RELLEQ,yytext);}
"==" {fprintf(yyout,"EQUOP %d %s\n",EQUOP,yytext);}
"!=" {fprintf(yyout,"UEQUOP %d %s\n",UEQUOP,yytext);}
"&&" {fprintf(yyout,"ANDAND %d %s\n",ANDAND,yytext);}
"||" {fprintf(yyout,"OROR %d %s\n",OROR,yytext);}
"=" {fprintf(yyout,"EQUAL %d %s\n",EQUAL,yytext);}
"/=" {fprintf(yyout,"ASSIGNDIV %d %s\n",ASSIGNDIV,yytext);}
"*=" {fprintf(yyout,"ASSIGNSTAR %d %s\n",ASSIGNSTAR,yytext);}
"%=" {fprintf(yyout,"ASSIGNCOM %d %s\n",ASSIGNCOM,yytext);}
"+=" {fprintf(yyout,"ASSIGNPLUS %d %s\n",ASSIGNPLUS,yytext);}
"-=" {fprintf(yyout,"ASSIGNMINUS %d %s\n",ASSIGNMINUS,yytext);}
"," {fprintf(yyout,"COMMA %d %s\n",COMMA,yytext);}
"#" {fprintf(yyout,"SHA %d %s\n",SHA,yytext);}
";" {fprintf(yyout,"SEMI %d %s\n",SEMI,yytext);}
":" {fprintf(yyout,"COLON %d %s\n",COLON,yytext);}
%%
int main()
{
  memset(map, 0, sizeof(map));
  yyin=fopen("testin.c","r");
  yyout=fopen("testout.txt","w");
  fprintf(yyout,"token name value\n");
  yylex();
  return 0;
}
int yywrap()
{
return 1;
}
```

将待分析的测试程序命名为`testin.c`，并执行：

```bash
$ lex c.lex
$ gcc lex.yy.c -o flex-demo -ll
$ ./flex-demo
```

例如：
```c
int a;
float b;

void(*(*f[3])(const char *p))(int x);

int main(int argc, char** argv) {
        int ______foo = (int)(void*)(&f);
        ___bar__________ = ______foo ^ 0x00114514u;
        return ___bar__________ & 0x01919810U;
}

int p;
```

分析结果为：
```
token name value
INT 3 int
ID 70 a
SEMI 66 ;
ID 71 float
ID 72 b
SEMI 66 ;
VOID 1 void
LP 39 (
STAR 46 *
LP 39 (
STAR 46 *
ID 73 f
LB 37 [
NUMBER 69 3
RB 38 ]
RP 40 )
LP 39 (
CONST 5 const
CHAR 2 char
STAR 46 *
ID 74 p
RP 40 )
RP 40 )
LP 39 (
INT 3 int
ID 75 x
RP 40 )
SEMI 66 ;
INT 3 int
ID 76 main
LP 39 (
INT 3 int
ID 77 argc
COMMA 64 ,
CHAR 2 char
STAR 46 *
STAR 46 *
ID 78 argv
RP 40 )
LC 35 {
INT 3 int
ID 79 ______foo
EQUAL 58 =
LP 39 (
INT 3 int
RP 40 )
LP 39 (
VOID 1 void
STAR 46 *
RP 40 )
LP 39 (
&ID 73 f
RP 40 )
SEMI 66 ;
ID 80 ___bar__________
EQUAL 58 =
ID 79 ______foo
^NUMBER 69 0
ID 81 x00114514u
SEMI 66 ;
RETURN 6 return
ID 80 ___bar__________
&NUMBER 69 0
ID 82 x01919810U
SEMI 66 ;
RC 36 }
INT 3 int
ID 74 p
SEMI 66 ;
```

不难从结果看出，该用例没有正确处理十六进制整数和个别运算符，不过还是很强了。