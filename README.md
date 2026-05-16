# ClailDesk

开源远程桌面软件，支持 Windows、Linux、Android。

## 功能特性

- 远程控制：跨平台远程桌面访问
- 文件传输：高速安全的文件传输
- 剪贴板同步：跨设备剪贴板共享
- 简洁界面：现代化扁平设计

## 系统要求

- Windows 10/11
- Linux (需要图形环境)
- Android 9.0+

## 构建

### Windows

```bash
# 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装依赖
# - Visual Studio Build Tools
# - CMake
# - Rust (stable)

# 编译
cargo build --release
```

## 许可证

MIT License
