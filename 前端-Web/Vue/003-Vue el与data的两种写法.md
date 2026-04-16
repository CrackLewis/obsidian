
`el`的两种写法：
- 创建时配置：`new Vue({ el: "#root", ... })`
- 创建后配置：先创建Vue实例`vm`，再执行`vm.$mount("#root")`。这个方法允许异步配置，更灵活一点。

`data`的两种写法：
- 对象式写法：`data: {}`。涉及组件时不能用这种写法！
- 函数式写法：`data() { ...; return {...}; }`。注意不能写成箭头函数，否则`this`就不再是Vue实例了！

示例：之前的el和data都是创建时配置、对象式写法，这里来一个创建后配置、函数式写法。

```html
<body>
  <div id="root">
    <!-- 插值语法：JS表达式 -->
    <h1>Hello, {{ name.toUpperCase() }}, {{ address }}!</h1>
  </div>

  <script type="text/javascript">
    Vue.config.productionTip = false; // 取消生产环境警告

    // 构造Vue对象
    const x = new Vue({
      // 这里暂不指定el
      data: function () { // 后续必须是函数式，且不能是lambda
        console.log("@@@", this); // 此处的this是Vue实例对象x
        return { // 规定必须返回对象
          name: "CrackLewis",
          address: "shanghai"
        };
      }
    });
    x.$mount("#root"); // 这一步才会将Vue实例和对象链接
  </script>
</body>
```

界面和控制台显示正常：

![[Pasted image 20240117231013.png]]