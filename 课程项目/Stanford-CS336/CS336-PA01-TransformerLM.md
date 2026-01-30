
breakdowns:
- Byte-Pair Encoding (BPE) tokenizer
- TransformerLM
- cross-entropy + AdamW
- training

## ch02-overview (p2)

why utf8: 效率高，不会因为未处理好未知字符丢失信息

tokenizer级别：word-level > subword-level > character-level > byte-level 
- word-level：最自然；词表巨大，OOV (out-of-vocab) 问题严重，无法处理词形变化
- character-level：词汇表小，无OOV；序列过长，语义丢失
- byte-level：放大了character-level的优势和劣势
- *subword-level*：
	- 目前主流，介于word和character级之间，权衡了词表规模和序列长度
	- 减少了OOV问题，但词汇表规模不易控制，训练成本较高

BPE tokenizer训练（p10-11）：
- 初始化词汇表：初始为character表，即256
- 预分词（pre-tokenize）
	- why：将单词遍历局限在一定区间而非整个语料库；防止不允许的单词合并
	- how：用正则表达式切割文本，令所有的单词合并行为局限于段内
- 迭代合并：
	- 识别出现频率最高的字节对，并对其进行合并
	- 当有若干对字节的频率并列最高时，选取*字典序较大*的一对
- 特殊标记：`</w>`表示单词结束；`<|endoftext|>`表示文本结束。特殊标记永不拆分

## ch03-transformer架构 (p20)

## ch04-transformer训练 (p40)