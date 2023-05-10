
## 数组长度

```js
var arr = [1, 2, 3, 4];
arr.length; // 4
```

## 识别数组

- `Array.isArray(obj)`方法
- `instanceof`运算符

```js
var arr = [1, 2, 3, 4];
var pseuarr = { a0: 1, a1: 2, a2: 3, a3: 4};

Array.isArray(arr); // true
Array.isArray(pseuarr); // false

arr instanceof Array; // true
pseuarr instanceof Array; // false
```

## 数组转字符串

```js
[1,2,3,4].toString(); // "1,2,3,4"

[1,2,3,4].join(" * "); // "1 * 2 * 3 * 4"
```

## 尾部操作

- `arr.push(item)`：在数组尾部追加一个元素，返回数组新长度
- `arr.pop()`：从尾部移除一个元素，作为方法的返回值

```js
var arr = [1, 2, 3, 4];

var _ = arr.pop(); // _ = 4
arr.push(5); // 4
arr.push(6); // 5
_ = arr.pop(); // _ = 6
// arr = [1, 2, 3, 5]
```

## 头部操作

- `arr.shift()`：从头部移除一个元素，作为方法的返回值
- `arr.unshift(item)`：从头部插入一个元素，返回数组新长度

```js
var arr = [1, 2, 3, 4];

var _ = arr.shift(); // _ = 1
arr.unshift(5); // 4
arr.unshift(6); // 5
_ = arr.shift(); // _ = 6
// arr = [5, 1, 2, 3]
```

## 拼接数组

`arr.splice(offset, delcnt, ele1, ele2, ...)`：从`offset`下标起删除`delcnt`个元素，并依次插入`ele1`、`ele2`等元素。

```js
// 省略ele列表则表示只删除
var fruits = ["Banana", "Orange", "Apple", "Mango"];
fruits.splice(0, 1); // fruits = ["Orange", "Apple", "Mango"]

// delcnt=0则表示只插入
fruits = ["Banana", "Orange", "Apple", "Mango"];
fruits.splice(2, 0, "Lemon", "Kiwi"); // fruits = ["Banana", "Orange", "Lemon", "Kiwi", "Apple", "Mango"]

// 普通情况下，先删除，后插入
fruits = ["Banana", "Orange", "Apple", "Mango"];
fruits.splice(2, 2, "Lemon", "Kiwi"); // fruits = ["Banana", "Orange", "Lemon", "Kiwi"]
```

## 连接两个数组

`arr.concat(oth1, oth2, ...)`：将数组`oth1`、`oth2`等依次拼接到`arr`的末尾。

```js
var arr1 = ["Cecilie", "Lone"];
var arr2 = ["Emil", "Tobias", "Linus"];
var arr3 = ["Robin", "Morgan"];
var myChildren = arr1.concat(arr2, arr3);
```

## 截取数组片段

`arr.slice(begin, end)`：表示截取数组中处于区间`[begin, end)`的元素子序列。

如果省略`end`，则默认`end = arr.length`，即截取到数组最后。

```js
[1, 2, 3, 4].slice(2, 4); // [3, 4]
```

-----

前文的功能多为结构性功能。这里介绍一些和算法密切相关的功能。

## 数组排序

数组排序方法`arr.sort(comp?)`是功能最强大的数组方法之一。该方法默认按照**字符串字典序**给元素升序排序，如果指定了比较函数`comp`，则按照比较函数的比较结果排序。

```js
var arr = [1, 2, 8, 9, 10, 12];
arr.sort(); // arr = [1, 10, 12, 2, 8, 9]
arr.sort((a, b) => { return a - b; }); // arr = [1, 2, 8, 9, 10, 12]
```

### 比较函数

比较函数是改变数组元素排列顺序的函数。

比较函数`func(a, b)`的返回值的意义：
- 正值：`a`会排列到`b`的右侧
- 负值：`a`会排列到`b`的左侧

**注意：如果不是出于特殊目的，不要对数值数列使用默认排序。**

## 数组求最值

`arr.sort`可以通过排序将最值置于两侧，但效率显然不够。

解决方法：
- `Math.max.apply(null, arr)`：求最大值
- `Math.min.apply(null, arr)`：求最小值

-----

## 数组迭代

数组迭代是依次访问每个数组元素的过程。

### arr.forEach

`arr.forEach(func(val, idx?, arr?))`提供一种最通用的遍历方法。对于每个元素`arr[idx]`，都会调用一次`func(arr[idx], idx, arr)`。

如果`func`只有一个参数，则默认传递数组元素值，即`func(arr[idx])`。

```js
var text = "";
[1, 2, 3, 4].forEach((ele) => { text = text + ele.toString(); });
// text = "1234"
```

### arr.map

`arr.map(func(val, idx?, arr?))`基于原数组的元素值信息，通过元素映射函数`func`得到映射值，并基于映射值创建一个新数组。

```js
var arr1 = [1, 2, 3, 4];
var arr2 = arr1.map((val) => { return val * 2; });
// arr2 = [2, 4, 6, 8]
```

### arr.filter

`arr.filter(func(val, idx?, arr?))`通过筛选函数`func`筛选原数组元素，将所有通过筛选的元素组成一个新数组。

```js
var arr1 = [1, 2, 3, 4];
var arr2 = arr1.filter((val) => { return val > 2;});
// arr2 = [3, 4]
```

### arr.reduce & arr.reduceRight

`arr.reduce(func(preval, val, idx?, arr?))`依次（从低索引到高索引）遍历各个数组元素，并将上一个元素的`func`返回值作为下一个元素遍历时的输入（`preval`）。

```js
// 该用例演示如何将二进制数位数组转为十进制
var arr1 = [1, 0, 1, 0, 1, 0];
arr1.reduce((pre, val) => { return pre * 2 + val; }); // 42
```

`arr.reduceRight(func(preval, val, idx?, arr?))`是一个遍历方向相反、功能相同的姊妹函数。

```js
// 延续上面的示例
arr1.reduceRight((pre, val) => { return pre * 2 + val; }); // 21
```

### arr.every & arr.some

`arr.every(func(val, idx?, arr?))`是一个检查所有元素是否都通过测试的函数，是一种全称量词判断函数。

```js
// 检查数组是否单调递增
[1, 2, 3, 4].every((val, idx, arr) => { return (idx == arr.length - 1) || (val <= arr[idx + 1]); }); // true
```

`arr.some(func(val, idx?, arr?))`是`arr.every`的存在量词版本，只要有元素符合要求，该函数便返回`true`。

```js
[1, 2, 3, 4].some((val) => { return val >= 3; }); // true
```

## 数组元素检索

数组元素检索方法与字符串内的子串检索方法相似，但不完全相同。

- `arr.indexOf(item, start?)`：从`start`索引（可选）处向后寻找`item`
- `arr.lastIndexOf(item, start?)`：从`start`索引（可选）处向前寻找`item`
- `arr.find(val, idx?, arr?)`：返回通过测试的首个元素的**值**
- `arr.findIndex(val, idx?, arr?)`：返回通过测试的首个元素的**索引**

TBC