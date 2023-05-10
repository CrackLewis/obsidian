
异步相对于同步，是一种非顺序式控制流。

例如：`setTimeout(func(), msecs)`允许用户在`msecs`毫秒后执行`func()`函数。

## 回调函数

回调是作为参数传递给另一个函数的函数。

回调参数允许用户对函数的功能进行抽象，并根据不同情形传递不同回调函数，以实现不同的功能。

```js
function myCalculator(num1, num2, myCallback) {
  let sum = num1 + num2;
  myCallback(sum);
}

function alertDisplayer(x) {
	alert(some);
}

function demoDisplayer(x) {
	document.getElementById("demo").innerHTML = x;
}

myCalculator(5, 5, alertDisplayer);
myCalculator(5, 5, demoDisplayer);
```

回调函数的主要应用在于与异步函数的共同使用。

## Promise对象

生产代码：需要一些时间执行的代码

消费代码：必须等待结果的代码

Promise对象是内置的、可以链接生产代码和消费代码的对象。

```js
let my_promise = new Promise((my_resolve, my_reject) => {
	let x = 0;
	for (let i = 1; i <= 100; ++i) {
		x += i;
	}
	if (x === 5050) my_resolve(x);
	else my_reject("bad result");
});

my_promise.then(
	(x) => { console.log(x); },
	(errmsg) => { console.log(errmsg); }
);
```

Promise使用的要点：
- `Promise`对象定义时传入的参数应有如下要求：
	- 必须是函数对象
	- 必须有两个回调形参，名称无所谓：
		- 第一个形参：指定异步操作成功后执行的操作，俗称`resolve`函数
		- 第二个形参：指定异步操作失败后执行的操作，俗称`reject`函数
	- 函数体内应分为两个阶段：
		- 第一个阶段：执行**生产代码**，即执行一些耗时操作，得到结果
		- 第二个阶段：根据结果，调用`resolve`或`reject`函数返回
- `Promise`对象定义和`Promise.then`之间可以执行一些**消费代码**
- `Promise.then`方法原则上必须调用，有如下要求：
	- 调用时机在消费代码结束后，等待生产代码的结果
	- 原则上有两个函数形参，如果不希望处理错误，可以只有一个：
		- 会分别被传入定义时的两个回调形参
		- 参数应当和定义时`resolve`和`reject`的参数列表一致

### Promise内部成员

`Promise.state`：Promise状态
`Promise.result`：Promise结果

状态：
- `"pending"`：处理中
- `"fulfilled"`：处理完毕，符合预期
- `"rejected"`：处理完毕，异常

结果：若状态处理中则为`undefined`，否则为结果值或error

### Promise的一些实例

等待文件：

```js
let myPromise = new Promise(function(myResolve, myReject) {
  let req = new XMLHttpRequest();
  req.open('GET', "mycar.htm");
  req.onload = function() {
    if (req.status == 200) {
      myResolve(req.response);
    } else {
      myReject("File not Found");
    }
  };
  req.send();
});

myPromise.then(
  function(value) {myDisplayer(value);},
  function(error) {myDisplayer(error);}
);
```

加载图像：

```js
const loadImage = url => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      resolve(img);
    };
    img.onerror = () => {
      reject(`Failed to load image ${url}`);
    };
    img.src = url;
  });
};

// 使用Promise加载图像
loadImage('https://www.example.com/image.jpg')
  .then(img => {
    console.log('Image loaded successfully');
    // 在这里使用图像
  })
  .catch(error => {
    console.error(error);
  });

```

## JS async & await

**@since ES2017**

Promise对象的问题在于写起来繁琐。代码里充斥大量的Promise会极大降低可读性。

`async`关键字可修饰函数，使该函数返回Promise；`await`关键字可修饰函数，使该函数等待Promise。

下面两个声明等效：
```js
async function myFunction() {
  return "Hello";
}

async function myFunction() {
  return Promise.resolve("Hello");
}
```

处理`async`返回值：
```js
async function myFunction() {
  return "Hello";
}
myFunction().then(
  function(value) {myDisplayer(value);},
  function(error) {myDisplayer(error);}
);
```

`await`修饰一个`Promise`变量，使函数等待该变量出现结果。该关键字只能在`async`函数中使用。

下面是一个加载文件的实例：

```js
async function getFile() {
  let myPromise = new Promise(function(myResolve, myReject) {
    let req = new XMLHttpRequest();
    req.open('GET', "mycar.html");
    req.onload = function() {
      if (req.status == 200) {myResolve(req.response);}
      else {myResolve("File not Found");}
    };
    req.send();
  });
  document.getElementById("demo").innerHTML = await myPromise;
}

getFile();
```