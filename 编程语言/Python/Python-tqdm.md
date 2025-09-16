
一个支持命令行/Jupyter上显示的进度条

```sh
$ pip install tqdm
```

## demo：迭代式进度条

```python
from tqdm import tqdm
import time

pbar = tqdm(range(300))

for i in pbar:
    time.sleep(.01)
```

优点：方便

缺点：无法较灵活地控制进度，每轮循环只推进1个进度

## demo：自定义显示、非迭代式推进

```python
unit = 'step(s)'
desc = 'A tqdm demo'
total = 10

pbar = tqdm(range(total), desc=desc, unit=unit)

# 注意这里不再对pbar进行迭代
for i in range(total):
	time.sleep(1)
	# 想让进度条推进，必须执行update
	pbar.update(1)

# 如果进度条需要中止，则需要调用close
# pbar.close()
```