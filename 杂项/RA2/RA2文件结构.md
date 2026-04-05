
## 总体结构

原版：
- `ra2.exe`：启动器程序
- `game.exe`：游戏程序
- `ra2.mix`：原版游戏数据文件
	- `cache.mix`
	- `conquer.mix`
	- `generic.mix`
	- `isogen.mix`
	- `isosnow.mix`
	- `isotemp.mix`
	- `isourb.mix`
	- `load.mix`
	- `local.mix`：本地AI规则、游戏规则、艺术资源定义和加载规则，艺术素材等
		- `*.aud`：音频文件（intro/maps/text1~3）
		- `*.hva`：载具部件调整控制。不过大部分的hva内容似乎都一致且很小（88B）
		- `*.pal`：色盘文件
		- `*.pcx`、`*.shp`：游戏贴图
		- 
	- `neutral.mix`
	- `sidec01.mix`
	- `sidec02.mix`
	- `sidenc01.mix`
	- `sidenc02.mix`
	- `sno.mix`
	- `snow.mix`
	- `tem.mix`
	- `temperat.mix`
	- `urb.mix`
	- `urban.mix`
	- `key.ini`
- `language.mix`：原版语言包扩展
- `maps01.mix`：官方地图包（1）
- `maps02.mix`：官方地图包（2）
- `movies01.mix`
- `movies02.mix`
- `multi.mix`
- `theme.mix`