
```bash
# pip
$ pip install redis
# conda
$ conda install redis
```

## 示例：stub

一个演示项目，可以根据这个项目扩充功能。

```python
import redis

rpool = redis.ConnectionPool(max_connections=10, host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=rpool)

def main():
  while True:
    print('> ', end='')
    opts = input().split(' ')
    if len(opts) == 0:
      continue
    if opts[0] == 'quit':
      break 
    
    # remove all empty strings until ValueError is raised
    try:
      while True:
        opts.remove('')
    except ValueError:
      pass 

    if len(opts) == 3 and opts[0] == 'set':
      r.set(opts[1], opts[2])
    elif len(opts) == 2 and opts[0] == 'get':
      print(r.get(opts[1]))
    else:
      print('E: Bad command or wrong arguments.')

if __name__ == '__main__':
  main()
```

