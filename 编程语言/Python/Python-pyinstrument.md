
pyinstrument可分析一段程序内各段的用时，找出耗时较长的部分。

```sh
$ pip install pyinstrument
```

## demo

```python
from pyinstrument import Profiler

def some_complicated_func():
	# 定义Profiler
	profiler = Profiler()
	profiler.start()

	# 中间进行一些耗时操作

	# 函数的末尾，执行stop
	profiler.stop()
	profiler.print()
```

输出类似于如下格式：

```

  _     ._   __/__   _ _  _  _ _/_   Recorded: 18:01:03  Samples:  10289
 /_//_/// /_\ / //_// / //_'/ //     Duration: 40.880    CPU time: 1776.267
/   _/                      v5.0.1

Profile at /root/workspace/video_enhance/main_v3.py:97

40.879 enhance  main_v3.py:89
└─ 40.867 enhance_video  main_v3.py:40
   ├─ 38.269 enhance_frame  main_v3.py:20
   │  ├─ 36.841 decorate_context  torch/utils/_contextlib.py:112
   │  │  └─ 36.803 RealESRGANer.enhance  realesrgan/utils.py:193
   │  │     ├─ 11.768 Tensor.cpu  <built-in>
   │  │     ├─ 10.293 RealESRGANer.process  realesrgan/utils.py:113
   │  │     │  └─ 10.293 RRDBNet._wrapped_call_impl  torch/nn/modules/module.py:1528
   │  │     │        [20 frames hidden]  torch, basicsr, <built-in>
   │  │     ├─ 5.700 [self]  realesrgan/utils.py
   │  │     ├─ 5.384 resize  <built-in>
   │  │     ├─ 2.445 ndarray.round  <built-in>
   │  │     └─ 0.979 ndarray.astype  <built-in>
   │  ├─ 0.873 RealESRGANer.__init__  realesrgan/utils.py:29
   │  └─ 0.553 RRDBNet.__init__  basicsr/archs/rrdbnet_arch.py:87
   │        [3 frames hidden]  basicsr
   └─ 2.564 [self]  main_v3.py
```

