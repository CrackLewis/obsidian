
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
- codec：编解码器。packet内并不能直接提取帧信息，需要先进行解码，同理frame转换为packet也需要编码

## demo：查看视频信息

```python
import av

container = av.open('./test.mp4')
vstream = next(s for s in container.streams if s.type == 'video')
astream = next((s for s in container.streams if s.type == 'audio'), None)
```

Work In Progress