
## fcitx-谷歌拼音

配置输入法系统：
```bash
$ im-config
```

弹出界面中点OK、Yes，接着选fcitx，点OK、OK。

随后需要在系统设置里安装中文支持，不同版本系统的方法不一样。

随后建议重启。

重启后，安装fcitx和谷歌拼音：
```bash
$ sudo apt install fcitx
$ sudo apt install fcitx-googlepinyin
```

配置输入法：
```bash
$ fcitx-config-gtk3
```

![[Pasted image 20231230100609.png]]

确保输入法中有拼音和英语键盘即可。

找到Fcitx Configuration，配置`Alt-Shift`为激活/解激活输入法的快捷键，`Ctrl-Shift`为切换输入法的快捷键。

![[Pasted image 20231230101753.png]]

按两次切换快捷键之间要等1s左右，属于Linux的传统艺能。

