
## MVVM模型

MVVM=Model+View+ViewModel
- M：模型，对应data中的数据
- V：模板
- VM：对应Vue实例对象

![[Pasted image 20240117232024.png]]

通过下面的例子注意到：
- `data`的所有属性都出现在了`vm`上。
- `vm`属性和`Vue`原型的所有属性，都能被Vue模板直接使用。

```html
<body>
  <div id="demo">
    <h2>名称：{{ name }}</h2>
    <h2>地址：{{ address }}</h2>
    <h2>属性测试：{{ $options }}</h2>
  </div>

  <script type="text/javascript">
    Vue.config.productionTip = false; 

    const x = new Vue({
      el: "#demo", 
      data: {
        name: "CrackLewis",
        address: "shanghai"
      }
    });
  </script>
</body>
```

![[Pasted image 20240118105851.png]]

## Vue数据代理

JS自带的`Object.defineProperty`方法可以实现相对简单的数据代理功能。下面的示例可以将对`obj2.x`的赋值和读取转化为对`obj.x`的实际修改。

```js
let obj = { x: 100 };
let obj2 = { y: 200 };

Object.defineProperty(obj2, 'x', {
  // value:1, // 配置数值
  // enumerable:false, // 控制obj2.x是否为可枚举，默认false
  // writable:false,  // 控制obj2.x是否为可写入，默认false
  // configurable:false, // 控制obj2.x是否可被删除，默认false
  get() { console.log("get obj2.x"); return obj.x; },
  set(value) { console.log("set obj2.x=" + value); obj.x = value; }
})
```

![[Pasted image 20240118112923.png]]

Vue中的数据代理：
- 通过`vm`对象来代理`data`对象中属性的操作（读和写）
- 好处是更加方便地操作`data`中的数据

Vue数据代理的原理：
- 通过`Object.defineProperty`将`data`对象中所有属性添加到`vm`上
- 为每一个添加到`vm`上的属性，都指定一个`getter`和`setter`
- 在`getter`、`setter`内部操作（读写）`data`中对应的属性

![[Pasted image 20240118111456.png]]

也就是说，模板在访问某一数据成员时，实际访问的是`vm._data`中的成员，而这些成员通过数据代理机制，通过`vm`对象暴露给程序员，即`const vm = new Vue({ data: { attr: 1 } })`后，可通过`vm.attr`读写`vm._data.attr`属性。

