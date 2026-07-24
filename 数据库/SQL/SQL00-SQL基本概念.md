
SQL = structural query language 结构化查询语言

*SQL分类*：

| 分类        | 功能              | 常见关键字                              |
| --------- | --------------- | ---------------------------------- |
| 数据查询语言DQL | 检索/查询数据         | `select`                           |
| 数据操作语言DML | 对库内数据添加/删除/修改   | `insert`、`delete`、`update`         |
| 数据定义语言DDL | 对库结构或表结构进行调整    | `create`、`alter`、`drop`、`truncate` |
| 数据控制语言DCL | 控制用户的数据库权限和安全等级 | `grant`、`revoke`                   |
| 事务控制语言TCL | 控制事务，保持数据一致性    | `commit`、`rollback`、`savepoint`    |

SQL数据库中的*常见概念*：
- 表（table）
- 视图（view）
- 索引（index）：一种用于加速数据检索的数据库对象
- 主键
- 外键
- 约束（constraint）

高级特性、编程概念：
- 事务（transaction）：一组要么全部成功、要么全部不执行的SQL操作，保证数据的原子/一致/隔离/持久（ACID）性质
- 存储过程（stored procedure）：预编译并存储在数据库的一组SQL语句，可像函数一样被调用执行
- 触发器（trigger）：一种特殊存储过程，会在特定数据库事件后自定执行
- 函数（function）：内建/用户自定义的，用于执行特定计算并返回值的程序
- 游标（cursor）：用于在结果集中逐行处理数据的数据库对象

*标准、方言和生态*：
- SQL标准：早年是`SQL-xx`，近年是`SQL:20xx`
- 方言：如pgSQL、MySQL等

