
## 简介

Vue Router是Vue的一个插件库，专用于实现SPA（single-page application，单页面应用）。

单页面应用VS传统应用：

| 项目     | SPA              | 传统应用          |
| ------ | ---------------- | ------------- |
| 应用形式   | 单个浏览器页面          | 多个页面，会话由浏览器维护 |
| 点击导航链接 | 不会刷新页面，会做页面的局部更新 | 可能会刷新页面       |
| 获取数据   | ajax请求           | ajax或重定向      |

什么是路由：
- 一个路由就是一组`k-v`映射关系，`k`是路径，`v`是组件或函数
- 分类：
	- 前端路由：`v`是组件，用于展示页面内容。路径改变时组件重新加载
	- 后端路由：`v`是函数。请求到达后端时，匹配到一个窗口函数处理请求，并返回响应数据

## 基本路由

Vue2对应的是`vue-router@3`，Vue3对应的是最新的vue-router 4版本。

```sh
npm install vue-router
```

在路由JS文件（`src/router/index.js`）中，编写路由对象：

```js
import VueRouter from 'vue-router';
import About from '../components/About';
import Home from '../components/Home';

const router = new VueRouter({
	routes: [
		{
			path: '/about',
			component: About
		},
		{
			path: '/home',
			component: Home
		}
	]
});

export default router;
```

Vue页面中使用`router-link`生成一个路由链接：

```vue
<router-link active-class="active" to="/about">About</router-link>
```

`router-view`元素会在点击路由链接后加载路由对应的组件（如点击`About`则加载`About.vue`组件中的内容。

```vue
<router-view></router-view>
```

注意事项：
- 通过点击路由链接才能加载的组件一般和普通组件区分开，前者一般存储在`src/pages`中，后者存放在`src/components`中。
- 切换前后，先前加载的旧组件默认被销毁。
- 组件内可以通过`this.$route`访问自己的路由信息。
- 整个应用只允许有一个`router`，通过`this.$router`属性访问。

## 多级路由

路由对象允许通过`children`指定下一级路由：

```js
const router = new VueRouter({
	routes: [
		{
			path: '/about',
			component: About
		},
		{
			path: '/home',
			component: Home,
			children: [
				{
					path: 'news',
					component: News
				},
				{
					path: 'message',
					component: Message
				}
			]
		}
	]
});
```

路由链接中要写完整路径：

```vue
<router-link to="/home/news">News</router-link>
```

## query参数

路由组件有可能需要传入数据，就像props属性一样。

RESTful写法：

```vue
<router-link :to="`/home/message/detail?id=${m.id}&title=${m.title}`">
	跳转
</router-link>
```

对象写法：

```vue
<router-link :to="{
		path: '/home/message/detail', 
		query: {
			id: m.id,
			title: m.title
		}
	}">
	跳转
</router-link>
```

被加载的组件通过`this.$route.query.xxx`访问query参数：

```js
this.$route.query.id
```

## 命名路由

如果路由名又臭又长，则可以给路由起别名，在`router-link`中可以采用别名。

```js
const router = new VueRouter({
	routes: [
		{
			path: '/demo',
			component: Demo,
			children: [
				{
					path: 'test',
					component: Test,
					children: [
						{
							// 这里给/demo/test/welcome路由起了别名hello
							name: 'hello',
							path: 'welcome',
							component: Hello
						}
					]
				}
			]
		}
	]
});
```

以下两个路由链接是等价的：

```vue
<router-link to="/demo/test/welcome">跳转</router-link>

<router-link :to="{name: 'hello'}">跳转</router-link>
```

## params参数

params参数用于支持可变路由，即路由中的部分路径可变，格式类似`/path/to/:var`。

```js
export default new VueRouter({
   routes:[
       {
           path:'/home',
           component: Home,
           children:[
               {
                   path: 'message',
                   component: Message,
                   children:[
                       {
                           name: 'particulars',
                           path: 'detail/:id/:title',
                           component: Detail
                       }
                   ],
               }
           ]
       }
   ]
});
```

路由链接支持以下两种写法。**注意**：如果使用对象写法，则对象内必须使用name，不能使用path。

```vue
<router-link :to="`/home/message/detail/${m.id}/${m.title}`">
	{{ m.title }}
</router-link>

<router-link
	:to="{
	  // path:'/home/message/detail',
	  name: 'particulars', //利用路由名字直接跳转路由简化多级路由的path配置
	  //注意如果你这里使用params传递参数,不能配置path，只能配置name,一定要注意
	  params: {
		id: m.id,
		title: m.title
	  }
	}">
	{{ m.title }}
</router-link>
```

获取参数可以通过`this.$route.params.xxx`获取。

## props配置

路由的params配置提供了更方便地传递路由参数的方法。

```js
export default new VueRouter({
	name: 'xiangqing',
	path: 'detail/:id',
	component: Detail,

	// 写法一：对象写法。该对象的所有k-v都会传给组件Detail
	// props: { a: 1, b: 'hello' },

	// 写法二：默认写法。意思是，把所有params参数传给组件Detail
	// props: true,

	// 写法三：函数写法。从函数参数提取参数并返回，返回值会被传给组件Detail
	props($route) {
		return {
			id: $route.query.id,
			title: $route.query.title
		};
	}
});
```

