
## 免密登录

首先被登录的设备要确保在`/etc/ssh/sshd_config`中：
- 将PubkeyAuthentication设为yes。
- 将RSAAuthentication设为yes。

添加登录方的公钥到被登录方`~/.ssh/authorized_keys`中：
- 直接输入：`cat id_rsa.pub >> ~/.ssh/authorized_keys`
- 从宿主机传送：`ssh-copy-id -i ~/.ssh/id_rsa.pub username@host`

如果仍不能免密登录：
- 重启一下`sshd`服务。
- 重启计算机（危险）。
- 考虑检查公钥是否有误，或者考虑重新生成（危险）。

## 生成ed25519密钥

```bash
$ ssh-keygen -t ed25519 -C "ghxx040406@163.com"
```

命令会要求输入*私钥内容*和*密钥存储目录*，输入对应内容，随后会在对应目录下存储两个文件：
- `id_ed25519`：私钥文件
- `id_ed25519.pub`：公钥文件

第三方应用一般要求持有SSH公钥，这时直接将公钥内容拷贝过去即可。