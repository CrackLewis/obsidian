
> 2401210309 李博宇

## 实验目的

通过部署并运行批量计算框架，加深对云计算技术的理解。

## 实验内容

在CentOS 7上部署Hadoop服务，并运行文本单词计数任务。

## 实验步骤

### 安装基本软件

首先在VMWare内安装CentOS 7虚拟机。为方便演示，安装桌面版。

![[Pasted image 20241204125224.png]]

在虚拟机内安装JDK 8和Hadoop 2.7.3。安装后通过检查Java和Hadoop版本，确认安装是否正确：

![[Pasted image 20241204125857.png]]

### 修改Hadoop配置

若要使Hadoop正常运行，需要修改系统环境变量，以及HDFS、MapReduce等服务的配置。

首先，将系统环境变量设置在`/etc/profile.d/hadoop-eco.sh`内：

```sh
JAVA_HOME=/opt/jdk
PATH=$JAVA_HOME/bin:$PATH

HADOOP_HOME=/opt/hadoop
PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
```

修改后执行`source /etc/profile.d/hadoop-eco.sh`使配置生效。

随后，修改Hadoop的`core-site.xml`文件，指明：
- HDFS运行在本机的9090端口
- 临时目录在`/opt/hadoop-record`下

```xml
<configuration>
        <property>
                <name>fs.defaultFS</name>
                <value>hdfs://localhost:9000</value>
        </property>
        <property>
                <name>hadoop.tmp.dir</name>
                <value>file:///opt/hadoop-record/tmp</value>
        </property>
</configuration>
```

再后，修改`hdfs-site.xml`，指明：
- 由于是单机运行，所以HDFS仅有1个副本。
- namenode和datanode在本机的位置

```xml
<configuration>
        <property>
                <name>dfs.replication</name>
                <value>1</value>
        </property>
        <property>
                <name>dfs.namenode.name.dir</name>
                <value>file:///opt/hadoop-record/name</value>
        </property>
        <property>
                <name>dfs.datanode.data.dir</name>
                <value>file:///opt/hadoop-record/data</value>
        </property>
</configuration>
```

随后，修改`mapred-site.xml`，指出MapReduce框架使用的是Yarn改进版：

```xml
<configuration>
        <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
        </property>
</configuration>
```

另外，修改`yarn-site.xml`，配置Yarn：

```xml
<configuration>
        <property>
                <name>yarn.resourcemanager.hostname</name>
                <value>localhost</value>
        </property>
        <property>
                <name>yarn.nodemanager.aux-services</name>
                <value>mapreduce_shuffle</value>
        </property>
</configuration>
```

### 启动Hadoop服务

首先需要格式化HDFS文件系统：

```sh
$ hdfs namenode -format
```

为防止服务启动不成功，先关闭系统防火墙：

```sh
$ sudo systemctl stop firewalld 
$ sudo systemctl disable firewalld 
```

启动文件系统和Yarn调度：

```sh
$ ./start-dfs.sh
$ ./start-yarn.sh
```

执行完毕后，执行`jps`检查正在运行的Hadoop服务：

```
[hadoop1@localhost hadoop]$ jps
52979 DataNode
53382 ResourceManager
58839 Jps
53178 SecondaryNameNode
53674 NodeManager
52828 NameNode
```

### 执行wordCount计算

由于运算需要在HDFS内执行，首先在HDFS内创建输入：

```sh
$ hadoop fs -mkdir /input
```

其次以Hadoop目录下的`LICENSE.txt`为例，将其拷入`/input`目录中。

```sh
$ hadoop fs -put LICENSE.txt /input
```

可以通过`hadoop fs -ls`命令检查：

![[Pasted image 20241204134255.png]]

执行如下命令，启动wordCount程序：

```sh
$ hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.3.jar wordcount /input /output2
```

![[Pasted image 20241204134511.png]]
![[Pasted image 20241204134527.png]]

输出说明了MapReduce的任务细节以及进度等信息。

在HDFS中执行`ls`命令，发现生成了两个结果文件，一个是只有文件名的flag文件，表示计算成功，另一个是结果信息文件。

![[Pasted image 20241204134733.png]]

将结果信息文件拷到本地，并查看：

![[Pasted image 20241204134942.png]]