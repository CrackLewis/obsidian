
## 概述

程序运行时出现的错误一般要么手动处理，要么运用*异常抛出-捕获-处理*机制。

两类可抛出对象：
- 错误（error）：严重的错误，程序难以或无法处理
- 异常（exception）：运行期间的一般错误，可以被外层程序捕获并处理
	- 运行时错误（`RuntimeException`）
	- 非运行时错误

`try-catch-finally`语句组用于捕获并处理`try`块内的异常。

如果一个方法显式标注了`throws xxxException`，则该方法的调用方必须设法捕获或显式抛出这种异常，否则编译不通过。
- 如果`void main(args)`方法设置`throws Exception`，则任何在`main`未捕获的异常都会使程序立刻退出。

异常对象的`printStackTrace()`方法可以记录和打印异常栈，非常实用。

## try-catch-finally

`catch`块可以有零或多个，要求靠前的`catch`异常不能是靠后`catch`异常的父类。只有最先捕获到异常的块会被执行。
- 如果方法没写`throws xxxException`，则至少要有一个`catch`块。

`finally`块无论是否捕获异常都会执行，可写可不写。

*异常嵌套*：
- 如果需要处理多层异常，则需要在下一次抛出时将异常参数（异常的起因）设置为此异常。
- 获取外部异常起因需要调用成员方法`getCause()`。

```java
try {
	...
} catch (LowerException e) {
	throw new UpperException(e);
}
```

*异常屏蔽*：
- 如果`catch`块内有异常，则会先执行`finally`，再抛出异常。
- 如果`catch`块内有异常，且执行`finally`块时又抛出了一个异常，则`catch`块异常会被屏蔽
- 解决方案：设法预先存储`catch`块内的异常，在执行`finally`块时将该异常通过`addSuppressed(e)`方法附加到`finally`块的异常中。获取被屏蔽的异常使用`getSuppressed()`方法。

```java
public class Main {
    public static void main(String[] args) throws Exception {
        Exception origin = null;
        try {
            System.out.println(Integer.parseInt("abc"));
        } catch (Exception e) {
            origin = e;
            throw e;
        } finally {
            Exception e = new IllegalArgumentException();
            if (origin != null) {
                e.addSuppressed(origin);
            }
            throw e;
        }
    }
}
```

## 自定义异常

Java的常用内置异常：

```ascii
Exception
├─ RuntimeException
│  ├─ NullPointerException
│  ├─ IndexOutOfBoundsException
│  ├─ SecurityException
│  └─ IllegalArgumentException
│     └─ NumberFormatException
├─ IOException
│  ├─ UnsupportedCharsetException
│  ├─ FileNotFoundException
│  └─ SocketException
├─ ParseException
├─ GeneralSecurityException
├─ SQLException
└─ TimeoutException
```

项目内自定义异常的基本玩法是：定义一个继承`RuntimeException`的根异常（如：`LewisBaseException`），再从此类型派生出其他异常类型。

## 空指针异常

对象引用为空，且试图访问对象引用时会引发空指针异常（`NullPointerException`）。此异常是一种编码逻辑错误，应当手动调整源码解决，*而非捕获处理*。

规避空指针异常的一些思路：
- 成员变量定义时初始化：如`private String foo = "";`，确保`foo`定义即有值。
- 函数尽可能返回空串、空数组而不是`null`。
- 使用`Optional<T>`。

定位`NullPointerException`：下列选项可以指示是哪个对象引发了异常

```bash
$ java -XX:+ShowCodeDetailsInExceptionMessages Main.java
```

## 断言

一种较老的Debug手段（C++：别骂了），modern java一般写单元测试

在运行选项中启用断言，断言才会被使用：

```bash
# 两种写法等价
$ java -enableassertions Main
$ java -ea Main
```

断言语法：

```java
assert x >= 0 : "x must be non-negative";
```

在启用断言且`x>=0`不成立时，触发`AssertionError`，并输出后面的提示信息。一旦断言触发，程序便不可恢复。