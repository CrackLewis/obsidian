
有关资源：
- [官网](https://redis.io/)
- [Redis命令参考](http://doc.redisfans.com/)
- [Redis中文网](https://redis.com.cn/tutorial.html)

WTF is Redis：跨平台、NoSQL的键值存储系统

## 安装

Linux:

```bash
$ sudo apt install redis-server
```

## 初步运行

启动`redis-server`，并将其作为一个后台进程运行。默认情况下，它会开放在`*:6379`端口上：

```bash
$ redis-server &
$ disown
```

通过运行`redis-cli`访问一个Redis服务器，默认是`127.0.0.1:6379`：

```bash
$ redis-cli
127.0.0.1:6379> set k1 v1
OK
127.0.0.1:6379> get k1
"v1"
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> quit
$
```

## Redis配置

> [!info] 注意
> 为编写简便，`127.0.0.1:6379`缩写为`LHR`（LocalHost Redis-port）。

### 查看配置

```bash
# 查看所有配置
LHR> config get *
  1) "dbfilename"
  2) "dump.rdb"
  3) "requirepass"
  4) ""
  5) "masterauth"
  6) ""
# omitted 208 more lines......

# 查看一个配置
LHR> config get loglevel
1) "loglevel"
2) "notice"
```

### 修改配置

```bash
# 修改一个配置
LHR> config set loglevel warning
OK
LHR> config get loglevel
1) "loglevel"
2) "warning"
```

### 常见配置及其含义、设置

[Redis 配置 - 参数说明](https://www.runoob.com/redis/redis-conf.html)

最常用：
- `bind`：绑定的IP地址，默认`127.0.0.1`
- `port`：绑定的端口，默认`6379`
- `daemonize`：是否以后台方式运行，默认`no`
- `timeout`：客户端的无动作存活时间，单位为秒
- `loglevel`：指定日志记录级别，Redis 总共支持四个级别：`debug`、`verbose`、`notice`、`warning`，默认为`notice`
- `dir`：数据库文件存放地址，一般为`./`
- `dbfilename`：数据库文件名，默认为`dump.rdb`
- `maxmemory`：Redis可使用的最大内存字节数，设为`0`表示不限制

## 数据操作

**数据类型**：
- String：字符串
- Hash：键值对集合，常用于存储对象
- List：列表
- Set：集合
- ZSet：有序集合

`del`命令可以删除一个kv对：

```bash
127.0.0.1:6379> set delval 233
OK
127.0.0.1:6379> get delval
"233"
127.0.0.1:6379> del delval
(integer) 1
127.0.0.1:6379> get delval
(nil)
```

### 操作key

增删改查：
- `set <key> <value>`：设置`key`的字符串值为`value`
- `get <key>`：查询`key`的字符串值
- `del <key>`：移除`key`键值对
- `exists <key>`：查询`key`是否存在
- `type <key>`：获取`key`值的类型
- `rename <key> <new_key>`：重命名`key`
- `mset <k1> <v1> [<k2> <v2> ...]`：依次设置多个键值对
- `mget <k1> [<k2> ...]`：依次获取多个值
- `getset <key> <value>`：设置`key`为新值，并返回旧值

时效相关：
- `expire <key> <seconds>`：设置key的过期时间（多少*秒*后过期）
- `expireat <key> <timestamp>`：设置key的过期UNIX时间戳
- `pexpire <key> <msecs>`：设置key的过期时间（多少*毫秒*后过期）
- `pexpireat <key> <timestamp>`：设置key过期的UNIX时间戳，*单位毫秒*
- `persist <key>`：移除key的过期时间
- `ttl <key>`：返回key的存活时间（Time To Live，TTL）
- `pttl <key>`：返回key的存活时间，*单位毫秒*

### 操作字符串

`get/set`指令即可创建和查询字符串kv对，具体不再陈述。

字符串限定指令（部分）：
- `incr/decr <key>`：在字符串为整数串时，令整数值加一或减一。
- `incrby/decrby <key> <value>`：在字符串为整数串时，令整数值加或减去`value`
- `append <key> <value>`：向`key`存储的字符串尾部追加`value`串
- `strlen <key>`：获取`key`存储的字符串长度
- `getrange <key> <start> <end>`：截取`[start,end]`范围的子串
- `setrange <key> <offset> <value>`：将`[start,~]`设置为
- `getbit <key> <offset>`：获取`key`值中`offset`处的字符值
- `setbit <key> <offset> <value>`

### 操作哈希表（Hash）

*注意*：
- 本节所有的`key`都必须指向一个已创建好的哈希表，否则报类型错。
- 本节所有的`field`都表示哈希表内的某个字段。

基本命令：
- `hset <key> <f1> <v1>`：设置单个字段
- `hget <key> <field>`：在哈希表中查询键对应的值
- `hexists <key> <field>`：查询某个字段是否存在
- `hdel <key> <f1> [<f2> ...]`：删除多个字段

其余修改命令：
- `hdel <key> <f1> [<f2> ...]`：删除多个字段
- `hincrby <key> <field> <increment>`：将某个字段的值递增一个整数
	- `hincrby ...`：递增一个浮点数
- `hset <key> <f1> <v1>`：设置单个字段
	- `hsetnx`：仅在字段不存在时，设置字段
- `hmset <key> <f1> <v1> [<f2> <v2> ...]`：同时设置多个字段

其余查询命令：
- `hexists <key> <field>`：查询某个字段是否存在
- `hget <key> <field>`：在哈希表中查询键对应的值。
- `hmget <key> <f1> [<f2> ...]`：同时获取多个字段
- `hgetall <key>`：获取所有可用值
- `hkeys <key>`：获取哈希表内所有字段名称
- `hvals <key>`：获取哈希表内所有字段值
- `hlen <key>`：获取哈希表大小
- `hscan <key> <cursor> [match <pattern>] [count <count>]`：从`cursor`号字段开始，按照`pattern`模式匹配所有字段值，并返回不超过`count`个匹配成功的字段值

```bash
127.0.0.1:6379> hmset myhash k1 v1 k2 v2 k3 v3
OK
127.0.0.1:6379> hget myhash k1
"v1"
127.0.0.1:6379> hget myhash k3
"v3"
127.0.0.1:6379> hget myhash k4
(nil)
```

### 操作列表（List）

Redis列表是一种字符串列表，支持左右两端添删元素（有点类似于`std::deque<T>`），也支持随机访问（下标为0）。

与前面的哈希表类似，这里的`key`全部指List列表对象。

基本命令：
- `lindex <key> <index>`：根据index随机访问元素
- `linsert <key> [before|after] <pivot> <value>`：在pivot位置前或后插入元素`value`
- `llen <key>`：获取表长
- `lpop <key>`：弹出并获取列表的首个元素
- `lpush <key> <v1> [<v2> ...]`：从头部依次插入多个元素（后插的元素会排在最前）
- `lrange <key> <start> <end>`：获取`[start, end]`内的所有元素
- `lrem <key> <count> <value>`：移除表内元素
- `lset <key> <index> <value>`：随机写入
- `rpop <key>`：弹出末尾元素
- `rpush <key> <v1> [<v2> ...]`：从右端依次插入元素（后插入的会在最后）


阻塞读写命令：列表的一类独有命令，如果无法读写则会阻塞至读写成功或超时
- `blpop <key> <timeout>`：阻塞式弹出首个元素
- `brpop <key> <timeout>`：阻塞式弹出最后一个元素
- `brpoplpush <srckey> <deskey> <timeout>`：见`rpoplpush`

其他命令：
- `rpoplpush <srckey> <deskey>`：从`srckey`所指列表弹出最后一个元素，将其压入`deskey`所指列表的左侧
- `lpushx <key> <v1> [<v2> ...]`：仅当列表存在时插入
- `ltrim <key> <start> <end>`：将列表修剪至仅剩`[start, end]`区间的元素
- `rpushx <key> <v1> [<v2> ...]`

示例：

```bash
127.0.0.1:6379> lpush rk 1 2 3
(integer) 3
127.0.0.1:6379> rpush rk 4 5 6
(integer) 6
127.0.0.1:6379> lrange rk 2 4
1) "1"
2) "4"
3) "5"
127.0.0.1:6379> rpop rk
"6"
127.0.0.1:6379> lpop rk
"3"
127.0.0.1:6379> rpush rk 7
(integer) 5
127.0.0.1:6379> lpush rk 8
(integer) 6
127.0.0.1:6379> rpoplpush rk rk
"7"
127.0.0.1:6379> lrange rk 0 5
1) "7"
2) "8"
3) "2"
4) "1"
5) "4"
6) "5"
```

### 操作集合（Set）

Redis集合是无序字符串集合，集合内各成员唯一，通过哈希表实现。

基本命令：
- `sadd <key> <m1> [<m2> ...]`：集合内添加成员
- `scard <key>`：获取集合大小
- `sismember <key> <member>`：判断`member`是否为集合成员
- `smembers <key>`：获取所有成员
- `smove <src> <dest> <mem>`：将`mem`元素从`src`集合移动到`dest`集合
- `spop <key>`：弹出随机元素
- `srem <key> <m1> [<m2> ...]`：从集合中移除元素

其他命令：包含集合运算、
- `sdiff <k1> [<k2> ...]`：求差集
	- `sdiffstore <dest> <k1> [<k2> ...]`：求差集并存储
- `sinter <k1> [<k2> ...]`：求交集
	- `sinterstore <dest> <k1> [<k2> ...]`：求交集并存储
- `srandmember <key> [<count>]`：返回集合中一个或多个随机数
- `sunion <k1> [<k2> ...]`：求并集
	- `sunionstore <dest> <k1> [<k2> ...]`：求并集并存储
- `sscan <key> <cursor> [match <pattern>] [count <count>]`：迭代元素并筛选符合样式的前`count`个元素

示例：

```bash
127.0.0.1:6379> del rk
(integer) 1
127.0.0.1:6379> sadd rk1 1 2 3 4 5
(integer) 5
127.0.0.1:6379> scard rk1
(integer) 5
127.0.0.1:6379> sadd rk2 3 4 5 6 7
(integer) 5
127.0.0.1:6379> sinter rk1 rk2
1) "3"
2) "4"
3) "5"
127.0.0.1:6379> sinterstore rk3 rk1 rk2
(integer) 3
127.0.0.1:6379> smembers rk3
1) "3"
2) "4"
3) "5"
127.0.0.1:6379> srem rk1 4
(integer) 1
127.0.0.1:6379> sdiff rk1 rk2
1) "1"
2) "2"
```

### 操作有序集合（Sorted-set, Z）

[Redis 有序集合](https://www.runoob.com/redis/redis-sorted-sets.html)

与Redis无序集合相比，有序集合虽然也使用哈希表，但对每个值按分数进行了排序，集合内元素的顺序是由分数大小相对确定的。

基本指令：
- `zadd <key> <sc1> <mem1> [<sc2> <mem2> ...]`：添加指定分数的成员
- `zcard <key>`：获取成员数
- `zincrby <key> <increment> <member>`：对集合内的指定成员加分数
- `zrank <key> <member>`：返回指定成员的索引
- `zrem <key> <mem1> [<mem2> ...]`：移除特定成员

集合运算：
- `zinterstore <dest> <numkeys> <k1> [<k2> ...]`：存储交集
- `zunionstore <dest> <numkeys> <k1> [<k2> ...]`：存储并集

统计指令：
- `zcount <key> <min> <max>`：计算`[min, max]`*分数区间*内的成员数
- `zlexcount <key> <min> <max>`：计算`[min, max]`*字典区间*内的成员数
- `zrange <key> <start> <end> [withscores]`：列举`[start, end]`*索引区间*内的成员
- `zrangebylex <key> <min> <max> [limit <offset> <count>]`：列举`[min, max]`*字典区间*内的成员
- `zrangebyscore <key> <min> <max> [withscores] [limit]`：列举`[min, max]`*分数区间*内的成员
- 区间删除系列：`zremrangebylex`、`zremrangebyrank`、`zremrangebyscore`
- 区间排序系列：`zrevrange`、`zrevrangebyscore`、`zrevrank`
- `zscan`

### HyperLogLog

HyperLogLog是一种计算基数（可重集合的不重复元素数）的算法。该算法可以在使用很小且固定的空间时，*估算*大量元素的基数，并支持不同基数的合并。但由于该算法高度压缩了元素信息，所以不能删除已经添加的元素，也不能获知基数具体包含哪些元素。

根据HyperLogLog论文的说法，估算值与实际值的误差在0.81%以内。

指令：
- `pfadd <key> <ele1> [<ele2> ...]`：添加指定元素到HLL中
- `pfcount <key1> [<key2> ...]`：返回给定HLL的基数估算值
- `pfmerge <dest> <src1> [<src2> ...]`：合并多个HLL

示例：

```bash

127.0.0.1:6379> del rk
(integer) 0
127.0.0.1:6379> del rk2
(integer) 1
127.0.0.1:6379> del rk3
(integer) 1
127.0.0.1:6379> pfadd rk 111 222 333 444 555 666 777 888 999
(integer) 1
127.0.0.1:6379> pfcount rk
(integer) 9
127.0.0.1:6379> pfadd rk "aaa" "bbb" "abc" "ccc"
(integer) 1
127.0.0.1:6379> pfcount rk
(integer) 13
127.0.0.1:6379> pfadd rk2 222 444 666 888 123 234 345 456 "bbb" "ddd"
(integer) 1
127.0.0.1:6379> pfcount rk2
(integer) 10
127.0.0.1:6379> pfmerge rk3 rk rk2
OK
127.0.0.1:6379> pfcount rk3
(integer) 18
```

**原理**：参考源码[src/hyperloglog.c](https://github.com/redis/redis/blob/unstable/src/hyperloglog.c)

### Redis GEO

Redis GEO是Redis提供的存储地理坐标的集合，支持添加、删除、获取地理坐标、查询离指定位置特定范围内的坐标、计算两点间地理距离等操作。

有关指令：
- `geoadd <key> <lon1> <lat1> <member1> [<lon2> <lat2> <mem2> ...]`：向GEO添加一个地理坐标，以经纬度为标准
- `geopos <key> <mem1> [<mem2> ...]`：获取GEO中特定成员的坐标
- `geodist <key> <mem1> <mem2> [m|km|ft|mi]`：获取GEO中两点的地理距离（米/公里/英尺/英里）
- `georadius <key> <long> <lat> <radius> [m|km|ft|mi] [withcoord] [withhash] [count <count>] [asc|desc] [store <nkey>] [storedist <skey>]`：获取GEO中离所指定坐标`radius`半径内，最近的`count`个坐标，并选择是否存储到新GEO中
	- `georadiusbymember`：功能类似，但中心点是GEO的某个成员
- `geohash <key> <mem1> [<mem2> ...]`：获取GEO成员的哈希值

### Redis Stream

Redis Stream是一种持久化的队列式数据结构，可以：
- 维护一个消息链表
- 记录每个用户访问链表的具体位置
- 允许用户访问任意时刻的历史数据
- 主备复制，确保在断电时不丢失数据

![[Pasted image 20240420140940.png]]

Stream的*核心概念*：
- 消费者组（consumer group）：由多个消费者组成，由`xgroup create`创建。
	- 游标（last-delivered id）：每个消费者组一个游标，指向Stream的一个位置。每次读写都会使游标前进
	- 状态变量（pending ids）：每个消费者一个状态变量，维护消费者已读取但未确认的ID。

**消息队列相关命令：**
- **XADD** - 添加消息到末尾
- **XTRIM** - 对流进行修剪，限制长度
- **XDEL** - 删除消息
- **XLEN** - 获取流包含的元素数量，即消息长度
- **XRANGE** - 获取消息列表，会自动过滤已经删除的消息
- **XREVRANGE** - 反向获取消息列表，ID 从大到小
- **XREAD** - 以阻塞或非阻塞方式获取消息列表

**消费者组相关命令：**
- **XGROUP CREATE** - 创建消费者组
- **XREADGROUP GROUP** - 读取消费者组中的消息
- **XACK** - 将消息标记为"已处理"
- **XGROUP SETID** - 为消费者组设置新的最后递送消息ID
- **XGROUP DELCONSUMER** - 删除消费者
- **XGROUP DESTROY** - 删除消费者组
- **XPENDING** - 显示待处理消息的相关信息
- **XCLAIM** - 转移消息的归属权
- **XINFO** - 查看流和消费者组的相关信息；
- **XINFO GROUPS** - 打印消费者组的信息；
- **XINFO STREAM** - 打印流信息

## 发布和订阅

Redis的发布订阅是一种消息通信模式：
- 服务端：维护频道
- 客户端发布方：向频道内发送消息
- 客户端接收方：从频道接收消息

命令：
- `subscribe <chn>`：订阅频道，阻塞监听频道传来的消息
- `publish <chn> <msg>`：向频道发送消息

## 事务

Redis事务由一组指令组成，由`multi`指令开始，由`exec`指令结束。

介于`multi-exec`之间的指令会被暂存（`QUEUED`），在`exec`指令被键入时依次执行完毕。

`multi-exec`不允许嵌套。

与SQL数据库的事务不同，Redis事务*不具有原子性*，即使某个指令执行失败了，剩余指令也会依次执行完毕，先前执行的指令也不会回滚。

相关指令：
- `multi`、`exec`：事务的起始和终止指令
- `discard`：取消事务，放弃所有暂存的指令
- `watch <k1> [<k2> ...]`：监视一或多个键，如果事务执行之前这些键被改动了，事务将被打断
- `unwatch`：取消`watch`的所有监视

示例：

```bash
127.0.0.1:6379> MULTI
OK

127.0.0.1:6379> set book-name "Mastering C++ in 21 days"
QUEUED

127.0.0.1:6379> get book-name
QUEUED

127.0.0.1:6379> sadd tag "C++" "Programming" "Mastering Series"
QUEUED

127.0.0.1:6379> smembers tag
QUEUED

127.0.0.1:6379> exec
1) OK
2) "Mastering C++ in 21 days"
3) (integer) 3
4) 1) "Mastering Series"
   2) "C++"
   3) "Programming"
```

## 脚本

Redis使用Lua解释器执行脚本。

这块是个坑，还没学过Lua，回头补。

WIP

## Redis连接

- `auth <psw>`：验证密码是否正确
- `echo <msg>`：回显字符串
- `ping`：查看服务是否运行
- `quit`：关闭连接
- `select <idx>`：切换到指定的数据库

## Redis服务器

客户端连接指令：
- `client list`：获取连接列表
- `client getname`：获取连接名称
- `client pause <timeout>`：在指定时间内终止运行来自客户端的命令
- `client setname <conn_name>`：设置当前连接名称
- `client kill [<ip>:<port>] [id <cli_id>]`：关闭连接

存储指令：
- `bgrewriteaof`：异步执行一个AOF（AppendOnly File）文件重写操作
- `bgsave`：后台异步保存数据库
- `lastsave`：返回最后一次成功保存的UNIX时间戳
- `save`：同步保存数据库

指令管理指令：
- `command`：获取所有命令的详情
- `command count`：获取命令总数
- `command getkeys <command>`：获取给定命令的所有键
- `command info <command1> [<comm2> ...]`：获取给定命令的描述

服务器配置指令：
- `config get <parameter>`：获取指定配置参数
- `config rewrite`：改写配置文件`redis.conf`
- `config set <parameter> <value>`：修改指定配置参数
- `config resetstat`：重置`info`命令中的某些统计数据

杂项指令：
- `cluster slots`：获取集群结点的映射数组
- `time`：服务器时间
- `dbsize`：获取当前数据库的key数量
- `debug object <key>`：获取key的调试信息
- `debug segfault`：让Redis服务崩溃
- `flushall`：删除所有数据库的所有key
- `flushdb`：删除当前数据库的所有key
- `info <section>`：获取Redis服务器的各种信息和统计数值
- `monitor`：监视服务器收到的指令
- `role`：返回主从实例所属的角色
- `shutdown [save] [nosave]`：异步保存数据并关闭服务器
- `slaveof <host> <port>`：将当前服务器变为指定服务器的从属服务器
- `slowlog <subcomm> [<args>]`：管理Redis慢日志
- `sync`：用于复制功能的内部命令