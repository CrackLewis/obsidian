
通常的函数语法：

```python
def func(a, b):
	return a + b
```

## 参数

### 参数类型注解

在被指定类型的参数后加`: <type>`。例如下面这个例子指明`a,b`要传`int`：

```python
def func_1(a: int, b: int):
	return a << b
```

注意：类型注解**不是强制的**，不会在传错类型时报错，而只会出现在函数的`__annotation__`属性中。它的作用更类似于让其他人知道函数怎么用。


### 参数默认值声明

在指定默认值的参数后加`: <value>`。例如：

```python
def func_2(a: int = 2):
	return a ** 2;
```

注意：默认值**必须是不可变的**。如果默认值是一个可修改的容器（如列表、集合、字典），应当使用`None`作为初始值：

```python
def spam(a, b=None):
	if b is None: # 不用not b的原因是不被0、[]、False等值干扰
		b = dict()
	return b
```

这样做的目的是，防止默认值有意或无意被修改。如果上面的这个函数将`[]`作为`b`的初值，则一旦`spam`的返回值被修改，默认值也会受到影响。

### 可变参数

根据参数的灵活性，参数可分为：
- 位置参数（positional argument）：实参只有值，只能依次传递到形参的对应位置。如第4个位置参数只能填入第4个形参。
- 关键字参数（keyword argument）：实参包含键和值，优先匹配形参中的同名变量。

位置参数默认是定长的，如果形参列表有4个位置参数（无默认值），则实参也只能提供4个，3个或5个都不行。但`*`参数允许任意数量的位置参数：

```python
def func_3(*etc):
	sum = 0
	for i in etc:
		sum += i
	return sum
```

上例中，`etc`是一个依次包含所有位置参数的元组。注意，`*`参数必须放在所有位置参数的后面。

关键字参数在所有位置参数之后。默认也是定长的，但允许利用`**`参数传递任意数量的关键字参数：

```python
def func_4(a, **kwargs):
	pass
```

其中`**kwargs`是一个包含了所有关键字参数键值对的字典。注意，`**`参数必须是最后一个参数。

如果有一个位置参数元组，要作为参数传给一个可变位置参数的函数，则需要先用`*`进行解包：

```python
def func(a, *args):
	# ...

my_args = (2, 3, 5)
func(*my_args)
```

### 强制关键字参数

可变参数实际上将参数列表划分为四部分：
- 位置参数
- `*`参数
- 位于`*`参数和`**`参数之间的参数
- `**`参数

通过`*`参数的“封锁”，第三部分无法通过位置参数指定，只能通过关键字参数`xx=yy`指定。`*`参数可以省略名字，此时变成：

```python
def func_5(a, b, *, kw1, kw2 = 0):
	pass

func_5(1, 2, 3) # TypeError: func_5() takes 2 positional arguments but 3 were given
func_5(1, 2) # TypeError: func_5() missing 1 required keyword-only argument: 'kw1'
func_5(1, 2, kw1=0) # ok
```

## 返回值
### 返回值类型声明

在函数体前，形参列表后写`-> <type>`：

```python
def func(a: int) -> int:
	return a ** 2
```

### 返回多个值

如果函数中有类似`return a,b,c`的语句，它的实际效果是创建一个元组`(a,b,c)`再返回：

```python
def func_6(x: int):
	return x, x ** 2, x ** 3

func_6(2) # (2, 4, 8)
```

元组允许组合赋值，所以以下这种形式也是合法的：

```python
p1, p2, p3 = func_6(2) # p1=2, p2=4, p3=8
```

## lambda函数

lambda函数允许一行就写好一个函数。这种函数没有函数体，只有参数和返回表达式，在逻辑功能上弱一些。

```python
comp = lambda x, y: 1 if x > y else (-1 if x < y else 0)
```

如果lambda函数使用了外部变量，则其值生效的时刻是**计算时**，而不是定义时：

```python
x = 10
a = lambda y : x + y
x = 20
a = lambda y : x + y

a(10) # 30，注意不是20
b(10) # 30
```

## 通过预设参数减少实参个数

对于下面这种函数，每次都写出整个形参列表非常恼人：

```python
def func(a,b,c,d,e,f,g,h,i,j,k,l,*args,**kwargs):
	pass
```

`functools.partial(func, params)`允许在正式调用前**预先设置部分参数值**，将这种设定保存在一个变量中，在需要调用函数时使用：

```python
func_preset = functools.partial(func,1,2,3,4,5,6,7,8,9)
func(10,11,12,foo=13) # ok
func(10,11,12,13,14) # ok
func(10,11,12,15,bar=16) # ok
```

如果使用得当，它应该可以减少代码间的不兼容性。例如，以到某个顶点距离为关键字排序，可以这么写：

```python
points = [(1,2),(3,4),(5,6),(7,8)]

import math
def distance(p1,p2):
	x1,y1=p1
	x2,y2=p2
	return math.hypot(x2-x1,y2-y1)

pt=(4,3)
# sort的key只接受列表元素一个参数，所以这里用partial缩到一个
points.sort(key=partial(distance,pt))
points # [(3, 4), (1, 2), (5, 6), (7, 8)]
```

## 类转换为函数

对于只有构造器和单一方法的类，可以考虑将其转化为函数。例如：

```python
from urllib.request import urlopen

class UrlTemplate:
	def __init__(self, template):
		self.template = template
		
	def open(self, **kwargs):
		return urlopen(self.template.format_map(kwargs))

# Example use. Download stock data from yahoo
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
	print(line.decode('utf-8'))
```

