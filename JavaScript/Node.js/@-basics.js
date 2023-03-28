/**
 * JavaScript 基础语法
 */

/**
 * 基本输出
 */
function output_demo() {
  // 浏览器弹框输出
  window.alert("Window Alert");
  // 写HTML文档
  document.write("New HTML content");
  // 写HTML元素
  document.getElementById("demo").innerHTML = "new-demo";
  // 输出到浏览器控制台
  console.log("Console log");
}

/**
 * 语法基本内容
 */
function grammar_demo() {
  /**
   * 字面量
   */
  // 数字字面量：整数、浮点数
  let _ = 3.14;
  _ = 1001;
  _ = 123e5;
  // 字符串字面量：可以使用单双引号包围
  _ = 'Joe Biden';
  _ = "Donald Trump";
  // 表达式字面量：用于计算
  _ = 5 * 6;
  _ = 5 + 10;
  // 数组字面量：定义一个数组
  _ = [ 40, 100, 1, 5, 25, 10 ];
  // 对象字面量：定义一个对象
  _ = {
    firstname : "Lewis",
    lastname : "Lee",
    age : 21,
    major : "Computer Science"
  };
  // 函数字面量：定义一个函数
  _ = function __subfunc(a, b) { return a + b; };

  /**
   * 变量
   */
  // 可以使用var/let定义一个变量
  // var的作用域为所在函数内（变量提升），let为所在代码块内

  // 此处ivar有效（undefined），但ilet无效
  if (1) {
    // 此处ivar有效（undefined），但ilet无效
    var ivar = 0;
    let ilet = 0;
    // 此处ivar有效（0），ilet有效（0）
  }
  // 此处ivar有效（0），但ilet无效

  /**
   * 操作符
   */
  // 算术、赋值、位移运算与Python类似
  _ = (5 + 6) / 10;  // _ = 1.1
  _ = _ * 2;         // _ = 2.2
  _ = 3 << 10;       // _ = 3072

  /**
   * 标识符和保留字
   * 标识符：_、字母、数字或$组成，不能是数字开头
   * 保留字：JavaScript语言标准保留的一些特殊单词，不能用作标识符
   */

  /**
   * 注释
   * 老生常谈，行注释和块状注释
   */

  /**
   * 数据类型：
   * 基础数据类型包括数字、字符串、数组、对象
   */
}

/**
 * JavaScript语句相关
 */
function statement_demo() {
  // 绝大部分JS语句都有一个关键词开头，唯一常见的例外是赋值语句
  let _ = undefined;

  // 变量声明语句：var、let
  var __ = 0;
  let ___ = null;

  // 分支语句：if-else、switch
  _ = 1;
  if (_) {
    console.log("test positive");
  } else {
    console.log("test negative");
  }

  switch (_) {
    case 1: {
      console.log("test 1");
      break;
    }
    case 2: {
      console.log("test 2");
      break;
    }
    default: {
      console.log("test unknown");
      break;
    }
  }

  // 循环语句：for、while、do-while、for-in
  for (_ = 0; _ < 10; ++_) {
    console.log("for " + _);
  }

  while (_) {
    console.log("while " + _);
    _--;
  }

  do {
    console.log("do-while " + _);
    _++;
  } while (_ < 10);

  let _arr = [ 1, 2, 3, 4, 5 ];
  for (i in _arr) {
    console.log("for-in " + i);
  }

  // 跳转语句：continue、break、return
  while (0) {
    if (_ == 1)
      continue;  // 继续循环
    else if (_ == 2)
      break;  // 跳出循环
    else if (_ == 3)
      return;  // 函数返回
  }

  // 异常处理语句：try、catch、throw
  try {
    if (_ == undefined) throw '_ is undefined!!!';
  } catch (err) {
    console.log(err);
  }

  // 函数嵌套定义语句：function
  function __subfunct() {}
}

/**
 * JavaScript变量相关
 */
