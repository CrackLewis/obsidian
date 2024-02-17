
日志与直接输出信息相比的优点：
- 可设置输出样式
- 可设置输出级别
- 可重定向到文件
- 可按包名控制日志级别
- etc

## JDK Logging

```java
import java.util.logging.Level;
import java.util.logging.Logger;

public class Hello {
    public static void main(String[] args) {
        Logger logger = Logger.getGlobal();
        logger.info("start process...");
        logger.warning("memory is running out...");
        logger.fine("ignored.");
        logger.severe("process will be terminated...");
    }
}
```

JDK日志分为7个级别（严重到普通）：
- severe
- warning
- info（默认级别，低于此级别默认不会输出）
- config
- fine
- finer
- finest

局限性：
- JVM启动时日志系统便初始化完毕，一旦`main(args)`开始执行，不能改配置
- 配置不便，要加一坨参数
```bash
$ java -Djava.util.logging.config.file=<config_file_name> Main
```

## Commons Logging

严格来说CL不是独立的日志系统，它先找Log4j，找不到Log4j再用JDK Logging。

Maven仓库地址：[Apache Commons Logging](https://mvnrepository.com/artifact/commons-logging/commons-logging)

```xml
<!-- https://mvnrepository.com/artifact/commons-logging/commons-logging -->
<dependency>
    <groupId>commons-logging</groupId>
    <artifactId>commons-logging</artifactId>
    <version>1.3.0</version>
</dependency>
```

示例：

```java
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class Main {
    public static void main(String[] args) {
        Log log = LogFactory.getLog(Main.class);
        log.info("start...");
        log.warn("end.");
    }
}
```

如果有JAR也可以纯文件编译、运行：

```bash
$ javac -cp commons-logging-1.3.0.jar Main.java
$ java -cp .;commons-logging-1.3.0.jar Main
```

CL日志分6个级别：
- fatal
- error
- warning
- info（默认级别）
- debug
- trace

## Log4j

为CL提供底层实现。

与CL相比，依赖配置文件。配置文件`log4j2.xml`必须位于项目的classpath下，下面是一个示例：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration>
	<Properties>
        <!-- 定义日志格式 -->
		<Property name="log.pattern">%d{MM-dd HH:mm:ss.SSS} [%t] %-5level %logger{36}%n%msg%n%n</Property>
        <!-- 定义文件名变量 -->
		<Property name="file.err.filename">log/err.log</Property>
		<Property name="file.err.pattern">log/err.%i.log.gz</Property>
	</Properties>
    <!-- 定义Appender，即目的地 -->
	<Appenders>
        <!-- 定义输出到屏幕 -->
		<Console name="console" target="SYSTEM_OUT">
            <!-- 日志格式引用上面定义的log.pattern -->
			<PatternLayout pattern="${log.pattern}" />
		</Console>
        <!-- 定义输出到文件,文件名引用上面定义的file.err.filename -->
		<RollingFile name="err" bufferedIO="true" fileName="${file.err.filename}" filePattern="${file.err.pattern}">
			<PatternLayout pattern="${log.pattern}" />
			<Policies>
                <!-- 根据文件大小自动切割日志 -->
				<SizeBasedTriggeringPolicy size="1 MB" />
			</Policies>
            <!-- 保留最近10份 -->
			<DefaultRolloverStrategy max="10" />
		</RollingFile>
	</Appenders>
	<Loggers>
		<Root level="info">
            <!-- 对info级别的日志，输出到console -->
			<AppenderRef ref="console" level="info" />
            <!-- 对error级别的日志，输出到err，即上面定义的RollingFile -->
			<AppenderRef ref="err" level="error" />
		</Root>
	</Loggers>
</Configuration>
```

## Slf4j、Logback

Log4j/CL的竞品。

接口：

|Commons Logging|SLF4J|
|---|---|
|org.apache.commons.logging.Log|org.slf4j.Logger|
|org.apache.commons.logging.LogFactory|org.slf4j.LoggerFactory|

Slf4j和LB需要`logback.xml`作为配置文件，下面是一个示例：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

	<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
		<encoder>
			<pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
		</encoder>
	</appender>

	<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
		<encoder>
			<pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
			<charset>utf-8</charset>
		</encoder>
		<file>log/output.log</file>
		<rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy">
			<fileNamePattern>log/output.log.%i</fileNamePattern>
		</rollingPolicy>
		<triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy">
			<MaxFileSize>1MB</MaxFileSize>
		</triggeringPolicy>
	</appender>

	<root level="INFO">
		<appender-ref ref="CONSOLE" />
		<appender-ref ref="FILE" />
	</root>
</configuration>
```