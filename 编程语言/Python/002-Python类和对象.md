
## 对象的字符串显示

一般思路是重写`__repr__`方法和`__str__`方法。两者区别在于，前者是对象的*内部表示*，后者是对象转换形成的字符串。

```python
class A:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return 'A({0.x}, {0.y})'.format(self)

	def __str__(self):
		return '({0.x}, {0.y})'.format(self)

a = A(1, 2)
a # A(1, 2)
repr(a) # 'A(1, 2)'
str(a) # '(1, 2)'
print(a) # (1, 2)
```

## 对象的格式化

重写对象的`__format__`方法可以实现自定义格式化。

```python
_formats = {
	'ymd' : '{d.year}-{d.month}-{d.day}',
	'mdy' : '{d.month}/{d.day}/{d.year}',
	'dmy' : '{d.day}/{d.month}/{d.year}'
}

class Date:
	def __init__(self, year, month, day):
		self.year = year
		self.month = month
		self.day = day
		
	def __format__(self, code):
		if code == '':
			code = 'ymd'
		fmt = _formats[code]
		return fmt.format(d=self)

# doomsday :)
d = Date(2012, 12, 21)
format(d)                       # '2012-12-21'
format(d, 'mdy')                # '12/21/2012'
'The date is {:ymd}'.format(d)  # 'The date is 2012-12-21'
'The date is {:mdy}'.format(d)  # 'The date is 12/21/2012'
```

## 上下文管理协议

对象默认不支持*上下文管理协议*（`with`语句），除非正确实现了`__enter__`和`__exit__`方法。

`__enter__`和`__exit__`分别会在`with`语句进入后执行前、执行后退出前执行一次。

```python
from socket import socket, AF_INET, SOCK_STREAM
from functools import partial

class LazyConnection:
	def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
		self.address = address
		self.family = family
		self.type = type
		self.sock = None
		
	def __enter__(self):
		if self.sock is not None:
			raise RuntimeError('Already connected')
		self.sock = socket(self.family, self.type)
		self.sock.connect(self.address)
		return self.sock
		
	def __exit__(self, exc_ty, exc_val, tb):
		self.sock.close()
		self.sock = None

conn = LazyConnection(('www.python.org', 80))
# Connection not open at this point
with conn as s:
	# conn.__enter__() executes: connection open
	s.send(b'GET /index.html HTTP/1.0\r\n')
	s.send(b'Host: www.python.org\r\n')
	s.send(b'\r\n')
	resp = b''.join(iter(partial(s.recv, 8192), b''))
	# conn.__exit__() executes: connection closed
```

如果需要`with`语句嵌套，则对象应当设计为工厂模式：

```python
from socket import socket, AF_INET, SOCK_STREAM
from functools import partial

class LazyConnection:
	def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
		self.address = address
		self.family = family
		self.type = type
		self.connections = []
	def __enter__(self):
		sock = socket(self.family, self.type)
		sock.connect(self.address)
		self.connections.append(sock)
		return sock
	def __exit__(self, exc_ty, exc_val, tb):
		self.connections.pop().close()

# Example use
conn = LazyConnection(('www.python.org', 80))
with conn as s1:
	pass
	with conn as s2:
		pass
		# s1 and s2 are independent sockets
```

## 节省对象内存

可以通过指定`__slots__`属性，减少单个对象实例的内存消耗。具体原理为，将对应属性存储为更紧凑的数组，而非字典。

这种方法尤其适用于需要大量创建一类对象的情形下。

```python
class Date:
	__slots__ = ['year', 'month', 'day']
	def __init__(self, year, month, day):
		self.year = year
		self.month = month
		self.day = day
```

## 封装成员

Python不会实施真正的封装技术，即不会真正实施Public-Protected-Private三级访问控制。

一个惯例（但非官方规定）是：公有成员名前不加下划线，保护成员加一道下划线，私有成员加两道下划线。

Python会内部处理名前加两道下划线的成员，将它们*改名*。例如，对`A`类的`__private`成员，会将其实际改名为`_A__private`。这使得该属性不会被继承类定义同名变量所覆盖。

保护成员不会被特殊处理。

```python
class A:
	def __init__(self):
		self.__private = 1

	def _get(self):
		return self.__private

	def _set(self, v):
		self.__private = v

a = A()
a.__private # AttributeError: 'A' object has no attribute '__private'
a._A__private # 1
a._get() # 1
a._set(2)
a._get() # 2
```

## 创建可管理的属性

将成员声明为一个属性后，可以自定义它的`setter`、`getter`和`deleter`，从而实现类型检查、合法性验证等逻辑。

```python
class Person:
    def __init__(self, name):
        self.name = name

    # Getter function
    @property
    def name(self):
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    @name.deleter
    def name(self):
        raise AttributeError("nice try bro")

a = Person('James')
a.name # 'James'
a.name = 1 # TypeError: Expected a string
a.name = 'Humphrey'
a.name # 'Humphrey'
del a.name # AttributeError: nice try bro
```

上例中，`_name`是实际存储属性的成员，构造器内对`self.name`的赋值是为了在第一次给属性赋值时便进行检查。

上面只是一个个例，实际上并不需要对每个属性都规定`getter/setter/deleter`。

## 调用父类方法

类内调用`super()`可以获得直接父类引用，在类内可以通过`super().xxx()`的格式调用父类的`xxx`方法。

`super(ThisClass, this)`可以访问对象归属于直接父类那一部分的成员。

Python继承会和其他语言一样引入交叉继承问题，Python给出的结局方案是指定*方法解析顺序*（method resolution order，MRO）。详细参考：[Python super()详解](https://blog.csdn.net/wanzew/article/details/106993425)

```python
class A:
	def __init__(self):
		print("A.init")

class B(A):
	def __init__(self):
		print("B.init")
		super(B, self).__init__()

class C(A):
	def __init__(self):
		print("C.init")
		super(C, self).__init__()

class D(B, C):
	def __init__(self):
		print("D.init")
		super(D, self).__init__()

d = D() # D.init B.init C.init A.init
```

## 子类扩展属性

通过`super(ThisClass, ThisClass).the_property`访问父类的属性名。

如果`the_property`属性设置了`setter/deleter`，可以通过`__set__/__delete__`方法访问。

```python
class SubPerson(Person):
	@property
	def name(self):
		print('Getting name')
		return super().name
	@name.setter
	def name(self, value):
		print('Setting name to', value)
		super(SubPerson, SubPerson).name.__set__(self, value)
	@name.deleter
	def name(self):
		print('Deleting name')
		super(SubPerson, SubPerson).name.__delete__(self)
```

