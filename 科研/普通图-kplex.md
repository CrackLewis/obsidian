
## LijunChang-Efficient maximum k-plex computation

问题：maximum k-plex prob'

核心工作：
- 新的最大k-plex计算框架
- core-truss co-pruning（CTCP）算法：提取一个小规模子图
- BBMatrix算法：针对从输入图提取的密集子图进行分支限界，使用一阶和二阶信息进行upper-bounding和pruning

有关工作：P2右下
- 最大k-plex计算
- 最大k-plex枚举
- clique计算

*计算框架核心内容*：

