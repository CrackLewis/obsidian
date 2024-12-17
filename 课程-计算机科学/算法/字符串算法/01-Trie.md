
字典树。

衍生品有AC自动机、01-Trie、可持久化Trie等。

## C++11实现

```cpp
template <class SymTy>
class Trie {
private:
	struct TrieNode {
		std::unordered_map<SymTy, TrieNode*> next_;	
		void* val_;
	};
public:
	Trie() {
		root_ = new TrieNode;
		nodes_.push_back(root_);
	}
	virtual ~Trie() {
		for (auto node: nodes_) delete node;
	}
	
private:
	std::vector<TrieNode*> nodes_;
	TrieNode* root_ = nullptr;
};
```

WIP：
- 可持久化Trie
- 01-Trie
- 数据库中使用的COW Trie