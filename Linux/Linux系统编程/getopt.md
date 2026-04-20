
**太长不读**：
- [[#示例：纯短参数解析]]
- 

Linux自带的命令行参数解析，功能较弱，可能需要人工增强（如类型检查、范围限制、参数互斥等）

```cpp
#include <getopt.h>
```

## 核心成员

`bits/getopt_core.h`

核心库的基本原理是根据用户指定的`optstring`（参数字符串），在`argv`中检索匹配的选项并通过`optarg`等成员返回给用户。

核心库可能不是线程安全的，有待考证。

成员：
- `char* optarg`：如果某个选项有附带参数，返回该选项的参数字符串
- `int optind`：argv的当前索引值
- `int opterr`：错误代码，默认为0
- `int optopt`：如果遇到无效选项字符（`getopt`返回`'?'`），则将该字符填入`optopt`
- `int getopt(argc, argv, shortopts)`：解析函数
	- `argc,argv`：一般由`main`直接传入
	- `shortopts`：即前文提到的`optstring`，详细见下

## optstring

`getopt`核心库不支持长选项解析，只支持短选项。`optstring`是标识这种短选项的手段，*区分大小写*。

`getopt`扩展库支持长选项解析。但如果长选项指定了同义短选项，则仍然需要在`optstring`中标出，而不得省略。

`optstring`由一系列的短选项组成，每个短选项`*`有三种模式：
- `*`：只接受无参匹配
- `*:`：只接受有参匹配，参数作为选项的下一项
- `*::`：接受无参和有参匹配，如果有参，则参数必须紧随选项后

| 用法       | `*` | `*:` | `*::` |
| -------- | --- | ---- | ----- |
| `-*`     | Y   |      | Y     |
| `-* arg` |     | Y    |       |
| `-*arg`  |     |      | Y     |
 
## 示例：纯短参数解析

假设需要解析如下参数：
- `-h <host>`：连接的主机IP，参数必带
- `-p <port>`：连接的主机端口，参数必带
- `-a[<password>]`：密码，参数可选
- `-s`：是否为无状态

```cpp
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char* fmt_usage = "\
Usage: %s -h <host> -p <port> [-a<password>] [-s]\n\
\n\
\t-h <host>: host IP\n\
\t-p <port>: host port\n\
\t-a<password>: password\n\
\t-s: status-free connection\n\
";
const char* optstr = "h:p:a::s";

int main(int argc, char** argv) {
  int o;
  char hoststr[20], psw[20] = "";
  int port, is_status_free = 0, host_sect[4] = {0, 0, 0, 0};
  void* errp = NULL;
  while ((o = getopt(argc, argv, optstr)) != -1) {
  // getopt会返回以下几种结果：
  // - 63：即'?'的ASCII，表示当前读到了一个未知选项，其具体值存储在optopt
  // - 非63的正值：选项的ASCII码，如有附带参数，则存储在optarg中
  // - -1：没有可以继续解析的参数
    switch (o) {
      case 'h': {
        if (strlen(optarg) > 19) {
          errp = hoststr;
          break;
        }
        strcpy(hoststr, optarg);
        int pos = 0, off = 0, prenum = 0;
        while (pos < 4) {
          while (hoststr[off] >= '0' && hoststr[off] <= '9')
            (host_sect[pos] *= 10) += (hoststr[off++] - '0'), prenum++;
          if (pos != 3 && hoststr[off++] != '.' || !prenum) {
            errp = hoststr;
            break;
          }
          ++pos, prenum = 0;
        }
        break;
      }
      case 'p': {
        port = atoi(optarg);
        if (port < 1024 || port > 65535) errp = &port;
        break;
      }
      case 'a': {
        (optarg && strlen(optarg) > 19) ? ({
          errp = psw;
          break;
        })
                                        : ({
                                            if (optarg) strcpy(psw, optarg);
                                            ;
                                          });
        break;
      }
      case 's': {
        is_status_free++;
        break;
      }
      case '?': {
        errp = &o;
        break;
      }
    }
    if (errp) break;
  }
  if (errp == NULL) {
    printf("Host: %d.%d.%d.%d:%d\n", host_sect[0], host_sect[1], host_sect[2],
           host_sect[3], port);
    printf("Password: %s\n", psw);
    printf("Status-Free: %s\n", is_status_free ? "true" : "false");
  } else {
    printf("Error: argument error: ");
    if (errp == hoststr)
      printf("bad host format\n");
    else if (errp == &port)
      printf("bad port number\n");
    else if (errp == psw)
      printf("too long password\n");
    else if (errp == &o) {
      printf("unknown argument %c\n", optopt);
    }
    printf(fmt_usage, argv[0]);
  }
  return 0;
}
```

## 示例：长短参数混合解析

`getopt`扩展库中的`getopt_long`函数添加了对长参数的支持。该函数需要一个`option`数组表示各个长参数。

`getopt_long`参数：
- `argc,argv`：命令行参数列表
- `shortopts`：短参数列表，传入`optstring`
- `longopts`：长参数列表，传入`option`数组
- `longind`：参数遍历索引指针，应由用户传入，初始设为0

返回值：
- 正数：识别了一个短参数、或映射到短参数的长参数
- 0：识别了一个没有映射到短参数的长参数
- -1：无参数可识别

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>

int main(int argc, char *argv[]) {
    int opt;
    int option_index = 0;

    struct option long_options[] = {
        {"file", required_argument, NULL, 'f'},
        {"verbose", no_argument, NULL, 'v'},
        {"help", no_argument, NULL, 'h'},
        {0, 0, 0, 0} // 结束标志
    };

    while ((opt = getopt_long(argc, argv, "vf:h", long_options, &option_index)) != -1) {
        switch (opt) {
            case 'f':
                printf("Option -f with value '%s'\n", optarg);
                break;
            case 'v':
                printf("Option -v (verbose) selected\n");
                break;
            case 'h':
                printf("Option -h (help) selected\n");
                break;
            case '?':
                // 处理未知选项
                fprintf(stderr, "Unknown option: %c\n", optopt);
                break;
            default:
                // 如果未处理的选项字符是一个长选项，这里会执行
                fprintf(stderr, "Usage: %s [-f filename] [-v] [-h]\n", argv[0]);
                exit(EXIT_FAILURE);
        }
    }

    return 0;
}
```

