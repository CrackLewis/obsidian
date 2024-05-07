
## amd64下编译ffmpeg 4.4.4

首先装`nasm`，这个是x264的依赖：

```bash
$ wget https://www.nasm.us/pub/nasm/releasebuilds/2.16.03/nasm-2.16.03.tar.gz
$ tar -zxvf nasm-2.16.03.tar.gz
$ cd nasm-2.16.03
$ ./configure
$ make
$ sudo make install
```

然后再装`x264`（听说挺重要的）：

```bash
$ sudo apt-get update
$ sudo apt-get install build-essential git-core checkinstall texi2html libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libsdl1.2-dev libtheora-dev libvorbis-dev libx11-dev libxfixes-dev zlib1g-dev yasm
$ git clone https://code.videolan.org/videolan/x264
$ cd x264
$ ./configure --enable-shared
$ make
$ sudo make install
```

装`x265`：

```bash
$ wget http://ftp.videolan.org/pub/videolan/x265/x265_3.2.tar.gz
$ sudo tar -zxvf x265_3.2.tar.gz
$ ./configure
$ make
$ sudo make install
```

最后装`ffmpeg`：

```bash
$ wget 
$ tar -zxvf ffmpeg-4.4.4.tar.gz
$ cd ffmpeg-4.4.4.tar.gz
$ ./configure --disable-stripping --enable-gpl --enable-libx264 --enable-libx265 --enable-shared --enable-version3 --enable-protocols --enable-protocol=rtsp
$ ./configure --disable-stripping --enable-gpl --enable-shared --enable-version3 --enable-protocols
$ make -j8
```

关于配置选项，网上有很多版本，下面是另一种据说成功率较高的版本：

```bash
$ ./configure --disable-static --enable-shared --enable-gpl --enable-version3 --disable-w32threads --enable-avisynth --enable-bzlib --enable-fontconfig --enable-frei0r --enable-gnutls --enable-iconv --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libfreetype --enable-libgme --enable-libgsm --enable-libilbc --enable-libmodplug --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libopus --enable-librtmp --enable-libschroedinger --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvo-aacenc --enable-libvo-amrwbenc --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxavs --enable-libxvid --enable-lzma --enable-decklink --enable-zlib
```

arm交叉编译：

```bash
$ ./configure --cross-prefix=/home/cracklewis/5.4.0/bin/arm-linux- --enable-cross-compile --arch=arm --target-os=linux --cc=/home/cracklewis/5.4.0/bin/arm-linux-gcc --disable-x86asm --disable-stripping --enable-gpl --enable-shared --enable-version3 --enable-protocols
```
## ffmpeg程序基本流程

- av_register_all
- avformat_open_input
- avformat_find_stream_info
- avcodec_find_decoder
- avcodec_open2
- 读取frame循环：
	- av_read_frame
	- 读取到一帧：avcodec_decode_video2 -> 后续环节（推流、本地存储、转播、etc）
	- 读取不到：读取结束
- 关闭程序

## 重要ffmpeg函数库

- avcodec：编码/解码库
- avdevice：各种设备I/O
- avformat：封装格式操作
- swscale：像素格式转换
- swresample：音频采样
- avfilter：滤镜和特效
- avutil：工具库
- postproc：后处理

## 重要ffmpeg结构

![[Pasted image 20240501113759.png]]

- `AVFormatContext`：封装格式上下文
	- `AVInputFormat`：封装格式
	- `AVStream`：各种文件中的各种流（视频流、音频流、etc）
		- `AVCodecContext`：编解码器上下文
			- `AVCodec`：各种文件中的编解码结构体
- `AVPacket`：一帧压缩数据编解码数据
- `AVFrame`：一帧解码后像素采样数据

### AVFormatContext

封装格式I/O上下文。

重要成员如下：
- `AVInputFormat* iformat`：输入文件的封装格式。
- `AVOutputFormat* oformat`：输出文件的封装格式。
- `int nb_streams`：输入文件的流数量。
- `AVStream** streams`：输入文件的流数组。
- `int64_t duration`：输入文件时长。
- `int bit_rate`：输入文件码率。