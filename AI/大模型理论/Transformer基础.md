
 Transformer：
 - 注意力机制：
	 - 自注意力
	 - 注意力掩模（因果注意力）
	 - 多头注意力
	 - 基于架构、算法等因素的优化
 - 位置编码：
	 - 正弦余弦编码
	 - [[RoPE]]
 - 残差连接
 - Encoder/Decoder
	 - Encoder：多头自注意力--AddNorm--FFN--AddNorm
	 - Decoder：多头掩模自注意力--AddNorm--多头注意力--AddNorm--FFN--AddNorm
 - 归一化