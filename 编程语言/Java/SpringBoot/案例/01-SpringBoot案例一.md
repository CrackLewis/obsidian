
## 大致步骤

- 建立实体类，和数据库表单字段保持一致
- 建立mapper接口，定义操作数据库的动作
- 建立mapper的xml文件，写具体的SQL语句
- 建立service类，处理业务逻辑
- 在controller类中展示结果

## 准备

### 建立IDEA项目

New Project->Spring Initializr

依赖：
- Spring Web
- Spring Boot Plugin?
- MySQL Driver
- JDBC API
- MyBatis Framework

JDK建议选20

### 改pom.xml

加MyBatis依赖

### 改应用配置文件

一般有一个`./src/main/resources/application.properties`文件，改成`application.yml`。

下面是一份可行的配置：

```yaml
server:  
  port: 8081  # 服务器端口
spring:  
  datasource:  
    driver-class-name: com.mysql.cj.jdbc.Driver  
    url: jdbc:mysql://127.0.0.1:3306/springboot1?characterEncoding=utf-8&useSSL=false&serverTimezone=UTC  
    username: root  
    password: Liboyu.021109  
mybatis:  
  mapper-locations: classpath:mapper/*.xml
```

上面的案例中：`spring.datasource.url`指定了应用连接哪个MySQL服务器的哪个数据库。`springboot1`是数据库名。

### 尝试编写一个示例Controller

比较低端的controller类似其他web服务器中的路由。

DemoEntity定义在同目录的DemoEntity.java中，描述一个元对象。
```java
package org.lewislee.project1.controller;  
  
import org.springframework.web.bind.annotation.RequestMapping;  
import org.springframework.web.bind.annotation.RestController;  
  
@RestController  
public class DemoController {  
    @RequestMapping("/abc")  
    public DemoEntity getEntity() {  
        return new DemoEntity("Sam", 21, DemoEntityGender.MALE);  
    }  
  
}
```

当用户对`localhost:8081/abc`发送一个GET请求时，它会返回一个JSON对象。

```json
{ "name": "Sam", "age": 21, "gender": "MALE" } 
```

## 正式工作

### 建立实体类

实体类应当尽量保证定义与MySQL数据库表单的字段序列一致。

```java
public class User {
    public int id;
    public String name;
    public int age;
    public String email;
}
```

可以通过以下几种方式添加Getter和Setter：
- 通过IDEA的代码补全添加
- 通过Java Bean的方式为需要getter和setter方法的成员添加`@Getter`和`@Setter`注解
- 通过Lombok的方式为整个类添加`@Getter`和`@Setter`注解

### 编写实体对应的mapper接口

```java
package org.lewislee.project1.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.lewislee.project1.entity.User;

import java.util.List;

@Mapper
public interface UserMapper {
    List<User> selectAll();
}
```

### 编写mapper对应的xml

在`./src/main/resources/mapper`中建立`UserMapper.xml`文件，编写操作需要使用的SQL语句。

写法比较固定，对着下面的代码块改就行了。

```xml
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.lewislee.project1.mapper.UserMapper">
    <select id="selectAll" resultType="org.lewislee.project1.entity.User">
        select * from users
    </select>
</mapper>
```

### 建立service类

建立`UserService`类，确定后端逻辑。

目前的后端逻辑是查SQL表，获取用户列表之后一股脑返回。

```java
package org.lewislee.project1.service;

import org.lewislee.project1.entity.User;
import org.lewislee.project1.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {

    @Autowired
    public UserMapper userMapper;

    public List<User> selectAll() {
        return userMapper.selectAll();
    }
}
```

### 建立controller类

建立`Controller`类，确定对外提供的路由。

```java
package org.lewislee.project1.controller;

import org.lewislee.project1.entity.User;
import org.lewislee.project1.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class DemoController {

    @Autowired
    private UserService userService;

    @RequestMapping("/users")
    public List<User> getAllUsers() {
        return userService.selectAll();
    }
}
```

## 效果

访问`localhost:8081/users`，程序返回一个所有用户的JSON列表。

## 项目结构

![[Pasted image 20230415151050.png]]