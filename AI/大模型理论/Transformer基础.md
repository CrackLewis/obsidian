
 Transformer：
 - 注意力机制：
	 - 自注意力
	 - 注意力掩模
	 - 多头注意力
 - 位置编码
 - 残差连接
 - Encoder/Decoder
	 - Encoder：多头自注意力--AddNorm--FFN--AddNorm
	 - Decoder：多头掩模自注意力--AddNorm--多头注意力--AddNorm--FFN--AddNorm
 - 