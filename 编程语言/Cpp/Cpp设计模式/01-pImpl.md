
将类的实现细节隐藏到`*.cpp`中，而非暴露到头文件中，这样可以免去在包含头文件时引入过多其他内容。

```cpp
// foo.h
class MyClass {
  // type aliases, constructors, destructor, operators, member functions,
  // etc.
  private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};

// foo.cpp
#include "foo.h"

struct MyClass::Impl {
	// members that aren't elegant enough to show up
};

MyClass::MyClass(): impl_(std::make_unique<Impl>(...)) {
	// some other stuff
}
```