
## torch结构

常用的标`*`

```
torch
+ accelerator         # 加速器的通用抽象
+ amp                 # 自动混合精度训练/推理，用于提升 GPU 训练效率、降低显存
+ ao                  # Accelerated/Architecture Optimization 相关包
+ *autograd           # 自动求导系统，构建计算图并反向传播（隐含）
+ backends            # 控制底层后端行为（CUDA/cuDNN/MPS/TF32等）
+ bin                 # 可执行脚本（不常用）
+ compiler            # PyTorch编译链
+ contrib             # 历史/贡献型扩展区域（不常用）
+ cpu                 # CPU相关接口（不常用）
+ csrc                # 
+ *cuda               # CUDA相关接口
+ distributed         # 分布式训练通信包
+ distributions       # 概率分布库
+ export              # 模型导出机制，将模型捕获为更标准化的图表示
+ fft                 # 快速傅里叶变换API
+ func                # 函数变换API
+ futures             # 异步执行结果对象
+ fx                  # Python 级模型图捕获、变换和分析框架
+ include             # C++ 头文件目录，编写C++/CUDA扩展或LibTorch开发时使用
+ jit                 # TorchScript JIT 编译/序列化接口
+ lib                 # 动态库目录
+ linalg              # 线性代数 API
+ masked              # MaskedTensor 或掩码语义相关实验性/原型能力
+ monitor             # 监控和事件记录相关接口
+ mps                 # Apple Silicon / Metal Performance Shaders 后端接口
+ mtia                # Meta Training and Inference Accelerator 接口
+ multiprocessing     # 多进程支持（常用于DataLoader等）
+ nativert            # Native Runtime 相关内部/部署运行时组件
+ nested              # NestedTensor 支持，用于表示变长/嵌套张量
+ *nn                 # 神经网络核心模块，包括module/层/loss/cont/init/fn等
+ numa                # NUMA亲和性/内存布局相关能力
+ onnx                # onnx格式模型导出
+ *optim              # 优化器包
+ package             # PyTorch代码打包工具
+ profiler            # 性能分析工具
+ quantization        # （迁移至torch.ao.quantization）
+ share               # 安装资源共享目录（不常用）
+ signal              # 信号处理相关实验/内部区域
+ sparse              # 稀疏张量和稀疏算子，如 COO/CSR/CSC/BSR/BSC、稀疏矩阵乘法
+ special             # 特殊数学函数，如erf/gamma/bessel/softmax等
+ testing             # 测试工具
+ types               # 类型标注辅助定义
+ *utils              # 工具集合，最常用dataset/dataloader/tensorboard等
+ version             # 版本信息
+ xpu                 # Intel GPU/XPU后端接口
```

按分类：

```
日常建模：torch / nn / optim / autograd / utils.data
GPU训练：cuda / amp / backends
多卡训练：distributed / multiprocessing
性能优化：compile / compiler / profiler / fx
部署导出：export / onnx / jit / package
数学扩展：linalg / fft / special / distributions / sparse
硬件后端：cuda / mps / xpu / accelerator / mtia
内部目录：csrc / include / lib / bin / share
```

最常用：
- torch.nn
- torch.optim
- torch.autograd
- torch.utils.data
- torch.cuda

## torch.nn结构

