
ref:
- [博客](https://blog.csdn.net/qq_45062768/article/details/133852543)：讲了一些实用的YOLO训练技巧

labelimg：数据集标注工具

YOLO是一系列的单轮目标检测/定位算法。

```sh
$ pip install ultralytics
```

```python
from ultralytics import YOLO

yolo = YOLO('./models/yolo11s.pt')

yolo.train(data='dataset.yaml', epochs=50, imgsz=640, batch=20)
```

## 指标介绍

| 损失项          | 核心目标       | 关键方法                | 解决的问题      |
| ------------ | ---------- | ------------------- | ---------- |
| **box_loss** | 精确的边界框定位   | IoU变体或分布预测（DFL）     | 物体位置与尺寸误差  |
| **cls_loss** | 准确的类别分类    | 交叉熵/Focal Loss      | 分类错误       |
| **dfl_loss** | 边界框分布的精细调整 | 离散概率分布 + Focal Loss | 复杂场景下的定位模糊 |

## 模型

模型名：`yolo<版本><规模>[-<用途>].pt`
- 版本：低于10的版本为vX，如v5、v8等
- 规模：最小的是n，依次更大的有s、m、l，最大的是x。越大的模型在目标检测/定位等任务的准确率越高，但推理时间也越长
- 用途：seg为实例分割，cls为分类，obb为定向检测，pose为姿势/关键点检测