可以转换为下面的写法。这个写法把初始成员`template`作为**闭包的参数**，闭包被调用后返回一个函数，主程序再将**方法参数**`name,fields`传给这个函数：

```python
# 闭包：利用template修饰内部函数
def urltemplate(template):
	# 内部函数：被返回的函数，接受template和关键字参数
	def opener(**kwargs):
		return urlopen(template.format_map(kwargs))
	return opener

# Example use
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
	print(line.decode('utf-8'))
```

## 回调函数访问外部信息

Python的回调函数通过参数传递，由接受者择机调用。回调函数可以访问传给它的参数，但在访问外部信息时会遇到麻烦。

一种解决方案是把函数包裹在`Handler`类中，将其中的一个成员方法作为回调函数传出。

```python
class CallbackHandler:
	def __init__(self, arg):
		self.arg = arg

	def handle(self, result):
		# 这里写回调函数的逻辑

r = CallbackHandler(my_arg)
# r.handle作为回调函数，在被调用时可以访问r的成员
callbacker(callback=r.handle)
```

另一种方法是使用函数闭包：

```python
def make_handler(**kwargs):
	# ...
	useable_vars = { ... }
	def handle(result):
		nonlocal useable_vars
		# 这里写回调函数的逻辑。可以访问useable_vars等闭包成员
	return handle

r = make_handler(arg1=1, arg2="2", ...)
# r.handle作为回调函数，在被调用时可以访问r的成员
callbacker(callback=r.handle)
```

还有一种基于协程的方法，它将协程的`send`方法作为回调。我目前不懂协程的具体细节，先把代码摆在这里：

```python
def apply_async(func, args, *, callback):
	# Compute the result
	result = func(*args)
	# Invoke the callback with the result
	callback(result)

def make_handler():
	sequence = 0
	while True:
		result = yield
		sequence += 1
		print('[{}] Got: {}'.format(sequence, result))

handler = make_handler()
next(handler) # 使handler推进到yield处
# 大意似乎是，等待apply_async执行handler.send(result)，
# 然后用result=yield完成赋值（？这也太nb了点）
apply_async(add, (2, 3), callback=handler.send)
```

## 内联回调函数

通过生成器和协程机制，可以实现通过`yield Async(func, args)`触发的回调函数机制不断推进函数进程，同时尽可能不搞乱程序控制流。

```python
def apply_async(func, args, *, callback):
	# Compute the result
	result = func(*args)
	# Invoke the callback with the result
	callback(result)

from queue import Queue
from functools import wraps

class Async:
	def __init__(self, func, args):
		self.func = func
		self.args = args

# 内联回调修饰器可以封装回调的细节，使得这个程序看起来是顺序执行的
def inlined_async(func):
	@wraps(func)
	def wrapper(*args):
		# 含yield的函数不会立刻执行，而是会返回一个生成器对象
		f = func(*args)
		result_queue = Queue()
		# 这个None是用于答复第一次的f.send
		result_queue.put(None)
		# 此时f还未执行，需要等待第一次f.send开始
		while True:
			result = result_queue.get()
			try:
				# f.send会激活func，使它执行到下一个yield并返回yield表达式
				# 这里的yield表达式是test中的Async对象
				a = f.send(result)
				apply_async(a.func, a.args, callback=result_queue.put)
			except StopIteration:
				break
	return wrapper

def add(x, y):
	return x + y

@inlined_async
def test():
	# 第一次f.send后，停顿于此，r的值由第二次f.send的参数赋予
	r = yield Async(add, (2, 3))
	print(r)
	# 第二次f.send后，停顿于此，r的值由第三次f.send的参数赋予
	r = yield Async(add, ('hello', 'world'))
	print(r)
	for n in range(10):
		r = yield Async(add, (n, n))
		print(r)
	print('Goodbye')
```

要点：
- 主程序在回调处应使用`yield`，这样内联回调修饰器可以介入执行进程并组织计算和返回过程。
- 内联回调修饰器必须和主程序在协程上达成一致。

实际上，上面例子的`apply_async`被刻意设计为与`multiprocessing.Pool`的同名成员方法一致。例如下面这个片段和直接执行`test()`的实际效果是一致的，但上面的例子是单线程，这个例子是多线程：

```python
import multiprocessing
pool = multiprocessing.Pool()
apply_async = pool.apply_async
test()
```

## 访问闭包中定义的变量

通常而言闭包内部变量不可见。但如果闭包函数附带了能够访问、修改内部变量的方法，则可以实现对闭包内部变量的访问：

```python
def sample():
	n = 0
	# Closure function
	def func():
		print('n=', n)
		
	# Accessor methods for n
	def get_n():
		return n
		
	def set_n(value):
		nonlocal n
		n = value
	
	# Attach as function attributes
	func.get_n = get_n
	func.set_n = set_n
	return func
```

下面是一个用闭包实现的栈。讽刺的是，这个栈比大部分通过类定义的栈的运行效率还高一些：

```python
import sys
class ClosureInstance:
	def __init__(self, locals=None):
		if locals is None:
			locals = sys._getframe(1).f_locals
			
	# Update instance dictionary with callables
	self.__dict__.update((key,value) for key, value in locals.items()
						if callable(value) )
	# Redirect special methods
	def __len__(self):
		return self.__dict__['__len__']()

# Example use
def Stack():
	items = []
	def push(item):
		items.append(item)
	def pop():
		return items.pop()
	def __len__():
		return len(items)
	return ClosureInstance()
```