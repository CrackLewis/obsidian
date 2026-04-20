
repo: [github-decord](https://github.com/dmlc/decord)

```sh
$ pip install decord
```

## 读取视频

```python
from decord import VideoReader
from decord import cpu
# 创建VideoReader对象
vr = VideoReader('path_to_your_video.mp4', ctx=cpu(0))
# 打印视频帧数
print('video frames:', len(vr))
# 读取指定帧
frames = vr.get_batch([1, 3, 5, 7, 9])
print(frames.shape) # 输出帧的形状
```

## 保存视频帧为图片

```python
import matplotlib.pyplot as plt
# 获取第一帧并转换为numpy数组
frame1 = vr[1].asnumpy()
# 显示并保存图片
plt.imshow(frame1)
plt.axis('off')
plt.savefig("frame1.jpg", bbox_inches='tight')
```

## demo：抽帧脚本

```python
import cv2
import os
from decord import VideoReader, cpu
from tqdm import tqdm

# 视频路径和保存路径
video_path = 'path_to_your_video.mp4'
pic_folder = 'frames'
file_basename = 'frame'
archive_fps = 30

# 定义图像大小调整函数
def resize_image(image):
   height, width = image.shape[:2]
   n_width = int(256 * width / max(width, height))
   n_height = int(256 * height / max(width, height))
   return cv2.resize(image, (n_width, n_height))

# 读取视频
vr = VideoReader(video_path, ctx=cpu(0))
fra_num = len(vr)

# 获取指定帧并进行resize保存
frames = vr.get_batch(list(range(0, fra_num, archive_fps))).asnumpy()
for count, frame in tqdm(enumerate(frames), total=len(frames)):
   frame = resize_image(frame)
   image_name = f"{file_basename}_{count}.jpg"
   cv2.imwrite(os.path.join(pic_folder, image_name), cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
```