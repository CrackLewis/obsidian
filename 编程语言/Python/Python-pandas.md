
FireDucks是一个基于GPU的pandas实现，速度更快，但为闭源库

## 基本概念

- series：一个数据列，包含标签和一列数据
- dataframe：一个数据表，由若干列及其数据组成

## 索引

Series索引：
- `loc[rows, columns]`：标签索引
- `iloc[row_idxs, column_idxs]`：位置索引