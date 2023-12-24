
POM=Project Object Model，项目对象模型

可以指定的配置，包括但不限于：
- 项目依赖
- 插件
- 执行目标
- 项目构建profile
- 项目版本
- 项目开发者列表
- 相关邮件列表信息

## pom.xml示例

```xml
<project xmlns = "http://maven.apache.org/POM/4.0.0" xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation = "http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"> <!-- 模型版本 --> 
	<modelVersion>4.0.0</modelVersion> 
	<!-- 公司或者组织的唯一标志，并且配置时生成的路径也是由此生成， 如com.companyname.project-group，maven会将该项目打成的jar包放本地路径：/com/companyname/project-group --> 
	<groupId>com.companyname.project-group</groupId> 
	<!-- 项目的唯一ID，一个groupId下面可能多个项目，就是靠artifactId来区分的 -->
	<artifactId>project</artifactId> <!-- 版本号 --> 
	<version>1.0</version> 
</project>
```

- `project`：项目根标签
- `modelVersion`：模型版本
- `groupId`：工程组标识
- `artifactId`：工程标识
- `version`：工程版本号

## 父POM

父POM为子POM提供了一些可被继承和应用的配置。

可以通过`mvn help:effective-pom`查看当前目录下`pom.xml`的完整配置。