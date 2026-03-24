
| 宏签名 (Macro Signature)                                                       | 功能描述 (Functionality)                                            |
| :-------------------------------------------------------------------------- | :-------------------------------------------------------------- |
| **布尔条件 (Boolean Conditions)**                                               |                                                                 |
| `ASSERT_TRUE(condition)` / `EXPECT_TRUE(condition)`                         | 验证 `condition` 是否为真 (true)。                                     |
| `ASSERT_FALSE(condition)` / `EXPECT_FALSE(condition)`                       | 验证 `condition` 是否为假 (false)。                                    |
| **二元比较 (Binary Comparison)**                                                |                                                                 |
| `ASSERT_EQ(val1, val2)` / `EXPECT_EQ(val1, val2)`                           | 验证 `val1 == val2`。适用于整数、指针、字符串等可比较类型。                           |
| `ASSERT_NE(val1, val2)` / `EXPECT_NE(val1, val2)`                           | 验证 `val1 != val2`。                                              |
| `ASSERT_LT(val1, val2)` / `EXPECT_LT(val1, val2)`                           | 验证 `val1 < val2` (Less Than)。                                   |
| `ASSERT_LE(val1, val2)` / `EXPECT_LE(val1, val2)`                           | 验证 `val1 <= val2` (Less or Equal)。                              |
| `ASSERT_GT(val1, val2)` / `EXPECT_GT(val1, val2)`                           | 验证 `val1 > val2` (Greater Than)。                                |
| `ASSERT_GE(val1, val2)` / `EXPECT_GE(val1, val2)`                           | 验证 `val1 >= val2` (Greater or Equal)。                           |
| **字符串比较 (String Comparison)**                                               |                                                                 |
| `ASSERT_STREQ(str1, str2)` / `EXPECT_STREQ(str1, str2)`                     | 验证两个 C 风格字符串 (`const char*`) 内容相等。                              |
| `ASSERT_STRNE(str1, str2)` / `EXPECT_STRNE(str1, str2)`                     | 验证两个 C 风格字符串内容不相等。                                              |
| `ASSERT_STRCASEEQ(str1, str2)` / `EXPECT_STRCASEEQ(str1, str2)`             | 验证两个 C 风格字符串内容相等（忽略大小写）。                                        |
| `ASSERT_STRCASENE(str1, str2)` / `EXPECT_STRCASENE(str1, str2)`             | 验证两个 C 风格字符串内容不相等（忽略大小写）。                                       |
| **浮点数比较 (Floating-point Comparison)**                                       |                                                                 |
| `ASSERT_FLOAT_EQ(val1, val2)` / `EXPECT_FLOAT_EQ(val1, val2)`               | 验证两个 `float` 值几乎相等（误差在 4 ULPs 以内）。                              |
| `ASSERT_DOUBLE_EQ(val1, val2)` / `EXPECT_DOUBLE_EQ(val1, val2)`             | 验证两个 `double` 值几乎相等（误差在 4 ULPs 以内）。                             |
| `ASSERT_NEAR(val1, val2, abs_error)` / `EXPECT_NEAR(val1, val2, abs_error)` | 验证 `val1` 和 `val2` 的差值绝对值不超过 `abs_error`。                       |
| **异常断言 (Exception Assertions)** <br>*(仅在支持异常的平台/配置下有效)*                     |                                                                 |
| `ASSERT_THROW(statement, exception_type)` / `EXPECT_THROW(...)`             | 验证 `statement` 抛出了指定类型的异常。                                      |
| `ASSERT_ANY_THROW(statement)` / `EXPECT_ANY_THROW(...)`                     | 验证 `statement` 抛出了任何类型的异常。                                      |
| `ASSERT_NO_THROW(statement)` / `EXPECT_NO_THROW(...)`                       | 验证 `statement` 没有抛出任何异常。                                        |
| **死亡测试 (Death Tests)** <br>*(验证程序是否按预期崩溃)*                                  |                                                                 |
| `ASSERT_DEATH(statement, regex)` / `EXPECT_DEATH(...)`                      | 验证 `statement` 导致程序崩溃，且 stderr 输出匹配正则表达式 `regex`。               |
| `ASSERT_EXIT(statement, predicate, regex)` / `EXPECT_EXIT(...)`             | 验证 `statement` 导致程序退出，退出状态满足 `predicate`，且 stderr 输出匹配 `regex`。 |
| *(注：还有 `ASSERT_DEBUG_DEATH`, `ASSERT_QUICK_EXIT` 等变体)*                      |                                                                 |
| **谓词断言 (Predicate Assertions)** <br>*(用于自定义检查逻辑)*                           |                                                                 |
| `ASSERT_PRED1(pred, v1)` / `EXPECT_PRED1(...)`                              | 验证一元谓词 `pred(v1)` 返回 true。                                      |
| `ASSERT_PRED2(pred, v1, v2)` / `EXPECT_PRED2(...)`                          | 验证二元谓词 `pred(v1, v2)` 返回 true。                                  |
| *(支持最多 5 元谓词 `ASSERT_PRED5`)*                                               |                                                                 |
| `ASSERT_PRED_FORMAT1(pred_formatter, v1)` / `EXPECT_PRED_FORMAT1(...)`      | 使用自定义格式化函数的一元谓词断言，可提供更友好的错误消息。                                  |
| *(支持最多 5 元 `ASSERT_PRED_FORMAT5`)*                                          |                                                                 |
| **HRESULT 断言 (Windows 特有)**                                                 |                                                                 |
| `ASSERT_HRESULT_SUCCEEDED(expr)` / `EXPECT_HRESULT_SUCCEEDED(expr)`         | 验证 Windows HRESULT 表达式成功 (SUCCEEDED)。                           |
| `ASSERT_HRESULT_FAILED(expr)` / `EXPECT_HRESULT_FAILED(expr)`               | 验证 Windows HRESULT 表达式失败 (FAILED)。                              |

