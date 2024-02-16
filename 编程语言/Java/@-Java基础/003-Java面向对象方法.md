
## 有关概念

- 方法、构造方法
- 方法重载
- 继承
- 多态
- 抽象类
- 接口
- 静态字段和静态方法
- 包
- 作用域
- 内部类
- classpath和jar
- class版本
- 模块（since 1.9）

## 内部类

类的内部可以嵌套定义类。

内部类在外部类内使用时直接用内部类名，在外部类外可见且被使用时，用`外部类名.内部类名`表示。

内部类对象的创建必须依赖一个已经创建的外部类对象。内部类可访问外部类对象示例，通过`外部类名.this`访问。内部类可访问外部类的private成员。

内部类被编译后的class文件名为`外部类名$内部类名.class`。

```java
public class Main {
    public static void main(String[] args) {
        Outer outer = new Outer("Nested"); // 实例化一个Outer
        Outer.Inner inner = outer.new Inner(); // 实例化一个Inner
        inner.hello();
    }
}

class Outer {
    private String name;
    Outer(String name) {
        this.name = name;
    }
    class Inner {
        void hello() {
            System.out.println("Hello, " + Outer.this.name);
        }
    }
}
```

## 匿名类

匿名类指不通过class定义创建类的方法，一般思路是通过实现现有的接口、或继承现有的类实现匿名类。

匿名类的权限与内部类类似，都有外部类的private权限。

匿名类编译后的class文件名为`外部类名$数字.class`。数字表示类内的第几个匿名类。


```java
public class Main {
    public static void main(String[] args) {
        Outer outer = new Outer("Nested");
        outer.asyncHello();
    }
}

class Outer {
    private String name;
    Outer(String name) {
        this.name = name;
    }
    void asyncHello() {
	    // 第一类方式：实现接口
        Runnable r = new Runnable() {
            @Override
            public void run() {
                System.out.println("Hello, " + Outer.this.name);
            }
        };
        new Thread(r).start();

		// 第二类方式：继承现有的类
		HashMap m = new HashMap<>() {
			{
				put("key", "Hello, " + Outer.this.name);
			}
		};
		System.out.println(m.get("key"));
    }
}
```

## 静态内部类

静态内部类和前两者相比，独立性更强，没有`Outer.this`的访问权限，但仍然能访问外部类的private静态成员。

```java
public class Main {
    public static void main(String[] args) {
        Outer.StaticNested sn = new Outer.StaticNested();
        sn.hello();
    }
}

class Outer {
    private static String NAME = "OUTER";
    private String name;
    Outer(String name) {
        this.name = name;
    }
    static class StaticNested {
        void hello() {
            System.out.println("Hello, " + Outer.NAME);
        }
    }
}
```

## classpath

类的寻找路径。

JVM会根据classpath逐个找所要找到的类，如果都找不到就报错。

**不要在classpath中添加核心库**，现代版本不依赖classpath找核心库。

**不要为了跑某个程序调全局classpath**。运行时设置即可。

运行时设置classpath的方法：
假设要执行当前目录下一级`demo`目录下的`Hello`类，它会索引`D:\myclasses`下的库，则运行时指令为：

```bash
$ java -classpath .;D:\myclasses demo.Hello
# 或者简写为-cp
$ java -cp .;D:\myclasses demo.Hello
```

classpath中可以放jar包，相当于一个目录。`MANIFEST.MF`提供了jar包的信息，如`Main-Class`等。

## class版本

源码和class的兼容版本可能不同，例如：源码可能兼容到Java 9，class可能兼容到Java 11。

设置统一的源码/class兼容版本：
```bash
$ javac --release 11 Main.java
```

设置不统一的版本：
```bash
$ javac --source 9 --target 11 Main.java
```

前者会对源码进行兼容性检查，但后者不会。

## 模块

[廖雪峰](https://www.liaoxuefeng.com/wiki/1252599548343744/1281795926523938)

模块是一种更高效的源码组织模式。

以下列某个自行编写的模块为例：

```ascii
oop-module
├── bin
├── build.sh
└── src
    ├── com
    │   └── itranswarp
    │       └── sample
    │           ├── Greeting.java
    │           └── Main.java
    └── module-info.java
```

`module-info.java`记录模块的信息。`requires`表示使用的外部模块，`exports`表示允许外部模块访问的内部包。

```java
module hello.world {
	exports com.itranswarp.sample; // 允许外部代码访问这个包

	requires java.base; // 可不写，任何模块都会自动引入java.base
	requires java.xml;
}
```

模块内部的类只能使用经过引入的外部类，以`Main.java`为例：

```java
package com.itranswarp.sample;

// 必须引入java.xml模块后才能使用其中的类:
import javax.xml.XMLConstants;

public class Main {
	public static void main(String[] args) {
		Greeting g = new Greeting();
		System.out.println(g.hello(XMLConstants.XML_NS_PREFIX));
	}
}
```

编译要在`oop-module`目录下，执行：

```bash
$ javac -d bin src/module-info.java src/com/itranswarp/sample/*.java
```

如果编译成功，则项目结构为：

```ascii
oop-module
├── bin
│   ├── com
│   │   └── itranswarp
│   │       └── sample
│   │           ├── Greeting.class
│   │           └── Main.class
│   └── module-info.class
└── src
    ├── com
    │   └── itranswarp
    │       └── sample
    │           ├── Greeting.java
    │           └── Main.java
    └── module-info.java
```

下一步是打成jar包，注意要标出主类名：

```bash
$ jmod create --class-path hello.jar hello.jmod
```

打包之后，用jmod将包转化为模块：

```bash
$ jmod create --class-path hello.jar hello.jmod
```

执行时不会使用到`hello.jmod`文件，用jar文件就够：

```bash
$ java --module-path hello.jar --module hello.world
Hello, xml!
```

`hello.jmod`文件用于打包JRE。反正在模块化之前，执行java也要下载JRE，不如只用标准库内的必要模块和`hello.jmod`打包出一个精简JRE，省时省力：

```bash
$ jlink --module-path hello.jmod --add-modules java.base,java.xml,hello.world --output jre/
$ jre/bin/java --module hello.world
Hello, xml!
```

