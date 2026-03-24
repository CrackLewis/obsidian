
Google整的一个单元测试框架。

## 安装和部署

Ubuntu/Debian：

```sh
$ sudo apt install libgtest-dev libgmock-dev
```

源码：

```sh
$ git clone https://github.com/google/googletest.git
$ cd googletest
$ mkdir -p build
$ cd build
$ cmake ..
$ make && sudo make install
```

## CMake中使用

CMake加载或自动安装gtest：

```cmake
# First try to find an installed GTest package. If not available, use FetchContent
find_package(GTest QUIET)
if(NOT GTest_FOUND)
  include(FetchContent)
  # avoid old timestamp behavior
  set(FETCHCONTENT_QUIET OFF)
  set(FETCHCONTENT_UPDATES_DISCONNECTED OFF)
  set(DOWNLOAD_EXTRACT_TIMESTAMP TRUE)

  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG main
  )
  FetchContent_MakeAvailable(googletest)
endif()
```

CMake为某个特定目标（一般是单元测试目标）链接+包含gtest库：

```cmake
if(TARGET gtest_main)
  target_link_libraries(${CURR_TARGET} PRIVATE gtest_main)
elseif(TARGET GTest::gtest_main)
  target_link_libraries(${CURR_TARGET} PRIVATE GTest::gtest_main)
else()
  message(FATAL_ERROR "GoogleTest not found and could not be fetched; install GTest or enable network access for FetchContent")
endif()
```

## demo-1：基本测试

```cpp
#include <gtest/gtest.h>

TEST(MyTestSuite, Test1) {
	ASSERT_EQ(2 + 3, 5);
}

int main(int argc, char* argv[]) {
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}
```

## 测试夹具

用于+在数个需要使用相同或相关数据/子程序的不同测试间，共享这些成员

定义夹具需要公开继承`::testing::Test`类，并重写`SetUp/TearDown`方法。

```cpp
class DemoFixture : public ::testing::Test {
protected:
	std::vector<int> data_;
	
	void SetUp() override {
		std::mt19937 rng(42);
		const int N = 1 << 17;
		for (int i = 0; i < n; ++i) data_.emplace_back(rng());
	}
	
	void TearDown() override = default;
};
```