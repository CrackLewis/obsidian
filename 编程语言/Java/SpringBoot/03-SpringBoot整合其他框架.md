
## 案例：整合JUnit

实现步骤：
- 搭建工程
- 引入`starter-test`起步依赖
- 编写测试类
- 添加测试相关注解
	- `@RunWith(SpringRunner.class)`
	- `@SpringBootTest(classes=xxx.class`
- 编写测试方法

### 编写被测试的类

在`./src/main/java`中添加`com.itheima.springboottest.UserService`类。

```java
@Service
public class UserService {
	public void add() {
		System.out.println("add...");
	}
}
```

### 编写测试类

在`./test/java`中添加`com.itheima.test.UserServiceTest`类。

```java
@RunWith(SpringRunner.class)
@SpringBootTest(classes=SpringbootTestApplication.class)
public class UserServiceTest {
	@Autowired
	private UserService userService;

	@Test
	public void testAdd() {
		userService.add();
	}
}

// 如果这个类也打包在com.itheima.springboottest中，那么classes=xxx.class属性就不是必需的
```

### 运行测试

编写完毕后，运行`testAdd`方法，发现控制台中输出了`add...`。

## 案例：整合Redis

实现步骤：
- 搭建工程
- 引入`redis`起步依赖
- 配置redis相关属性
- 注入RedisTemplate模板
- 编写测试方法，测试

### 创建项目

依赖除了传统的Spring Initializr依赖外，还需选择`NoSQL->Spring Data Redis (Access+Driver)`。

教程项目artifact为`com.itheima.springbootredis`。

### 编写测试类

```java
@RunWith(SpringRunner.class)
public class SpringbootRedisApplicationTests {
	@Autowired
	private RedisTemplate redisTemplate;

	@Test
	public void testGet() {
		redisTemplate.boundValueOps("name").set("zhangsan");
	}

	@Test
	public void testSet() {
		Object name = redisTemplate.boundValueOps("name").get();
		System.out.println(name);
	}
}
```

### 启动测试

本机Redis服务必须处于运行状态。

先执行`testSet`，再执行`testGet`，控制台输出`zhangsan`。

## 案例：整合MyBatis

实现步骤：
- 搭建工程
- 引入MyBatis起步依赖，添加MySQL驱动
- 编写DataSource和MyBatis相关配置
- 定义表和实体类
- 编写DAO和Mapper文件/纯注解开发
- 测试

### 搭建工程

- `SQL->MyBatis Framework`
- `SQL->MySQL Driver`

内容与之前看过的一个案例比较重叠：[[01-SpringBoot案例一]] 

