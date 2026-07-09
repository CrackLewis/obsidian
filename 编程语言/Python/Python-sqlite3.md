
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

```python
"""
sqlite_helper.py - SQLite3 最佳实践封装工具

Usage:
    from sqlite_helper import SQLiteHelper
    
    db = SQLiteHelper("myapp.db")
    
    # 创建表
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 插入单条
    user_id = db.insert("users", {"name": "Alice", "email": "alice@example.com"})
    
    # 批量插入
    data = [{"name": f"User{i}", "email": f"user{i}@ex.com"} for i in range(100)]
    db.insert_many("users", data)
    
    # 查询
    users = db.query("SELECT * FROM users WHERE name LIKE ?", ("A%",))
    for row in users:
        print(row["name"], row["email"])
    
    # 更新
    db.execute("UPDATE users SET email = ? WHERE id = ?", ("new@ex.com", 1))
    
    # 事务
    with db.transaction():
        db.execute("UPDATE users SET name = ? WHERE id = ?", ("Bob", 1))
        db.execute("UPDATE users SET name = ? WHERE id = ?", ("Charlie", 2))
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class SQLiteHelper:
    """SQLite3 数据库工具类 - 封装最佳实践"""
    
    def __init__(
        self,
        db_path: Union[str, Path],
        *,
        row_factory: Any = sqlite3.Row,
        foreign_keys: bool = True,
        wal_mode: bool = True,
        busy_timeout: int = 5000,
        synchronous: str = "NORMAL",
        check_same_thread: bool = False,
    ):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库文件路径，或 ":memory:" 使用内存数据库
            row_factory: 行工厂，默认 sqlite3.Row（字典式访问）
            foreign_keys: 是否启用外键约束（默认开启）
            wal_mode: 是否启用 WAL 模式（默认开启）
            busy_timeout: 锁等待超时（毫秒）
            synchronous: 同步模式，NORMAL 配合 WAL 性能最佳
            check_same_thread: 是否检查同一线程（多线程场景建议 False）
        """
        self.db_path = str(db_path)
        self._row_factory = row_factory
        self._foreign_keys = foreign_keys
        self._wal_mode = wal_mode
        self._busy_timeout = busy_timeout
        self._synchronous = synchronous
        self._check_same_thread = check_same_thread
        
        # 创建目录（如果是文件数据库）
        if self.db_path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
    
    def _get_connection(self) -> sqlite3.Connection:
        """创建并配置一个新的数据库连接"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=self._busy_timeout / 1000,  # connect() 的 timeout 单位是秒
            check_same_thread=self._check_same_thread,
        )
        
        # 设置行工厂（字典式访问列）
        conn.row_factory = self._row_factory
        
        # 设置 PRAGMA（必须在每个连接上设置！）
        if self._wal_mode:
            conn.execute("PRAGMA journal_mode=WAL")
        
        if self._foreign_keys:
            conn.execute("PRAGMA foreign_keys=ON")  # 默认是 OFF，必须显式开启！
        
        conn.execute(f"PRAGMA busy_timeout={self._busy_timeout}")
        conn.execute(f"PRAGMA synchronous={self._synchronous}")
        
        return conn
    
    @contextmanager
    def connection(self):
        """上下文管理器：自动获取和关闭连接"""
        conn = self._get_connection()
        try:
            yield conn
        finally:
            conn.close()
    
    @contextmanager
    def transaction(self):
        """
        事务上下文管理器
        
        进入时自动开始事务，退出时自动提交（无异常）或回滚（有异常）
        
        Example:
            with db.transaction():
                db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
                db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = ?", (1,))
        """
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    @contextmanager
    def cursor(self):
        """游标上下文管理器：自动获取游标并确保关闭"""
        with self.connection() as conn:
            with conn.cursor() as cur:
                yield cur
    
    def execute(self, sql: str, params: Union[tuple, dict, None] = None) -> sqlite3.Cursor:
        """
        执行单条 SQL 语句（自动管理连接和游标）
        
        Args:
            sql: SQL 语句，使用 ? 占位符
            params: 参数元组或字典
        
        Returns:
            游标对象（已自动关闭，但 lastrowid 等属性仍可访问）
        
        Example:
            db.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "a@ex.com"))
            db.execute("SELECT * FROM users WHERE id = ?", (1,))
        """
        with self.cursor() as cur:
            cur.execute(sql, params or ())
            # 如果是 SELECT，保留结果供 fetch 使用
            if sql.strip().upper().startswith("SELECT"):
                return cur
            return cur
    
    def query(
        self,
        sql: str,
        params: Union[tuple, dict, None] = None,
        *,
        one: bool = False,
    ) -> Union[List[Dict], Dict, None]:
        """
        执行查询并返回结果
        
        Args:
            sql: SQL 查询语句
            params: 参数
            one: 是否只返回一条记录
        
        Returns:
            one=True: 返回单条字典或 None
            one=False: 返回字典列表
        
        Example:
            users = db.query("SELECT * FROM users WHERE age > ?", (18,))
            user = db.query("SELECT * FROM users WHERE id = ?", (1,), one=True)
        """
        with self.cursor() as cur:
            cur.execute(sql, params or ())
            if one:
                row = cur.fetchone()
                return dict(row) if row else None
            return [dict(row) for row in cur.fetchall()]
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        插入单条记录
        
        Args:
            table: 表名
            data: 字段名 -> 值的字典
        
        Returns:
            插入行的 lastrowid
        
        Example:
            user_id = db.insert("users", {"name": "Alice", "email": "a@ex.com"})
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.cursor() as cur:
            cur.execute(sql, tuple(data.values()))
            return cur.lastrowid
    
    def insert_many(self, table: str, data_list: List[Dict[str, Any]]) -> int:
        """
        批量插入多条记录（使用 executemany，性能提升 50-100 倍）
        
        Args:
            table: 表名
            data_list: 字典列表，所有字典必须包含相同的键
        
        Returns:
            插入的行数
        
        Example:
            data = [{"name": f"User{i}", "email": f"u{i}@ex.com"} for i in range(1000)]
            db.insert_many("users", data)
        """
        if not data_list:
            return 0
        
        columns = list(data_list[0].keys())
        column_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        sql = f"INSERT INTO {table} ({column_str}) VALUES ({placeholders})"
        
        # 构建参数列表
        params_list = [tuple(d.get(col) for col in columns) for d in data_list]
        
        with self.cursor() as cur:
            cur.executemany(sql, params_list)
            return len(data_list)
    
    def upsert(
        self,
        table: str,
        data: Dict[str, Any],
        conflict_columns: List[str],
        update_columns: Optional[List[str]] = None,
    ) -> int:
        """
        UPSERT：存在则更新，不存在则插入
        
        Args:
            table: 表名
            data: 数据字典
            conflict_columns: 冲突检测列（通常是唯一键）
            update_columns: 需要更新的列，默认更新所有非冲突列
        
        Returns:
            影响的行数
        
        Example:
            db.upsert("users", {"id": 1, "name": "Alice", "email": "a@ex.com"}, ["id"])
        """
        columns = list(data.keys())
        placeholders = ", ".join(["?"] * len(columns))
        col_str = ", ".join(columns)
        
        # 构建 ON CONFLICT 子句
        conflict_str = ", ".join(conflict_columns)
        
        if update_columns is None:
            update_columns = [c for c in columns if c not in conflict_columns]
        
        if update_columns:
            update_set = ", ".join([f"{c}=excluded.{c}" for c in update_columns])
            sql = f"""
                INSERT INTO {table} ({col_str}) VALUES ({placeholders})
                ON CONFLICT({conflict_str}) DO UPDATE SET {update_set}
            """
        else:
            sql = f"""
                INSERT INTO {table} ({col_str}) VALUES ({placeholders})
                ON CONFLICT({conflict_str}) DO NOTHING
            """
        
        with self.cursor() as cur:
            cur.execute(sql, tuple(data.values()))
            return cur.rowcount
    
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        result = self.query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
            one=True,
        )
        return result is not None
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """获取表结构信息"""
        return self.query(f"PRAGMA table_info({table_name})")
    
    def vacuum(self):
        """收缩数据库，释放空闲空间"""
        self.execute("VACUUM")
    
    def backup(self, backup_path: Union[str, Path]) -> None:
        """
        备份数据库到另一个文件
        
        Args:
            backup_path: 备份文件路径
        """
        backup_path = str(backup_path)
        with self.connection() as src_conn:
            with sqlite3.connect(backup_path) as dst_conn:
                src_conn.backup(dst_conn)
```

使用示例：

```python
# 初始化（数据库文件自动创建）
db = SQLiteHelper("data/myapp.db")

# 建表
db.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL CHECK(price >= 0),
        stock INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 日常操作
db.insert("products", {"name": "Laptop", "price": 999.99, "stock": 10})
db.insert_many("products", [
    {"name": "Mouse", "price": 29.99, "stock": 50},
    {"name": "Keyboard", "price": 79.99, "stock": 30},
])

# 查询（返回字典列表，通过列名访问）
results = db.query("SELECT * FROM products WHERE price > ?", (50,))
for p in results:
    print(f"{p['name']}: ${p['price']}")
```