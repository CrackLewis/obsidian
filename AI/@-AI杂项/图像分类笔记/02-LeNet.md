
## Prerequisites

- Anaconda3
- PyTorch with available GPUs

参考教程：[Training a Classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#)

## LeNet (1998)

输入->卷积->下采样->卷积->下采样->全连接->全连接->高斯连接

![[Pasted image 20230502133524.png]]

- 输入是灰度图。对于彩色图，需要分R/G/B三个通道

**PyTorch Tensor通道排序：\[batch, channel, height, width\]**

### 导入包

```python
import torch.nn as nn
import torch.nn.functional as F
```

### 搭建LeNet模型

关于PyTorch内各设施的用法，参考PyTorch API。

定义模型和其构造器：

```python
class LeNet(nn.Module):
	def __init__(self):
		super(LeNet, self).__init__()
		# 输入：3@32*32
		self.conv1 = nn.Conv2d(3, 16, 5)
		# 输出：16@28*28
		self.pool1 = nn.MaxPool2d(2, 2)
		# 输出：16@14*14
		self.conv2 = nn.Conv2d(16, 32, 5)
		# 输出：32@10*10
		self.pool2 = nn.MaxPool2d(2, 2)
		# 输出：32@5*5
		self.fc1 = nn.Linear(32*5*5, 120)
		# 输出：120
		self.fc2 = nn.Linear(120, 84)
		# 输出：84
		self.fc3 = nn.Linear(84, 10)
		# 结果：10
```

定义前向传播方法：
```python
...
	"输入x为一张数据图片"
	def forward(self, x):
		x = F.relu(self.conv1(x))
		x = self.pool1(x)
		x = F.relu(self.conv2(x))
		x = self.pool2(x)
		x = x.view(-1, 32*5*5) # 将数据展平为一维
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		x = self.fc3(x)
		return x
```

### 下载数据集

```python
transform = transforms.Compose(
	# 将PIL图像或NumPy图像转化为一个torch tensor
    [transforms.ToTensor(),
    # 用均值和标准差手段来标准化图像：第一个参数为各通道均值，第二个参数为各通道标准差
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

# 50000张训练图片
# 第一次使用时要将download设置为True才会自动去下载数据集
train_set = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=36, shuffle=True, num_workers=0)

# 10000张验证图片
# 第一次使用时要将download设置为True才会自动去下载数据集
val_set = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
val_loader = torch.utils.data.DataLoader(val_set, batch_size=5000, shuffle=False, num_workers=0)
```

测试机载入使用迭代方法：

```python
val_data_iter = iter(val_loader)
val_image, val_label = next(val_data_iter)
```

### 定义模型、损失函数、优化器

```python
net = LeNet()
loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)
```

### 定义训练流程

```python
for epoch in range(5):  # 数据集过5遍
	running_loss = 0.0
    for step, data in enumerate(train_loader, start=0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

		# zero the parameter gradients
		optimizer.zero_grad()
		# forward + backward + optimize
		outputs = net(inputs)
		loss = loss_function(outputs, labels)
		loss.backward()
		optimizer.step()

		# print statistics
		running_loss += loss.item()
		if step % 500 == 499:    # print every 500 mini-batches
			with torch.no_grad():
				outputs = net(val_image)  # [batch, 10]
				predict_y = torch.max(outputs, dim=1)[1]
				accuracy = torch.eq(
					predict_y, val_label).sum().item() / val_label.size(0)

				print('[%d, %5d] train_loss: %.3f  test_accuracy: %.3f' % (epoch + 1, step + 1, running_loss / 500, accuracy))
				running_loss = 0.0

print('Finished Training')
```

### 保存模型

```python
save_path = './Lenet.pth'
torch.save(net.state_dict(), save_path)
```

### 验证

```python
import torch
import torchvision.transforms as transforms
from PIL import Image

from model import LeNet


def main():
    transform = transforms.Compose(
        [transforms.Resize((32, 32)),
         transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    net = LeNet()
    net.load_state_dict(torch.load('Lenet.pth'))

    im = Image.open('1.jpg')
    im = transform(im)  # [C, H, W]
    im = torch.unsqueeze(im, dim=0)  # [N, C, H, W]

    with torch.no_grad():
        outputs = net(im)
        predict = torch.max(outputs, dim=1)[1].numpy()
    print(classes[int(predict)])


if __name__ == '__main__':
    main()
```