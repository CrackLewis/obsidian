创建数据库

```mysql
create <dbname>;
```

删除数据库

```mysql
drop <dbname>;
```

选择数据库

```mysql
use <dbname>;
```

数据类型（值类型）

| 类型        | 大小                    | 范围                  |
| ----------- | ----------------------- | --------------------- |
| TINYINT     | 1                       | C++ char              |
| SMALLINT    | 2                       | C++ short             |
| MEDIUMINT   | 3                       | [-8388608,8388607]    |
| INT/INTEGER | 4                       | C++ long              |
| BIGINT      | 8                       | C++ long long         |
| FLOAT       | 4                       | C++ float             |
| DOUBLE      | 8                       | C++ double            |
| DECIMAL     | DECIMAL(M,D):max(M,D)+2 | relying on M,D        |
| DATE        | 3                       | 1000-01-01~9999-12-31 |
| TIME        | 3                       | \[-35day,+35day)       |
| YEAR        | 1                       | 1901~2155             |
| DATETIME    | 8                       | \[1000,10000)          |
| TIMESTAMP   | 4                       | \[1970,2038\]           |



数据类型（字符串类型）

| 类型                  | 大小         | 用途             |
| --------------------- | ------------ | ---------------- |
| CHAR/BINARY           | 0-255        | 定长字符串       |
| VARCHAR/VARBINARY     | 0-65535      | 变长字符串       |
| TINYBLOB              | 0-255        | 极短二进制字符串 |
| TINYTEXT              | 0-255        | 极短文本字符串   |
| BLOB                  | 0-65535      | 短二进制字符串   |
| TEXT                  | 0-65535      | 短文本字符串     |
| MEDIUMBLOB/MEDIUMTEXT | 0-16777215   | 中二进制/中文本  |
| LONGBLOB/LONGTEXT     | 0-4294967295 | 长二进制/长文本  |

创建表

```mysql
create table <tbname> ( key1 type1, key2 type2, ... , PRIMARY KEY( key1 ), ...);
```

删除表

```mysql
drop table <tbname>;
```

插入数据

```MySQL
insert into <tbname> ( key1, key2, ... ) value ( val1, val2, ... );
```

查询数据

