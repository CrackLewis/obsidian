
```sh
$ pip install pyav
```

PyAV基于FFmpeg的部分库实现视频处理。

## 核心概念

- container：容器。储存一整个视频的所有内容
- stream：流。是容器内的一条通道，可能为：
	- 视频流（video stream）：存储一系列视频帧
	- 音频流（audio stream）：存储一系列音频帧
	- 字幕流（subtitle stream）或其他
- packet：包。是数据在容器内的存放方式，一般是编码好的音视频或字幕文本
- frame：帧。一个packet包含0至任意多帧的信息，每帧存储一幅图像、一段音频或一段字幕
	- VideoFrame：视频帧
	- AudioFrame：音频帧
- codec：编解码器。packet内并不能直接提取帧信息，需要先进行解码，同理frame转换为packet也需要编码

### av.AudioFrame

单个音频帧的实例。

方法成员：
- `to_ndarray`：转换为NumPy数组
- `from_ndarray`：将NumPy数组加载到帧内
- `make_writable`：确保帧可写，防止写入共享区域导致错误

数据成员：
- 时间相关：
	- `dts`：解码时间戳（decode timestamp）
	- `pts`：播放时间戳（presentation timestamp）。音频帧一般满足dts=pts
	- `time_base`：该帧采用的时间单元
	- `time`：该帧播放的时刻，一般为`pts * time_base`
- 速率：
	- `sample_rate`：音频帧的采样率（每秒采样次数）
		- 个人在实践中发现`sample_rate`基本是time\_base倒数
	- `rate`：音频帧所在流的采样率
- `format`：音频格式`av.AudioFormat`，如fltp、aac等
- `is_corrupt`：是否为坏帧
- `key_frame`：是否为关键帧
- `layout`：`av.AudioLayout`，表示音频的通道信息
- `opaque`：上下文数据
- `planes`：平面数据（planar data），对应一或多个声道的数据
- `samples`：采样数
- `side_data`：附加数据

### av.VideoFrame

单个视频帧的实例。

方法成员：

数据成员：
- 时间相关：
	- `dts`：解码时间戳
	- `pts`：播放时间戳。可能和dts不同，后面详解
	- `time`：该帧播放的时刻，一般为`pts * time_base`
	- `time_base`：该帧采用的时间单元
- 尺寸：
	- `width`、`height`：图像实际尺寸
- `format`：图像格式，`av.VideoFormat`
- `color_range`
- `colorspace`
- `interlaced_frame`：表示视频帧是否是隔行扫描（interlaced）的。
	- 隔行扫描帧由两个场（field）组成，分别包含奇数行和偶数行
	- 在去隔行（deinterlacing）处理时有大用
- `is_corrupt`：是否为坏帧
- `key_frame`：是否关键帧
- `opaque`：上下文数据
- `pict_type`：描述该帧的时序类型，后面详解
- `planes`：平面数据（planar data），对应一或多个图像通道的数据
	- 灰度图只有1个plane，RGB图有3个planes
- `rotation`：旋转角度（以度为单位）
- `side_data`：附加数据

#### 视频帧的时序

视频帧按照解码/播放时序，分为三类：
- I帧（关键帧）
- P帧（预测帧）
- B帧（双向预测帧）

I帧的pts一般等于dts，即解码时刻=播放时刻

P帧是预测帧，它存储的是与前一帧相比*图像的变化量*，只有离它最近的一个I帧及之后全部P帧都成功解码，它才能成功解码。所以P帧的pts\>dts

B帧是双向预测内插编码帧，需要参考前后的I帧或P帧来解码。因此B帧的pts\<dts。

### av.Packet

packet是从视频内demux出来的媒体包。它一般编码了一段视频或音频帧

## demo：查看视频信息

```python
import av

container = av.open('./test.mp4')
vstream = next(s for s in container.streams if s.type == 'video')
astream = next((s for s in container.streams if s.type == 'audio'), None)
```

Work In Progress