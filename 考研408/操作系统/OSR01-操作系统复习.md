
## 进程调度算法

### 评价指标

- CPU利用率
- 系统吞吐量
- 周转时间：
	- 作业周期
	- 多作业指标：平均周转时间、带权周转时间、平均带权周转时间
	- 等待时间、响应时间

### 七种调度算法

![[Pasted image 20230906152735.png]]

**优先级调度算法**：
- 静态优先级、动态优先级
- 优先级的一般规律：
	- I/O密集型>CPU密集型
	- 系统进程>用户进程
	- 交互型进程>非交互型进程

**多级队列调度算法**：根据作业或进程类型或性质的不同，设置多个就绪队列，每个队列采用不同的调度算法。

## 互斥实现方法

- 软件方法：
	- 单标志法：依赖其他进程先执行
	- 双标志法先检查：可能同时进入
	- 双标志法后检查：可能互相谦让
	- Peterson算法：
- 硬件方法：中断屏蔽、硬件指令方法（TestAndSet、Swap）
- 互斥锁、信号量
- 管程

### Peterson算法

既设置flag数组，也设置turn。既不会饥饿，也可以互斥访问。

Pi进程：
```cpp
flag[i]=1;turn=j;//turn的设置明确了只有一个flag有意义，避免了饥饿
while(flag[j]&&turn==j);//flag的设置明确了谁能进入互斥区
work();
flag[i]=0;
afterwork();
```

Pj进程：
```cpp
flag[j]=1;turn=i;
while(flag[i]&&turn==i);
work();
flag[j]=0;
afterwork();
```

### 管程

```cpp
monitor Demo {
	data_structure S;
	condition x;
	init_code() { //...
	}
	take_away() {
		if(S<=0) x.wait();
		//allocate on S
	}
	give_back() {
		//deallocate on S
		if(有进程等待) x.signal();
	}
}
```

## 银行家算法

[[OS02-进程管理#死锁避免措施]]

## 同步和互斥的应用问题

