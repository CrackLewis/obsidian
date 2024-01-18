
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
  get() { console.log("get obj2.x"); return obj.x; },
  set(value) { console.log("set obj2.x=" + value); obj.x = value; }
})
```

Vue中的数据代理：
- 通过`vm`对象来代理`data`对象中属性的操作（读和写）
- 好处是更加方便地操作`data`中的数据

