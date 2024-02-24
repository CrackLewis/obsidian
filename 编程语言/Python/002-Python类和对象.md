
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