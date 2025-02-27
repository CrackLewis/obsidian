
## 简介

Vuex是一种在Vue中进行集中式状态/数据管理的插件。

使用时机：
- 多个组件依赖于同一状态
- 来自不同组件的行为需要变更同一状态

旧式集中数据管理：数据存储在单个组件中，靠事件总线机制进行数据读写。

![](https://cdn.nlark.com/yuque/0/2022/png/1379492/1643034632699-15503880-2c10-44e1-bf8f-c088d0896ba6.png)

Vuex数据管理：

![](https://cdn.nlark.com/yuque/0/2022/png/1379492/1643034632949-1f50dc65-b44d-4b00-bed1-10222a2e87e5.png)

## 案例：求和

项目结构：

```
src/
+ components/
	+ Count.vue    # 求和组件
+ store/
	+ index.js     # 描述项目的公共存储结构
+ App.vue
+ main.js
```

`src/components/Count.vue`：

```vue
<template>
  <div>
    <h1>当前求和为: {{ sum }}</h1>
    <!--让其收集到的数据全是number类型的 number修饰符-->
    <h3>当前求和放大3倍为:{{ bigSum }}</h3>
    <h3>我在{{ school }}, 学习{{ subject }}</h3>
    <select v-model.number="n">
      <!--让所有的value全部绑定为数字-->
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
    </select>
    <button @click="increment(n)">+</button>
    <button @click="decrement(n)">-</button>
    <button @click="incrementIfOdd(n)">当前求和为奇数再加</button>
    <button @click="incrementWait(n)">等一等再加</button>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions} from 'vuex';
export default {
  //计数组件
  name: "Count",
  data(){
    return {
      n: 1,// 代表用户在select框开始的时候选择的数字
    }
  },
  computed:{
    //借助mapState从state中生成计算属性,对象写法
    // ... mapState({
    //   sum:'sum',
    //   school: 'school',
    //   subject: 'subject'
    // }),
    //借助mapState从state中生成计算属性,数组写法(即代表了生成的计算属性名为sum，同时也代表了从state找到sum)
    ... mapState(['sum', 'school', 'subject']),

    //借助mapGetters从getters中生成计算属性,对象写法
    // ...mapGetters({ bigSum: 'bigSum' }),
    //借助mapGetters从getters中生成计算属性,数组写法
    ...mapGetters(['bigSum']),

  },
  methods:{
    // increment(){
    //   this.$store.commit('INCREMENT', this.n);
    // },
    // decrement(){
    //   this.$store.commit('DECREMENT', this.n);
    // },
    //借助mapMutations生成对应方法，方法会调用commit去联系mutations，对象写法
    ...mapMutations({
      increment: 'INCREMENT',
      decrement: 'DECREMENT',
    }),
    //借助数组写法生成方法,但注意你生成的方法名和mutations里对应的方法名将会一样的
    // ...mapMutations(['increment', 'decrement']),

    // incrementOdd(){
    //   this.$store.dispatch('incrementIfOdd', this.n);
    // },
    // incrementWait(){
    //   this.$store.dispatch('incrementWait', this.n);
    // }

    //借助mapMutations生成对应方法，方法会调用dispatch去联系actions，对象写法
    // ...mapActions({
    //   incrementIfOdd: 'incrementIfOdd',
    //   incrementWait: 'incrementWait',
    // }),

    ...mapActions(['incrementWait', 'incrementIfOdd']), //数组写法,同上
  },
}
</script>

<style scoped>
   button{
     margin-left: 5px;
   }
</style>
```

`src/store/index.js`：

```js
/**
 * 该文件用于创建vuex中最核心的store
 */

//引入Vuex
import Vuex from 'vuex';
import Vue from "vue";

//使用vuex来集中管理状态,必要
//new store的前提是必须要使用Vuex插件
Vue.use(Vuex);

//创建actions(本质就是对象) 用于响应组件中的动作
const actions = {
    //收到上下文对象(包含commit)和dispatch过来的值
    // increment(context, value){
    //     context.commit('INCREMENT', value);
    // },
    // decrement(context, value){
    //     context.commit('DECREMENT', value);
    // },
    incrementIfOdd(context, value){
        // console.log(`action中的incrementIfOdd被调用`);
        // console.log('处理了一些事情');
        // context.dispatch('demo1', value);
        if(context.state.sum % 2) {
            console.log('@')
            context.commit('INCREMENT',value);
            // context.state.sum += 1;//这样可以实现但是记住本次对状态的改变开发者工具将无法捕获，因为开发者工具是对mutations对话的
        }
    },
    incrementWait(context, value){
        setTimeout(() => {
            context.commit('INCREMENT', value);
        },500)
    },
    // demo1(context, value){
    //     console.log('处理了一些事情---demo1');
    //     context.dispatch('demo2', value);
    // },
    // demo2(context, value){
    //     console.log('在action的demo中完成最终的逻辑');
    //     if(context.state.sum % 2) {
    //         console.log('@')
    //         context.commit('INCREMENT',value);
    //     }
    // }
}

//创建mutations(本质也是对象) 用于修改数据(state)
const mutations = {
    //收到state和要操作数value
    INCREMENT(state, value) {
        state.sum += value;
    },
    DECREMENT(state, value) {
        state.sum -= value;
    },
}

//准备getters用于加工state，将其共享于各个组件当中
const getters = {
    bigSum(state){
        return state.sum * 10;
    }
}

//准备state(数据) 存储数据
//类似于各个组件里的computed(计算属性),只不过它是共享的
const state = {
    sum: 0,
    school: 'Wust',
    subject: 'Computer Science',
}

//创建并暴露store
export default new Vuex.Store({
    actions,
    mutations,
    state,
    getters
});
```

`src/App.vue`：

```vue
<template>
   <div>
     <Count/>
   </div>
</template>

<script>
import Count from "@/components/Count";
export default {
  name: "App",
  components:{
    Count
  },
  mounted() {
    console.log('App', this);
  }
}
</script>

<style lang="css" scoped>
</style>
```

`src/main.js`：

```js
//引入Vue
import Vue from "vue";
//引入App
import App from './App';
//引入store
import store from './store';

//关闭Vue的生产提示
Vue.config.productionTip = false;

new Vue({
    el: '#app',
    store,
    render: h => h(App),
});
```

## 引入Vuex

Vue2引入Vuex方式：

```js
// src/store/index.js
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

// ...

export default new Vuex.Store({
	// ...
});

// src/main.js
import Vue from "vue";
import store from "./store";
import App from "./App";

new Vue({
	el: "#app",
	// 在Vue实例中引入成员
	store,
	render: h => h(App)
});
```

Vue3引入Vuex：
- `Vue.use(Vuex)`不再使用。
- 创建Vue实例：`createApp(App).use(store).mount("#app");`。

## Vuex写法

`Vuex.Store`的四个核心成员：
- `actions`：一组响应组件中用户动作的函数。这些函数只能调用
- `mutations`：一组修改`state`中变量数据的函数
- `state`：数据容器
- `getters`：一组加工`state`数据的函数

## 4个map方法

`mapState`：映射state的数据为计算属性。

```js
// 这两段是等价的，其他3个map函数同理

export default {
	computed: {
		// 实例内属性名 : "state成员名"
		...mapState({ sum: "sum", school: "school", subject: "subject" })
	}
}

export default {
	computed: {
		...mapState(["sum", "school", "subject"])
	}
}
```

`mapGetters`：映射getters为计算属性。

```js
export default {
	computed: {
		...mapGetters(["bigSum"])
	}
	// 组件内通过this.bigSum访问
	// 模板通过bigSum访问
}
```

`mapActions`：映射actions为成员方法。

```js
export default {
	methods: {
		...mapActions(["incrementIfOdd", "incrementWait"])
	}
	// 组件内通过this.xxx访问
	// 模板通过方法名访问
}
```

`mapMutations`：映射mutations为成员方法。

```js
export default {
	methods: {
		...mapMutations({
			increment: 'INCREMENT',
			decrement: 'DECREMENT'
	    });
	}
}
```

## 模块化、命名空间

Vuex允许由数个不同的模块组成数据，每个模块有一套自己的`state`、`getters`、`actions`、`mutations`。

```js
// src/store/submodule1.js
export default Vuex.Store({
	namespaced: true, // 重要！
	state: {},
	getters: {},
	actions: {},
	mutations: {}
};
```

Vuex的根文件则负责合并这些模块：

```js
// src/store/index.js
import Vuex from "vuex";
import submod1 from "./submodule1";
// 其他模块...

export default new Vuex.Store({
	modules: {
		submod1,
		// 其他模块...
	}
});
```

组件内访问state：

```js
// 第一种方式
this.$store.state.submod1.data1;
// 第二种方式
...mapState('submod1', ['data1'])
```

组件内访问getters：

```js
this.$store.getters['submod1/getter1'];
...mapState('submod1', ['getter1']);
```

组件内调用dispatch：

```js
this.$store.dispatch('submod1/action1', payload);
...mapActions('submod1', ['action1'])(payload);
```

组件内调用commit：

```js
this.$store.commit('submod1/mutation1', payload);
...mapMutations('submod1', ['mutation1'])(payload);
```