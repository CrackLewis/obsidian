
- 在配置文件中通过`profiles`或`activeProfiles`指定。
- 会在构建时修改POM
- 用于给参数设定不同的目标环境，如开发、测试、生产环境

## 构建配置文件类型

- 项目级：定义在`pom.xml`中
- 用户级：定义在`~/.m2/settings.xml`中
- 全局级：定义在`$M2_HOME/conf/settings.xml`中

## 构建配置文件格式

```xml
<!-- 前文 --->
<profiles>
	<profile>
		<id>test</id>
		<build>
			<plugins>插件配置</plugins>
		</build>
	</profile>
</profiles>
<!--- 后文 --->
```

## 构建配置文件激活

