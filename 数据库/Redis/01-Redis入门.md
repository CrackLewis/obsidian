
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

字符串限定指令：
- `incr/decr <key>`：在字符串为整数串时，令整数值加一或减一。
- `incrby/decrby <key> <value>`：在字符串为整数串时，令整数值加或减去`value`
- `append <key> <value>`：向`key`存储的字符串尾部追加`value`串
- `strlen <key>`：获取`key`存储的字符串长度
- `getrange <key> <start> <end>`：截取`[start,end]`范围的子串
- `setrange <key> <offset> <value>`：将`[start,~]`设置为

### 操作哈希表

`hmset`：向一个哈希表插入一或若干对键值。

`hget`：在哈希表中查询键对应的值。

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

### 操作序列

