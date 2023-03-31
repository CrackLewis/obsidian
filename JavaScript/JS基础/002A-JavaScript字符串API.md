
## 字符串长度

`str.length`

```js
var str = "123456";
str.length; // 6
```

## 字符串内查找子串

`str.indexOf(子串)`方法查找一个子串在字符串中的首个出现位置。

`str.lastIndexOf(子串)`查找最后一个字串位置。

返回值：
- 查找成功：首个/最后一个出现位置
- 查找失败：-1

```js
var str = "Practice makes perfect.";
str.indexOf("makes"); // 9
str.indexOf(" "); // 8
str.lastIndexOf(" "); // 14
str.indexOf("idle"); // -1
```

两种方法都接受第二个参数，作为查找的起始索引。

```js
var str = "The full name of China is the People's Republic of China.";
//         0----5----0----5----0----5----0----5----0----5----0----56
//         0---------1---------2---------3---------4---------5-----5
str.indexOf("China", 18); // 51
str.indexOf("China", 52); // -1
str.lastIndexOf("China", 50); // 17
str.lastIndexOf("China", 16); // -1
```

`str.search(子串)`方法是一个功能与`str.indexOf`功能类似的方法。区别在于：
- `str.indexOf`不支持正则表达式检索。
- `str.search`不支持设置开始位置参数。

`str.match(regex)`会返回`str`中匹配`regex`的子串。

```js
var text = "The rain in SPAIN stays mainly in the plain";
text.match(/ain/ig); // ["ain", "AIN", "ain", "ain"]
```

`str.includes(substr)`返回`str`是否包含`substr`。
```js
"Albus".includes("bus"); // true
"Potter".includes("one"); // false
```

`str.startsWith(prefix)`判断`str`是否以`prefix`开头。
`str.endsWith(suffix)`判断`str`是否以`suffix`结尾。

## 截取子串

`str.substring(start, end)`是一个子串截取方法，截取索引位于`[start, end)`区间内的。

```js
var str = "abcdeedcba";
str.substring(2, 6); // "bcde"
```

`str.slice(start, end)`方法是上面方法的延伸。它支持负数索引，如果索引为负，表示从串末尾向前截取。

```js
var str = "abcdeedcba";
str.slice(-6, -2); // "eedc"
```

`str.substr(start, len)`在含义上有所区别。它的第二个参数表示截取的子串长度。

```js
var str = "abcdeedcba";
str.substr(2, 6); // "cdeedc"
str.substr(5); // "edcba"
```

## 字符串替换内容

`str.replace(old, new)`会将`str`中首个匹配`old`的子串替换为`new`。

该方法默认只替换首个匹配，默认大小写敏感。如果需要全部替换，或者大小写敏感，请使用正则表达式。

```js
var str = "Play Mental Omega";
str.replace("Mental Omega", "Genshin Impact"); // "Play Genshin Impact"

str = "bee sea BEE dee a bee"
str.replace(/BEE/i, "ef"); // "ef sea BEE dee a bee"
str.replace(/bee/g, "ef"); // "ef sea BEE dee a ef"
```

## 大小写切换

- `str.toUpperCase()`
- `str.toLowerCase()`

## 字符串拼接

`str = str.concat(str1, str2, ...);`

等价于

`str = str + str1 + str2 + ...;`

## 去除两边空格

```js
"   lol   ".trim() // "lol"
```

## 随机访问

- `str.charAt(idx)`：返回索引为`idx`的字符。
- `str.charCodeAt(idx)`：返回索引为`idx`字符的Unicode编码。
- `str[idx]`：直接属性访问。与前两种方法相比不安全。

```js
// 以下几种方法等效。
var str = "12你好34";
str.charAt(2); // "你"
str.charCodeAt(2); // 20320
str[2]; // "你"

// 越界访问
str.charAt(8); // ""
str.charCodeAt(8); // NaN
str[8]; // undefined
```

## 字符串切分为数组

`str.split(delimiter)`会以每个`delimiter`为切割点，切割`str`为一系列子串。

```js
var str = "aababaabbaaba";
str.split("b"); // ["aa", "a", "aa", "", "aa", "a"]
```

## 字符串模板

字符串模板使用反引号包裹。

模板性质：
- 内部允许使用单双引号
- 允许内部无转义换行
- 支持字符串插值语法

```js
var schools = ["Tsinghua", "Peking", "Zhejiang", "Tongji"];

for (const x of schools) {
	console.log(`Welcome to ${x} University!`);
}
```