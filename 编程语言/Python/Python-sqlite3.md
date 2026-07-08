
sqlite3是Python的内置库，不需要安装

```python
import sqlite3
```

## 数据类型和方法

数据类型：
- `sqlite3.Connection`：到数据库的一个连接会话
	- `.cursor()`：创建一个属于该连接的cursor对象
	- `.commit()`：提交当前事务，保存更改
	- `.rollback()`：回滚当前事务，撤销更改
	- `.close()`：关闭数据库连接
	- `row_factory` ：可调用对象，决定如何格式化查询返回的每一行数据
	- `total_changes`：连接打开以来，数据库改动了多少行
- `sqlite3.Cursor`：一个操作游标，用于查询/修改数据库表
	- `execute(sql, <params>)`：执行单条SQL
	- `executemany(sql, seq_of_params)`：对参数序列中的每个参数执行同一条SQL
	- `executescript(sql_script)`：一次性执行多条SQL
	- `fetchone()`：获取查询结果的下一行
	- `fetchall()`：获取查询结果集的所有剩余行
	- `fetchmany(size=cursor.arraysize)`：获取结果集的下一组行
	- `rowcount`：返回上一次`execute()`操作影响的行数
	- `connection`：RO，返回创建该游标的conn对象
	- `arraysize`：RW，控制fetchmany默认获取的行数，默认为1
	- `description`：RO，返回结果集中每列的描述信息

库方法：
- `sqlite3.connect(db_file)`：连接到本地文件数据库
- `sqlite3.register_adapter(type, adapter)`：注册一个转换函数，用于将自定义的 Python 类型转换为 SQLite 支持的类型
- `sqlite3.register_converter(typename, converter)`：注册一个转换函数，用于将从 SQLite 读取的指定类型数据转换为 Python 对象

## demo：sqlite3小牛刀

