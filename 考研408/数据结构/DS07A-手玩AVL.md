
## 结点定义

```cpp
class Node {
public:
	int key;
	Node* left;
	Node* right;
	int height;
	
	Node(int k) : key(k), left(nullptr), right(nullptr), height(1) {}
};
```

## 辅助函数

```cpp
int __height(Node* node) {
	if (node == nullptr) return 0;
	return node->height;
}

// 平衡因子是左子树高度减右子树高度。它不能超过正负1。
int __balance_factor(Node* node) {
	if (node == nullptr) return 0;
	return __height(node->left) - __height(node->right);
}
```

## 左旋

对结点`x`左旋的含义是：在不改变中序遍历序列的前提下，将`x`为根节点的子树的根节点调整为`x`的右子节点。

```cpp
Node* __rotate_left(Node* x) {
	Node* y = x->right;
	Node* T2 = y->left;
	
	// 变换形态：(Xl)X((T2)Y(Yr)) => ((Xl)X(T2))Y(Yr)
	y->left = x;
	x->right = T2;
	
	// 重新计算高度
	x->height = 1 + std::max(__height(x->left), __height(x->right));
	y->height = 1 + std::max(__height(y->left), __height(y->right));
	
	return y;
}
```

## 右旋

对结点`x`右旋的含义是：在不改变中序遍历序列的前提下，将`x`为根结点的子树的根结点调整为`x`的左子结点。

```cpp
Node* __rotate_right(Node* y) {
	Node* x = y->left;
	Node* T2 = x->right;
	
	// 变换形态：((Xl)X(T2))Y(Yr) => (Xl)X((T2)Y(Yr))
	x->right = y;
	y->left = T2;
	
	// 重新计算高度
	y->height = 1 + std::max(__height(y->left), __height(y->right));
	x->height = 1 + std::max(__height(x->left), __height(x->right));
	
	return x;
}
```

## 平衡性维护

目的：维护整棵二叉树的平衡性。

诱因：
- 插入元素导致某棵子树失衡。
- 删除元素导致部分树或全树失衡。

平衡性维护的四种情形：
- LL情形：在`x`左儿子的左子树中插入节点，导致`x`子树失衡。解决思路是对`x`进行一次右旋。
- RR情形：在`x`右儿子的右子树中插入节点，导致`x`子树失衡。解决思路是对`x`进行一次左旋。
- LR情形：在`x`左儿子的右子树中插入节点，导致`x`子树失衡。解决思路是，先对`x`的左子树进行一次左旋，转化为LL情形，再对`x`进行一次右旋。
- RL情形：在`x`右儿子的左子树中插入节点，导致`x`子树失衡。解决思路是，先对`x`的右子树进行一次右旋，转化为RR情形，再对`x`进行一次左旋。

```cpp
// 通过特定的旋转策略恢复平衡状态。
  Node* __balance(Node* root) {
    int balance = __balance_factor(root);

    if (balance > 1) {
      if (__balance_factor(root->left) >= 0) {
        /**
         * @brief
         *
         * 情形一：LL情形，root的左儿子的左子树插入节点，导致失衡。
         *
         * 解决方式：root右旋一次即可恢复平衡。
         *
         * 初始：((Bl)B(Br))A(Ar)，Bl,Br,Ar高度均为H
         * 插入后：Bl高度变为H+1，A处失衡。
         * A右旋后：(Bl)B((Br)A(Ar))，Bl高度为H+1，Br,Ar高度为H，子树重新平衡。
         *
         * @return return
         */
        return __rotate_right(root);
      } else {
        /**
         * @brief
         *
         * 情形二：LR情形，root左儿子的右子树插入节点，导致失衡。
         *
         * 解决方式：需要先对root的左儿子进行一次左旋，再对root进行一次右旋。
         *
         * 初始：((Bl)B((Cl)C(Cr)))A(Ar)，Bl,Ar高度为H，Cl,Cr高度为H-1。
         * 插入后：Cl或Cr高度升为H，结点A失衡。
         * 第一次旋转：B左旋，(((Bl)B(Cl))C(Cr))A(Ar)，实际转化为LL情形。
         * 第二次旋转：A右旋，((Bl)B(Cl))C((Cr)A(Ar))，和解决LL情形的方法一致。
         *
         */
        root->left = __rotate_left(root->left);
        return __rotate_right(root);
      }
    } else if (balance < -1) {
      if (__balance_factor(root->right) <= 0) {
        /**
         * @brief
         *
         * 情形三：RR情形，root右儿子的右子树插入节点，导致失衡。
         *
         * 解决方式：root左旋一次解决。
         *
         * 总体原理和LL情形类似。
         *
         * @return return
         */
        return __rotate_left(root);
      } else {
        /**
         * @brief
         *
         * 情形四：RL情形，root右儿子的左子树插入节点，导致失衡。
         *
         * 解决方式：root右儿子右旋一次，转化为RR情形，再对root左旋一次解决。
         *
         * 总体原理和LR情形类似。
         */
        root->right = __rotate_right(root->right);
        return __rotate_left(root);
      }
    }

    // 无失衡情形，无需平衡。
    return root;
  }
```

## 插入元素

机制：
- 如果是叶结点处插入，直接就地构造即可。
- 如果是在子树中插入：
	- 如果取值和根结点雷同，则忽略本次操作。
	- 如果取值落在左子树或右子树中，则先递归执行对应子树的插入语句，再更新高度数据，最后根据平衡因子的取值情况进行平衡性维护。

```cpp
Node* __insert(Node* root, int key) {
	if (root == nullptr) return new Node(key);
	
	if (key < root->key)
	  root->left = __insert(root->left, key);
	else if (key > root->key)
	  root->right = __insert(root->right, key);
	else
	  return root;  // Duplicate keys are not allowed
	
	root->height = 1 + std::max(__height(root->left), __height(root->right));
	
	return __balance(root);
}
```

## 删除元素

求子树的最左结点：
```cpp
Node* __leftmost(Node* node) {
	Node* current = node;
	while (current->left != nullptr) current = current->left;
	return current;
}
```

机制：
- 递归向下找到待删除节点，如果没找到则忽略操作。
- 对于待删除结点：
	- 如果两个子结点均为空，说明为叶结点，直接删除。
	- 如果有一个非空子结点，则用其顶替自己的位置。
	- 如果两个子结点均为非空，则让右子树的最左结点顶替自己的位置，最左结点原来所在的结点删除。
- 任何情形下都需要维护平衡性质。


```cpp
Node* __remove(Node* root, int key) {
    if (root == nullptr) return nullptr;

    if (key < root->key)
      root->left = __remove(root->left, key);
    else if (key > root->key)
      root->right = __remove(root->right, key);
    else {
      // 键值恰好匹配，删除root。

      // 两个子结点不同时存在时，可以用一支直接顶上去。
      if (root->left == nullptr || root->right == nullptr) {
        Node* temp = root->left ? root->left : root->right;
        if (temp == nullptr) {
          temp = root;
          root = nullptr;
        } else
          *root = *temp;

        delete temp;
      } else {
        // 如果两个子结点同时存在，需要找到该结点的直接后驱（右子树的最左结点），用其换下当前节点。
        Node* temp = __leftmost(root->right);
        root->key = temp->key;
        // 然后需要删除这个后继结点。
        root->right = __remove(root->right, temp->key);
      }
    }

    if (root == nullptr) return root;

    root->height = 1 + std::max(__height(root->left), __height(root->right));
    // 由删除引发的失衡情形同样需要处理。
    return __balance(root);
  }
```


