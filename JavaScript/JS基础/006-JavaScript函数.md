
## 函数定义

- 传统定义：`function`关键字开头，后带形参列表和函数体
- 构造器定义：`new Function(arg1, ..., bodytext)`。
- 箭头函数定义：`(arg1, ...) => { body }`。

## 函数的参数

JS允许在函数定义中指定任意多个形参。

JS不会：
- 限定参数的类型
- 限定外部调用时传参数量
- 对调用实参进行类型检查

如果传参个数少于形参列表变量个数，则多余形参将使用`undefined`为值。

如果传参个数过多，则需要访问`arguments`对象。

### arguments对象

`arguments`是函数内置数组对象，会依序存储传入的各参数。

```js
x = sumAll(1, 123, 500, 115, 44, 88);

function sumAll() {
    var i, sum = 0;
    for (i = 0; i < arguments.length; i++) {
        sum += arguments[i];
    }
    return sum;
}
```

### 传址还是传值？

如果参数是对象：传址

如果参数非对象：传值

## call() & apply()

`A.func.call(B, args)`和`A.func.apply(B, arglist)`在B对象上执行A对象方法`func`。

`func`函数内访问B对象时使用`this`属性。

```js
var person = {
  fullName: function(city, country) {
    return this.firstName + " " + this.lastName + "," + city + "," + country;
  }
}
var person1 = {
  firstName:"Bill",
  lastName: "Gates"
}
person.fullName.call(person1, "Seattle", "USA");
person.fullName.apply(person1, ["Seattle", "USA"]);
```

区别：
- `call`方法依次传参
- `apply`方法传递一个参数数组

## 闭包

