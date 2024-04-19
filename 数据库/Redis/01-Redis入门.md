
有关资源：
- [官网](https://redis.io/)
- [Redis命令参考](http://doc.redisfans.com/)

WTF is Redis：
- 跨平台、NoSQL的键值存储系统

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

统计指令：
- `zcount <key> <min> <max>`：计算`[min, max]`*分数区间*内的成员数
- `zlexcount <key> <min> <max>`：计算`[min, max]`*字典区间*内的成员数
- `zrange <key> <start> <end> [withscores]`：列举`[start, end]`*索引区间*内的成员
- `zrangebylex <key> <min> <max> [limit <offset> <count>]`：列举`[min, max]`*字典区间*内的成员
- `zrangebyscore <key> <min> <max> [withscores] [limit]`：列举`[min, max]`*分数区间*内的成员
- 区间删除系列：`zremrangebylex`、