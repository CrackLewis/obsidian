
字典树。

衍生品有AC自动机、01-Trie、可持久化Trie等。

## C++11实现

```cpp
template <class SymTy>
class Trie {
 private:
  struct TrieNode {
    std::unordered_map<SymTy, TrieNode*> next_;
    enum class NodeType { DEFAULT, WITH_VALUE, MAX } type_ = NodeType::DEFAULT;

    virtual ~TrieNode() = default;
  };
  template <class ValTy>
  struct TrieNodeWithVal : public TrieNode {
    ValTy* val_;
    explicit TrieNodeWithVal(const ValTy& val) {
      TrieNode::type_ = TrieNode::NodeType::WITH_VALUE;
      val_ = new ValTy(val);
    }
    explicit TrieNodeWithVal(ValTy&& val) {
      TrieNode::type_type_ = TrieNode::NodeType::WITH_VALUE;
      val_ = new ValTy(std::move(val));
    }
    virtual ~TrieNodeWithVal() {
      if (val_) delete val_;
    }
  };

 public:
  Trie() {
    root_ = new TrieNode;
    nodes_.insert(root_);
  }
  virtual ~Trie() {
    for (auto node : nodes_) delete node;
  }

  template <class ValTy>
  void put(const std::vector<SymTy>& key, const ValTy& val) {
    if (key.size() <= 0u) return;

    TrieNode *cur = root_, *new_node = new TrieNodeWithVal<ValTy>(val), *tmp;
    nodes_.insert(new_node);

    for (int idx = 0; idx < key.size() - 1; idx++) {
      if (cur->next_.find(key[idx]) == cur->next_.end()) {
        cur->next_[key[idx]] = (tmp = new TrieNode);
        nodes_.insert(tmp);
      }
      cur = cur->next_[key[idx]];
    }
    if ((tmp = cur->next_[key.back()]) != nullptr) {
      new_node->next_ = tmp->next_;
      nodes_.erase(tmp);
      delete tmp;
    }
    cur->next_[key.back()] = new_node;
  }

  template <class ValTy>
  ValTy* get(const std::vector<SymTy>& key) {
    TrieNode* cur = root_;
    for (const auto& sym : key) {
      if (cur->next_.find(sym) == cur->next_.end()) {
        return nullptr;
      }
      cur = cur->next_[sym];
    }
    if (cur->type_ == TrieNode::NodeType::WITH_VALUE) {
      auto vnode = dynamic_cast<TrieNodeWithVal<ValTy>*>(cur);
      return vnode ? vnode->val_ : nullptr;
    }
    return nullptr;
  }

 private:
  std::unordered_set<TrieNode*> nodes_;
  TrieNode* root_ = nullptr;
};
```

WIP：
- 可持久化Trie
- 01-Trie
- 数据库中使用的COW Trie