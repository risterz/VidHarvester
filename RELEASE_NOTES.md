# VidHarvester v1.0.0 Release Notes

## 🎉 Initial Release

Welcome to the first official release of **VidHarvester** - a professional video downloading application!

### ✨ **Key Features**

#### 🎥 **Core Functionality**
- **Multi-format Support**: Download videos in MP4, WebM, MKV formats
- **Quality Selection**: Choose from auto-best, 720p, 1080p, and highest available
- **Subtitle Embedding**: Automatic subtitle download and embedding
- **Thumbnail Support**: Extract and embed video thumbnails

#### 🔌 **Advanced Capture Methods**
- **Browser Extensions**: Chrome, Firefox, and Edge extensions for automatic URL capture  
- **Smart URL Detection**: Automatically converts stream URLs to page URLs for better compatibility
- **Proxy Integration**: mitmproxy support for transparent video capture
- **Direct Input**: Manual URL input with drag & drop support

#### 🖥️ **Modern Interface**
- **Clean PyQt6 GUI**: Responsive dark theme interface
- **Real-time Progress**: Live download progress with speed and ETA
- **Queue Management**: Download multiple videos concurrently
- **History Tracking**: Complete download history with statistics
- **System Tray**: Minimize to tray with notifications

### 🔧 **Technical Improvements**
- **Smart URL Processing**: Fixed issue where direct stream URLs caused download failures
- **Enhanced Browser Extensions**: Improved filtering to capture only main videos (not thumbnails)
- **Debounced Capture**: Prevents spam captures with intelligent cooldown
- **Cross-platform Support**: Works on Windows, Linux, and macOS

### 📦 **What's Included**

#### Windows Releases:
- **VidHarvester-Setup-1.0.0.exe** - Full Windows installer with dependencies
- **VidHarvester-Portable-1.0.0.zip** - Portable version, no installation required
- **VidHarvester-OneFile-1.0.0.exe** - Single executable file

#### Browser Extensions:
- **VidHarvester-Extensions-1.0.0.zip** - Chrome, Firefox, and Edge extensions

#### Source Code:
- **Source code (zip)** - Complete source code archive
- **Source code (tar.gz)** - Complete source code archive

### 🚀 **Getting Started**

1. **Download the installer** for your platform
2. **Install VidHarvester** following the setup wizard
3. **Load browser extension** from the extensions folder
4. **Start downloading** videos from your favorite sites!

### 📋 **System Requirements**

- **Windows 10/11** (x64)
- **Python 3.10+** (for source installation)
- **FFmpeg** (automatically included in Windows installer)
- **2GB RAM minimum**, 4GB recommended
- **500MB free disk space**

### 🐛 **Known Issues**
- Some video sites may require cookies for authentication
- Very long URLs may cause filename truncation on Windows
- Proxy mode requires manual certificate installation

### 🔄 **Migration from Beta**
This is the first stable release. No migration needed.

### 🤝 **Contributing**
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 📞 **Support**
- **Issues**: [GitHub Issues](https://github.com/risterz/VidHarvester/issues)
- **Discussions**: [GitHub Discussions](https://github.com/risterz/VidHarvester/discussions)
- **Documentation**: [Wiki](https://github.com/risterz/VidHarvester/wiki)

---

**Full Changelog**: Initial release

**Download now and start harvesting videos!** 🎬