
Java语法有诸多和C++、C#相似之处。这些相似之处不会被展开叙述。

## 基本语法

- 大小写敏感
- 源文件名必须和类名相同
- 主方法入口为`public static void main(String[] args)`，一处都不能改

## 标识符

- 可由字母、美元符号、下划线、数字组成
- 首字母不能是数字
- 不能是关键字或者字面常量
- 大小写敏感

## 修饰符

访问控制修饰符：
- `default`：默认权限
- `public`、`protected`、`private`：类的三级访问权限

非访问控制修饰符：
- `final`：不可继承的类
- `abstract`：抽象类
- `static`：静态的
- `synchronized`：同步的

## 关键字

- 访问控制：public/protected/default/private
- 类、方法、变量修饰符：abstract/class/extends/final/implements/interface/native/new/static/strictfp/synchronized/transient/volatile
- 程序控制语句：break/case/continue/do/else/for/if/instanceof/return/switch/while
- 错误处理：assert/catch/finally/throw/throws/try
- 包相关：import/package
- 基本类型：boolean/byte/char/double/float/int/long/short
- 变量引用：super/this/void
- 保留关键字：goto/const

null、true、false不是关键字，是字面常量，不能用作标识符。

## 类

类是创建Java对象的模板。

类内允许定义类变量（静态变量）、成员变量（非静态变量）、类方法和成员方法。

### 构造方法

类内默认提供一个无参空白构造方法。可以自行定义一至多个。

```java
public class Foo {
	public Foo() {
		bar = 0;
	}

	public Foo(int val) {
		bar = val;
	}

	private int bar;

	public int getBar() {
		return bar;
	}

	public int setBar(int newBar) {
		bar = newBar;
	}
}
```

### 创建对象

```java
Foo newObject = new Foo(15);
```

### 访问成员变量和成员方法

```java
// allowed
int oldBar = newObject.getBar();
newObject.setBar(114514);
// disallowed: access violation
newObject.bar;
```

### 源文件中的类声明规则

- 单个源文件中只能有一个`public`类，但可以有任意个非`public`类
- 源文件名和`public`类名必须一致
- 如果在包内定义，`package`语句必须放在首行
- `import`语句应当放在`package`语句后，其他语句前

### 包

包将类和接口分离开来。

## 基本数据类型

8种=4种整数类型+2种浮点类型+1种字符类型+1种布尔类型

- 整数类型
	- `byte`：1字节
	- `short`：2字节
	- `int`：4字节
	- `long`：8字节
- 浮点类型
	- `float`：32位单精度
	- `double`：64位双精度
- 字符类型：`char`：16位Unicode字符
- 布尔类型：`boolean`

基本类型相关常量：
- `typeclass.SIZE`：类型所占二进制位数，如`Character.SIZE`为16
- `typeclass.MIN_VALUE`
- `typeclass.MAX_VALUE`

### 引用类型

引用类型是相对基本数据类型而言的。后者存储值，前者存储值的引用。

类对象、数组均为引用类型，默认值为`null`。

### 类型转换

隐式类型转换：将B类型值赋给A类型。

强制类型转换：`(type_b)value_a`

## 变量

分类：
- 局部变量：定义在函数内
	- 参数变量：在形参列表中定义的局部变量
- 成员变量：定义在类内，每个类对象一份
- 类变量：定义在类内，每个类一份

Java**不允许**全局变量。

## 访问控制

| 修饰符 | 当前类 | 同一包内 | 包内派生类 | 包外派生类 | 其他包 |
| --- | --- | --- | --- | --- | --- |
| `public` | Y | Y | Y | Y | Y |
| `protected` | Y | Y | Y | Y/N* | N |
| `default` | Y | Y | Y | N | N |
| `private` | Y | N | N | N | N |

`private`和`protected`不能修饰外部类和接口。

\*: 如果包外的派生类继承该类，则可以访问该类的protected方法。

## 运算符

大部分运算符与C++中的同义。下面是不同或不存在于C++的个例：
- `>>>`：按位右移补零
- `instanceof`：对象是否为类的实例

## 逻辑结构

Java的分支结构与C++完全相同，循环结构的三段式`for`、`while`和`do-while`语句也相同，跳转语句`break`和`continue`也相同。

Java不支持goto。

Java支持对数组进行冒号遍历：
```java
int arr[5] = {1, 2, 3, 4, 5};
int ans = 1;
for (int x : arr) {
	ans *= x;
}
// ans = 120.
```

## 数组

Java数组是一系列同类型元素组成的序列。

声明数组可以用`new`或初始化列表声明：
```java
dataType[] arr1 = new dataType[12];
dataType[] arr2 = { 2, 3, 4 };
```

多维数组也是类似：
```java
dataType[][] arr3 = new dataType[6][5];
dataType[][][] arr4 = {{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}};
```

### Arrays类

`java.util.Arrays`类定义了一些数组上的方法：
- `Arrays.search(arr, key)`：在有序数组中二分搜索`key`
- `Arrays.equals(arr1, arr2)`：判断两个数组是否相等
- `Arrays.fill(arr, val)`：等值填充
- `Arrays.sort(arr)`：数组升序排序

## 方法

Java的方法必须定义在类内。

传参形式：
- 传值方式：基本数据类型
- 传址方式：对象、数组、etc

### 可变参数

@since JDK1.5

必须置于列表最后，可变参数代表的所有参数必须为同一类型。

```java
public static double getMax(double first, double... oth) {
	double ret = first;
	for (int i = 0; i < oth.length; ++i) {
		if (oth[i] > ret)
			ret = oth[i];
	}
	return ret;
}
```

### finalize方法

对象被回收前调用。

