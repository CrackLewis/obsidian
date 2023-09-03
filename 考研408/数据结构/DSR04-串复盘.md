
## 框架

- 串的模式匹配算法
	- 暴力匹配法
	- KMP算法：部分匹配值表、next数组、next函数的推理过程
	- nextval数组

## KMP算法

### 部分匹配值（PM）表

子串`S[1...n]`的部分匹配值是满足`S[1...k]==S[n-k+1...n]`且`k<n`的最大值，即前后缀匹配的最大长度。

如，`ababa`的部分匹配值数列为`[0,0,1,2,3]`，`abcac`的部分匹配值数列为`[0,0,0,1,0]`。

### 利用模式串的PM表匹配文本串

设模式串为`P=abcac`，文本串为`T=ababcabcacbab`。`P`的PM表为`[0,0,0,1,0]`。

匹配思想是：`P`的开头对齐`T`的开头，逐字符对照，如果发生失配，则将模式串右移`k`个位置，其中`k=已匹配的字符数-最后一个匹配位置的PM值`。移动后，从头重新开始匹配，即已匹配字符数清零。

第一趟匹配，从头开始，在`T[2]`处失配。

```
a b a b c a b c a c b a b
a b c
    ^
```

右移`k=2-0=2`个位置，第二趟匹配，在`T[6]`处失配。

```
a b a b c a b c a c b a b
    a b c a c
            ^
```

右移`k=4-1=3`个位置，第三趟匹配，匹配成功。

```
a b a b c a b c a c b a b
          a b c a c
```

### next数组

在运用PM表进行模式串匹配时，在模式串第`j`个字符失配的解决方法是：`Move=(j-1)-PM[j-1]`，这样使用略有不便。

令`next[j+1]=PM[j]`，且`next[1]=-1`。则`abcac`的`next`数组为`[-1,0,0,0,1]`。如果发生失配，则令`j=j-Move=j-((j-1)-next[j])=next[j]+1`，因此得到子串指针变换公式`j=next[j]+1`。

也有令`next[j+1]=PM[j]+1`和`next[1]=0`的做法，即`abcac`的`next`数组为`[0,1,1,1,2]`。此时子串指针变换公式为`j=next[j]`。

`next`数组的含义：当在模式串的第`j`个位置与文本串失配时，应当跳到模式串的哪个位置重新匹配。

### next数组的确切定义

- 如果`j=1`，则`next[j]=0`。
- 如果`j>1`，则：
	- 如果存在`P[1...k-1]==P[j-k+1...j-1]`，则`next[j]`取所有`k`的最大值。
	- 如果不存在，则`next[j]=1`。

### nextval数组

如果`P[j]==P[next[j]]`，则移动模式串之后的下一次匹配仍旧是无意义的：因为`T[i]!=P[j]`，所以必有`T[i]!=P[next[j]]`。

这时考虑计算`nextval`数组，`j=nextval[i]`是第一个满足`P[j]!=P[i]`的位置，其中`j=next[next[...[i]]]`。

例如，`aaaab`的`next`数组为`[0,1,2,3,4]`，则`nextval`数组为`[0,0,0,0,4]`。

用`nextval`数组替代`next`数组进行失配转移可以提升KMP算法的效率。

### KMP算法实现

```cpp
/**
 * Knuth-Morris-Pratt (KMP) Algorithm
 *
 * KMP is famous for its ability to check all presences of the pattern string in
 * the text in O(nlogn) time complexity.
 *
 * The function kmp_build(const string& str) returns the fail
 * function(fail[0]~fail[n]) of str. Fail function indicates the next position
 * to match if the current match fails. Specifically, fail[0]=-1,
 * fail[i]<=fail[i-1]+1.
 *
 * str = "ababa" --> fail = [-1 0 0 1 2 3]
 *
 * ATTENTION: fail array has a length of str.length()+1 instead of str.length().
 */
vector<int> kmp_build(const string& str) {
  int len = str.length();
  vector<int> fail(len + 1, 0);
  fail[0] = -1;
  for (int i = 1, j; i <= len; ++i) {
    for (j = fail[i - 1]; ~j && str[i - 1] != str[j]; j = fail[j])
      ;
    fail[i] = j + 1;
  }
  return fail;
}

/**
 * If you simply want to run KMP algorithm, just invoke this function.
 *
 * ATTENTION: match array has a length of text.length()+1 instead of
 * text.length().
 */
vector<int> kmp(const string& text, const string& pattern) {
  vector<int> fail = kmp_build(pattern);
  int len = text.length();
  vector<int> match(len + 1, 0);
  for (int i = 1, j; i <= len; ++i) {
    for (j = match[i - 1]; ~j && text[i - 1] != pattern[j]; j = fail[j])
      ;
    match[i] = j + 1;
  }
  return match;
}
```