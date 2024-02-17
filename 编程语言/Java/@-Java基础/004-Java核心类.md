
## String

是内置的字符串类型，所有字符串字面量都转换为此类型。

**此类型不可变**。如果需要可变字符串，使用`StringBuilder`、`StringBuffer`、`StringJoiner`等。

比较字符串应当使用`a.equals(b)`的方法，不能使用`a == b`。

### 大小写转换

大小写转换相关方法：
- `toUpperCase()`
- `toLowerCase()`
- `equalsIgnoreCase()`：忽略大小写进行比较

### 子串检索

```java
// 检索是否包含某个子串：contains
"Hello".contains("ll"); // true
// 查找子串并返回其起始位置
"Hello".indexOf("1"); // 2
"Hello".lastIndexOf("1"); // 3
"Hello".startsWith("He"); // true
"Hello".endsWith("lo"); // true
```

### 子串截取

```java
// 截取子串
"Hello".substring(2); // "llo"
"Hello".substring(2, 4); // "ll"
```

### 去除首尾空白字符

注意非ASCII空白字符也会被去除

```java
"\u3000Hello\u3000".strip(); // "Hello"
" Hello ".stripLeading(); // "Hello "
" Hello ".stripTrailing(); // " Hello"
```

### 判断是否为空串

- `empty`：长度为0
- `blank`：全串完全由空白字符（空格、制表、回车等）组成

```java
// 判断是否为空串（长度为0）
"".isEmpty(); // true
"  ".isEmpty(); // false
// 判断是否为空白字符串（可能包含空格、回车、制表符）
"  \n".isBlank(); // true
" Hello ".isBlank(); // false
```

### 子串替换、分割、拼接

子串替换

```java
// 字面替换：将字符或字符串替换为其他字符或字符串
String s = "hello";
s.replace('l', 'w'); // "hewwo"
s.replace("ll", "~~"); // "he~~o"
// 正则表达式替换：将所有匹配替换为某个字面串
String s = "A,,B;C ,D";
s.replaceAll("[\\,\\;\\s]+", ","); // "A,B,C,D"
```

子串分割

```java
String s = "A,B,C,D";
String[] ss = s.split("\\,"); // {"A", "B", "C", "D"}
```

子串拼接

```java
String[] arr = {"A", "B", "C"};
String s = String.join("***", arr); // "A***B***C"
```

### 格式化字符串

