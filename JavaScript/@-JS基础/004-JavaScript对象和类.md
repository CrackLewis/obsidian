
## 对象的创建

创建方法：
- 通过赋值对象字面量创建。最简单。
- 通过`new Object()`创建一个空对象。
- 通过类定义的构造器创建一个类对象。

```js
var obj1 = { attr1: 2, attr2: "3", attr3: () => { return attr1 + attr2; }};
var obj2 = new Object();
var obj3 = new Date(2002, 11, 9);
```

## 对象的引用

**注意：在任何环境下的JS中，变量都只是引用对象，并不负责存储对象。赋值不会复制对象，而只会给对象增加一个新的引用。**

```js
var a = { x: 1 };
var b = a;
// a = { x: 1 }, b = { x: 1 }
b.x = 2;
// a = { x: 2 }, b = { x: 2 }
```

## 对象的属性

属性定义了对象中包含的细节信息。每个属性必定对应一个值。

### 访问单个属性

访问单个属性必须指定属性名。

访问一个之前不存在的属性会创建它。

```js
object["attrname"];
object.attrname;
var x = "attrname";
object[x];
```

### 迭代访问属性

迭代访问一般用`for-in`循环。

```js
var person = {fname:"Bill", lname:"Gates", age:62}; 
var txt = "";

for (x in person) {
    txt += person[x];
}
```

### 删除属性

使用`delete`关键字可以删除一个属性。

```js
delete person.age;
```

## 对象的方法

方法是一种特殊的对象属性。它可以被外界调用，以实现某些特定的行为。

对象的方法内允许使用`this`关键字指代对象本身，以完成对对象成员的修改。

## 对象的字符串表示

- `JSON.stringify(obj)`：将对象转换为JSON
- `Object.values(obj)`：各个属性值通过逗号隔开

## 对象访问器：getter和setter

@since ES2009

getter是一种获取对象信息的设施，setter是一种设置对象信息的设施。

定义：
- `get mygetter()`
- `set mysetter(args)`

```js
var person = {
	firstName: "Bill",
	lastName : "Gates",
	language : "en",
	
	get fullName() {
		return this.firstName + ' ' + this.lastName;
	},

	set fullName(name) {
		var nameList = name.split(' ');
		this.firstName = nameList[0];
		this.lastName = nameList[1];
	}
};

var old = person.fullName; // old = "Bill Gates"
person.fullName = "Elon Musk";
person.firstName; // "Elon"
person.lastName; // "Musk"
```

 为什么使用 Getter 和 Setter：
-   它提供了更简洁的语法
-   它允许属性和方法的语法相同
-   它可以确保更好的数据质量
-   有利于后台工作

## 对象构造器

```js
function 构造器名(参数列表) {
	this.属性1 = 值1;
	this.属性2 = 值2;
	...;
}

var 对象 = new 构造器名(实参列表);
```

### 对象原型

可以通过`构造器名.prototype`访问一类对象构造器的原型对象。

向构造器的原型对象中加入属性，可以实现在不修改构造器的情形下，为所有该构造器后续创建的对象增加属性。

```js
function Person(first, last, age, eyecolor) {
    this.firstName = first;
    this.lastName = last;
    this.age = age;
    this.eyeColor = eyecolor;
}
Person.prototype.name = function() {
    return this.firstName + " " + this.lastName;
};

var a = new Person("Elon", "Musk", 50, "blue");
a.name(); // "Elon Musk";
```

## 对象方法

管理对象

```js
// 以现有对象为原型创建对象
Object.create()

// 添加或更改对象属性
Object.defineProperty(object, property, descriptor)

// 添加或更改对象属性
Object.defineProperties(object, descriptors)

// 访问属性
Object.getOwnPropertyDescriptor(object, property)

// 以数组返回所有属性
Object.getOwnPropertyNames(object)

// 访问原型
Object.getPrototypeOf(object)

// 以数组返回可枚举属性
Object.keys(object)
```

保护对象

```js
// 防止向对象添加属性
Object.preventExtensions(object)

// 如果属性可以添加到对象，则返回 true
Object.isExtensible(object)

// 防止更改对象属性（不是值）
Object.seal(object)

// 如果对象被密封，则返回 true
Object.isSealed(object)

// 防止对对象进行任何更改
Object.freeze(object)

// 如果对象被冻结，则返回 true
Object.isFrozen(object)
```

`Object.defineProperty(_object_, _property_, {_value_ : _value_})`：更改对象属性。

`Object.getOwnPropertyNames(obj)`：获取所有属性名。

## 类

@since ES2015

JS将类定义为一种创建、管理对象的**模板**。

### Constructor方法

创建对象的方法。任何类都应当至少具备一个`constructor`方法。

类定义外，用`类名(参数)`的方式可以创建一个类对象。

```js
class Car {
  constructor(name, year) {
    this.name = name;
    this.year = year;
  }
  age() {
    let date = new Date();
    return date.getFullYear() - this.year;
  }
}

let myCar = new Car("Ford", 2014);
```

### 成员方法

类定义内可以书写任意个成员方法。通过构造器创建对象后，所有成员方法将成为对象的成员。

### 类继承

`class DerivedClass extends BaseClass`

继承类内：
- `super`方法指代父类的`constructor`
- 会携带所有父类成员

### static方法

类内用`static`修饰的方法归属类，不归属某个对象。

类外调用`static`方法应用`类名.方法名(参数)`的格式。

## Map()和Set()

Map()是JS内置的映射表容器，Set()是JS内置的集合容器。

### Map()

- `new Map()`：构造器
- `map.set({ name: "keyname"}, value)`：设置键值对
- `map.get({ name: "keyname"})`：由键取值
- `map.entries()`：获取键值对数组。
- `map.keys()`：获取键数组。
- `map.values()`：获取值数组。
- `map.clear()`：清除所有元素。
- `map.delete({ name: "keyname"})`：删除指定键值对。
- `map.has({ name: "keyname"})`：查询键是否存在。
- `map.forEach(func(val, key))`：遍历所有键值对。
- `map.size`：映射表的大小。

### Set()

- `new Set()`：空白构造器
- `new Set(arr)`：带元素构造器
- `set.add(val)`：插入元素
- `set.clear()`：清除所有元素
- `set.delete(val)`：删除某个元素
- `set.entries()`：返回值数组
- `set.has(val)`：查询某个值是否存在
- `set.forEach(func(val))`：遍历集合。
- `set.keys()`：返回值数组
- `set.values()`：返回值数组（Set中与`key()`等义）
- `set.size`：集合的大小。

