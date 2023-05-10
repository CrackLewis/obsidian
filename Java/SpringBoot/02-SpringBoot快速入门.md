
## 案例

需求：搭建工程，定义`HelloController.hello()`，返回`Hello SpringBoot!`。

实现步骤：
- 创建Maven项目
- 导入SpringBoot起步依赖
- 定义Controller
- 编写引导类
- 启动测试

### 在IDEA中创建项目

使用Spring Initializr模板，创建为Maven项目。

教程用Java 8，这边建议也用Java 8（？

最好在初始化时一次性添加依赖，否则后期会比较麻烦：
- Web：Spring Web
- 。。。

### 创建Controller

在`<your-repo>`下创建`controller`目录，添加`HelloController.java`，编写：

```java
@RestController
public class HelloController {
	@RequestMapping("/hello")
	public String hello() {
		return "Hello SpringBoot!";
	}
}
```

## 配置文件

使用`application.properties`或者`application.yml`，可以替换一些默认的SpringBoot配置。

```properties
server.port=8081
```

```yaml
server:
	port: 8081
```

优先级：`.properties`>`.yml`>`.yaml`

### SpringBoot读取自定义配置

方法一：`@Value("${variant}")`

```yaml
# application.yml
super:
	boba: "YES"
```

```java
public class HelloController {
	// ...
	@Value("${super.boba}")
	private String boba;

	@RequestMapping("")
	public String greet() {
		return boba;
	}
}
```

方法二：注入整个环境

方法二的好处在于：不必声明每一个引入的环境变量。

```java
public class HelloController {
	@Autowired
	private Environment env;

	@RequestMapping("")
	public String greet() {
		return env.getProperty("super.boba");
	}
}
```

方法三：`@ConfigurationProperties`

方法三可以一次注入整个对象，适合一组配置的高效读入。

```yaml
person:
	name: "Tommy"
	age: 18
```

```java
@Component
@ConfigurationProperties(prefix="person")
@Getter
@Setter
public class Person {
	private String name;
	private int age;
}
```

### 动态配置切换

SpringBoot程序常会被安装到不同环境。profile机制允许在不同的配置文件之间进行动态切换，而不需在每次安装时都重写配置文件。

配置方式：
- 多profile文件方式
- yml多文档方式

profile激活方式：
- 配置文件
- 虚拟机参数
- 命令行参数

#### 多profile文件配置方式

在`./src/main/resources`下有`application.properties`和多个备选配置：
- `application-dev.properties`：开发时配置
- `application-test.properties`：测试时配置
- `application-rel.properties`：发布时配置

在`application.properties`可以指定当前的活动配置文件：
```properties
spring.profiles.active=dev
```

#### yml多文档配置方式

在`./src/main/resources`下编写`application.yml`：
```yml
---
server:
	port: 8081
spring:
	profiles: dev
---
server:
	port: 8080
spring:
	profiles: rel
---
```

#### 激活特定的profile

配置文件内手动激活：
```yaml
spring:
	profiles:
		active: dev
```

或者在项目的虚拟机参数中指定：
![[Pasted image 20230418104738.png]]

或者在命令行参数中指定：
```bash
$ java -jar xxx.jar --spring.profiles.active=dev
```

### 内部配置加载顺序

优先级从高到低：
- `file:./config/`：当前项目的`config`目录下
- `file:./`：当前项目的根目录
- `classpath:/config/`：classpath的config目录
- `classpath:/`：classpath的根目录

SpringBoot的默认配置是最低优先级，因为`./src/main/resources`中的文件会被统一打包到`./target/classes`，也就是`classpath:/`中。

`file:./`指的是项目目录**上一级**目录。也就是说，`../config/application.properties`具有最高的优先级（如果文件存在）。

### 外部配置加载顺序

比内部配置文件优先，从高到低：
- 命令行参数
- 来自`java:comp/env`的JNDI属性
- Java系统属性：`System.getProperties()`
- 操作系统环境变量
- `RandomValuePropertySource`配置的`random.*`属性值

比内部配置文件低：
- `@Configuration`注解类上的`@PropertySource`指定的配置文件
- 通过`SpringApplication.setDefaultProperties`指定的默认属性
