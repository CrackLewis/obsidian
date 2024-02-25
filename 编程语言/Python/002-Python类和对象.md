
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

## 上下文管理

