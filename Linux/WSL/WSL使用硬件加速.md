
背景：宿主机有显卡，WSL输入`nvidia-smi`正常，但通过SDL2编译的图形程序极其卡顿，通过检查`glxinfo`输出中的`OpenGL renderer`发现使用的是软件渲染（llvmlite），没有用到GPU加速。

解决方案：在`~/.bashrc`中添加两行：

```sh
export GALLIUM_DRIVER=d3d12
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
```

