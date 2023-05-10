
TODO：该部分有点超出我目前的知识范围，需要后续完善。

[参考教程](https://www.bilibili.com/video/BV1Lq4y1J77x)



## 自动配置

Condition是Spring 4.0增加的条件判断功能。通过这个功能可以实现选择性的创建Bean操作。

在引导类中：
```java
public class SpringbootConditionApplication {
	public static void main(String[] args) {
		// 启动应用，返回Spring IOC容器
		ConfigurableApplicationContext context = SpringApplication.run(SpringbootConditionApplication.class, args);
		// 获取Bean，redisTemplate
		Object redisTemplate = context.getBean("redisTemplate");
		System.out.println(redisTemplate);
	}
}
```

## 监听机制



## 启动流程分析