function variable_demo() {
  /**
   * 变量类型：
   * 可分为两大类，值类型和引用类型
   *
   * 值类型包括所有的基本数据类型，保存在栈中，占用固定空间，使用typeof判断类型
   * 引用类型占用不固定的空间，保存在堆中，使用instanceof判断类型，一般使用new()等方法创建
   */

  /**
   * 作用域与优先级
   * 局部变量>参数变量>全局变量
   *
   * 与C++/Python不同，var变量没有块级作用域的概念，只有let区分块级作用域
   */
}

/**
 * JavaScript数据类型相关
 */
function data_type_demo() {
  /**
   * 数据类型：
   * 字符串(String)
   * 数字(Number)
   * 布尔(Boolean)
   * 数组(Array)
   * 对象(Object)
   * 空(Null)
   * 未定义(Undefined)
   */

  var _;

  // 数字包括整型、实型两种类别
  // 实数可以用小数定义，也可以用十进制科学计数法定义
  _ = 114514.0 + 1.919810e6;
  // 整数可以用八进制、十进制和十六进制定义
  _ = 0337522 + 2333 * 0x1d4b42;
  // 实数范围由Number.MIN_(MAX_)VALUE定义
  _ = Number.MAX_VALUE + Number.MIN_VALUE;
  // 整数范围由Number.MIN_(MAX_)SAFE_INTEGER定义
  _ = Number.MIN_SAFE_INTEGER + Number.MAX_SAFE_INTEGER;
  // 超出计算范围的值由Number.POSITIVE_(NEGATIVE_)INFINITY定义
  _ = Number.POSITIVE_INFINITY + Number.NEGATIVE_INFINITY;
  _ = Infinity;
  _ = -Infinity;
  // 测试一个数是否溢出可使用Number.isFinite
  if (Number.isFinite(_) == false) console.log('finity test failed');
  // 还有一个非数值量，不等于任何数值，与任何值都不相等包括自己，用isNaN测试
  _ = NaN;
  if (Number.isNaN(_) == true) console.log('nan test failed');

  // 字符串默认为Unicode编码，整个生命期内不改变值
  // 转义符是字符串内用于表示特殊字符的符号序列，\x表示ANSI标准字符，\u表示Unicode字符
  _ = '\n\t\b\r\f\\\'\"\x23\u0051';
  // toString方法是一个常用的其他类型转字符串的方法，具体后面详解
  _ = 123;
  _ = _.toString(16);  // _ = '7b'
  // eval方法用于执行一个字符串内的JS代码，该方法安全性较低，后面详解
  eval('console.log(\'this is a line of code inside the eval method.\')');

  // 数组：下面几种定义方式都是合法的。
  _ = new Array;  // (1)
  _[0] = 0;
  _[1] = 1;
  _[2] = 2;
  _ = new Array(0, 1, 2);  // (2)
  _ = [ 0, 1, 2 ];         // (3)

  // 对象：一组属性和方法的集合
  _ = new Object;
  // 下面两种操作属性的方法都是允许的
  _.first_attr = '1';
  _['second_attr'] = 2;
  // 属性不一定要是变量属性，也可以是函数属性
  _.func = function() { return 0; };
  // 也可以一次性定义整个对象
  _ = {first_attr : '1', second_attr : 2};
  // 对象运行时检测属性是否存在用hasOwnProperty
  console.log(
      '_.hasOwnProperty = %s',
      String(_.hasOwnProperty('first_attr')));  // '_.hasOwnProperty = true'
  // 运行时检测某个属性是否可枚举
  console.log(String(_.propertyIsEnumerable('second_attr')));  // 'false'
  // toString是对象自带的字符串表示函数，可以被重写
  console.log(_.toString());  // '[object Object]'
  // valueOf是对象自带的值表示函数，可以被重写
  console.log(_.valueOf());  // '{ first_attr: "1", second_attr: 2 }'

  // 布尔值：只有true和false两个值
  // 空字符串、零、NaN、null和undefined都转换为false，否则为true
  _ = '' | 0 | NaN | null | undefined;

  // null逻辑上是一个空对象指针，用typeof查询会显示Object
  _ = typeof null;  // _ = 'object'

  /**
   * 类型转换
   * 这里的类型转换一般指其他类型转数字或字符串
   */
  
}