格式化字符串：
- 常用占位符：`%s`、`%d`、`%x`、`%f`。
- 完整的格式化规则：[JavaDocs](https://docs.oracle.com/en/java/javase/14/docs/api/java.base/java/util/Formatter.html#syntax)

```java
public class Main {
    public static void main(String[] args) {
        String s = "Hi %s, your score is %d!";
        System.out.println(s.formatted("Alice", 80));
        System.out.println(String.format("Hi %s, your score is %.2f!", "Bob", 59.5));
    }
}
```

### 其他类型转换为String

```java
String.valueOf(123); // "123"
String.valueOf(45.67); // "45.67"
String.valueOf(true); // "true"
String.valueOf(new Object()); // 类似java.lang.Object@636be97c
```

### String转换为其他类型

```java
// String -> int
int n1 = Integer.parseInt("123"); // 123
int n2 = Integer.parseInt("ff", 16); // 按十六进制转换，255
// String -> bool
boolean b1 = Boolean.parseBoolean("true"); // true
boolean b2 = Boolean.parseBoolean("FALSE"); // false
```

### 与char数组互相转换

```java
char[] cs = "Hello".toCharArray();
String s = new String(cs);
```

### 编码、解码

- UTF-8、GBK等可直接使用`String`内的方法
- URL、Unicode、Base64等的编解码较繁琐，要用对应的库进行处理

```java
// 字符串转换为字节串的过程称为编码
byte[] b1 = "Hello".getBytes(); // 按系统默认编码转换，不推荐
byte[] b2 = "Hello".getBytes("UTF-8"); // 按UTF-8编码转换
byte[] b2 = "Hello".getBytes("GBK"); // 按GBK编码转换
byte[] b3 = "Hello".getBytes(StandardCharsets.UTF_8); // 按UTF-8编码转换
// 字节串转换为字符串的过程称为解码
String s3 = new String(b3, "GBK");
```

## StringBuilder

`StringBuilder`是一个字符串容器，可以在生命周期内任意修改，并在需要时转换为`String`：

```java
public class Main {
    public static void main(String[] args) {
        var sb = new StringBuilder(1024);
        sb.append("Mr ")
          .append("Bob")
          .append("!")
          .append("jinitaimei") // 谁家小黑子捣乱
          .delete(sb.length() - 10, sb.length()) // 你干嘛，哎呦
          .insert(0, "Hello, ");
        System.out.println(sb.toString());
    }
}
```

注意：现阶段不需要刻意将所有的`String`相加都改为`StringBuilder`操作，因为Java编译期会做这些事情。

`StringBuffer`是它的一个线程安全版本，没有必要刻意使用。

## java.util.StringJoiner

如果所有的`String`相加符合`A,B,C,D,....`的形式，那么可以考虑使用`StringJoiner`类。

例：问候所有人

```java
public class Main {
    public static void main(String[] args) {
        String[] names = {"Bob", "Alice", "Grace"};
        // 第一个参数是分隔符，第二个是前缀，第三个是后缀
        var sj = new StringJoiner(", ", "Hello ", "!");
        for (String name : names) {
            sj.add(name);
        }
        System.out.println(sj.toString());
    }
}
```

如果不指定开头结尾，那么`String.join`方法也同样方便：

```java
String[] names = {"Bob", "Alice", "Grace"};
var s = String.join(", ", names);
```

## 基本类型包装类

|基本类型|对应的引用类型|
|:--|:--|
|boolean|java.lang.Boolean|
|byte|java.lang.Byte|
|short|java.lang.Short|
|int|java.lang.Integer|
|long|java.lang.Long|
|float|java.lang.Float|
|double|java.lang.Double|
|char|java.lang.Character|

Java支持这些包装类和对应的基本类型隐式转换。

如果需要显式转换为基本类型，则一般使用`obj.xxxValue`方法，如：`i.intValue()`。但不建议在程序中频繁装拆箱，影响效率，且容易产生空指针异常。

包装类的`valueOf`方法可以将字符串或其他字面量转换为对应的基本类型。

同其他类一样，比较也必须使用`equals(...)`。

### 进制转换

`Integer`类支持整数和不同进制字面量之间的转换。

```java
int x1 = Integer.parseInt("100"); // 100
int x2 = Integer.parseInt("100", 16); // 256,因为按16进制解析

System.out.println(Integer.toString(100)); // "100",表示为10进制
System.out.println(Integer.toString(100, 36)); // "2s",表示为36进制
System.out.println(Integer.toHexString(100)); // "64",表示为16进制
System.out.println(Integer.toOctalString(100)); // "144",表示为8进制
System.out.println(Integer.toBinaryString(100)); // "1100100",表示为2进制
```

### 常量

```java
// boolean只有两个值true/false，其包装类型只需要引用Boolean提供的静态字段:
Boolean t = Boolean.TRUE;
Boolean f = Boolean.FALSE;
// int可表示的最大/最小值:
int max = Integer.MAX_VALUE; // 2147483647
int min = Integer.MIN_VALUE; // -2147483648
// long类型占用的bit和byte数量:
int sizeOfLong = Long.SIZE; // 64 (bits)
int bytesOfLong = Long.BYTES; // 8 (bytes)
```

## JavaBean

JavaBean是一种Java类的编写规范：
- 所有属性必须私有化。
- 所有私有化属性必须通过public方法暴露给其他类。
- 方法命名采用camel-case，每个属性对应一个get方法和一个set方法。

枚举JavaBean属性：

```java
import java.beans.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BeanInfo info = Introspector.getBeanInfo(Person.class);
        for (PropertyDescriptor pd : info.getPropertyDescriptors()) {
            System.out.println(pd.getName());
            System.out.println("  " + pd.getReadMethod());
            System.out.println("  " + pd.getWriteMethod());
        }
    }
}

class Person {
    private String name;
    private int age;
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
}
```

## 枚举类

下面两种枚举代码在形式上等价：

```java
// 第一种：enum关键字定义
public enum Color {
    RED, GREEN, BLUE;
}

// 第二种：定义具有枚举功能的类
public final class Color extends Enum { // 继承自Enum，标记为final class
    // 每个实例均为全局唯一:
    public static final Color RED = new Color();
    public static final Color GREEN = new Color();
    public static final Color BLUE = new Color();
    // private构造方法，确保外部无法调用new操作符:
    private Color() {}
}
```

为了增强枚举项的功能，可以设置枚举项的初值，或者添加字段和成员方法：

```java
enum Weekday {
    MON(1, "星期一"), TUE(2, "星期二"), WED(3, "星期三"), THU(4, "星期四"), FRI(5, "星期五"), SAT(6, "星期六"), SUN(0, "星期日");

    public final int dayValue;
    private final String chinese;

    private Weekday(int dayValue, String chinese) {
        this.dayValue = dayValue;
        this.chinese = chinese;
    }

    @Override
    public String toString() {
        return this.chinese;
    }
}
```

枚举比较适合用于switch语句。

## 记录类

不变类：
- 类本身为`final`，不可派生
- 所有成员为`final`，不可修改

Java 14开始可以通过record关键字创建记录类，该类是不变类，且不需要重写`hashCode`和`equals`等方法。

以下两种写法在形式上等价：

```java
record Point(int x, int y) {}

final class Point extends Record {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int x() {
        return this.x;
    }

    public int y() {
        return this.y;
    }

    public String toString() {
        return String.format("Point[x=%s, y=%s]", x, y);
    }

    public boolean equals(Object o) {
        ...
    }
    public int hashCode() {
        ...
    }
}
```

为记录类设置构造方法可以实现差错。为简写形式，构造方法省略了形参列表：

```java
public record Point(int x, int y) {
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException();
        }
    }
}
```

## 高精度类型

### java.math.BigInteger

`BigInteger`用int数组模拟一个大数，它和其他整数包装类型一样继承`Number`类。

只能通过成员方法进行计算，不能使用运算符。

可以通过`xxxValue`方法转换为基本类型。如果对应的基本类型溢出，会抛出ArithmeticException。

```java
BigInteger bi = new BigInteger("1234567890");
System.out.println(bi.pow(5)); // 2867971860299718107233761438093672048294900000

BigInteger i1 = new BigInteger("1234567890");
BigInteger i2 = new BigInteger("12345678901234567890");
BigInteger sum = i1.add(i2); // 12345678902469135780

BigInteger i = new BigInteger("123456789000");
System.out.println(i.longValue()); // 123456789000
System.out.println(i.multiply(i).longValueExact()); // java.lang.ArithmeticException: BigInteger out of long range
```

### java.math.BigDecimal

`BigDecimal`可表示任意大小和精度的、完全准确的浮点数。

加、减、乘时，其精度不会丢失，但除法如果除不尽，则会抛出异常。

成员方法`divideAndRemainder`支持同时求除法的商和余数。

默认的比较方法`equals`要求数值和scale同时相等。如果只是比较数值而非具体位数，则应使用`compareTo`方法。

```java
BigDecimal bd = new BigDecimal("123.4567");
System.out.println(bd.multiply(bd)); // 15241.55677489

BigDecimal d1 = new BigDecimal("123.45");
BigDecimal d2 = new BigDecimal("123.4500");
BigDecimal d3 = new BigDecimal("1234500");
System.out.println(d1.scale()); // 2,两位小数
System.out.println(d2.scale()); // 4
System.out.println(d3.scale()); // 0

BigDecimal d1 = new BigDecimal("123.4500");
BigDecimal d2 = d1.stripTrailingZeros();
System.out.println(d1.scale()); // 4
System.out.println(d2.scale()); // 2,因为去掉了00

BigDecimal d3 = new BigDecimal("1234500");
BigDecimal d4 = d3.stripTrailingZeros();
System.out.println(d3.scale()); // 0
System.out.println(d4.scale()); // -2

BigDecimal d1 = new BigDecimal("123.456");
BigDecimal d2 = new BigDecimal("23.456789");
BigDecimal d3 = d1.divide(d2, 10, RoundingMode.HALF_UP); // 保留10位小数并四舍五入
BigDecimal d4 = d1.divide(d2); // 报错：ArithmeticException，因为除不尽

BigDecimal n = new BigDecimal("12.75");
BigDecimal m = new BigDecimal("0.15");
BigDecimal[] dr = n.divideAndRemainder(m);
if (dr[1].signum() == 0) {
    // n是m的整数倍
}

BigDecimal d1 = new BigDecimal("123.456");
BigDecimal d2 = new BigDecimal("123.45600");
System.out.println(d1.equals(d2)); // false,因为scale不同
System.out.println(d1.equals(d2.stripTrailingZeros())); // true,因为d2去除尾部0后scale变为3
System.out.println(d1.compareTo(d2)); // 0
```

## 其他工具类

- Math
- java.util.HexFormat
- java.util.Random
- java.security.SecureRandom