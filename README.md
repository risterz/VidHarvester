<div align="center">

# 🎬 VidHarvester

### *Professional Video Downloading Application*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)](https://pypi.org/project/PyQt6/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-powered-red.svg)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/risterz/VidHarvester)

*A comprehensive video downloading application with PyQt6 GUI, browser extension integration, and proxy-based video capture capabilities.*

[🚀 Quick Start](#-quick-start) • [📋 Features](#-features) • [📦 Installation](#-installation) • [🔧 Usage](#-usage) • [🛠️ Building](#️-building)

---

</div>

## 🌟 Overview

**VidHarvester** is a powerful, feature-rich video downloading application that combines the reliability of **yt-dlp** with an intuitive **PyQt6** interface. It offers multiple capture methods including browser extensions, proxy interception, and headless browser automation for maximum compatibility.

### ✨ Why VidHarvester?

- 🎯 **Smart Capture**: Multiple capture methods for maximum compatibility
- 🖥️ **Modern GUI**: Clean, responsive PyQt6 interface with dark/light themes
- 🔄 **Queue Management**: Download multiple videos with progress tracking
- 🧩 **Browser Integration**: Chrome/Firefox extensions for seamless capture
- 🔒 **Proxy Support**: Transparent capture via mitmproxy integration
- ⚡ **High Performance**: Concurrent downloads with speed optimization
- 📱 **Cross-Platform**: Works on Windows, Linux, and macOS

---

## 📋 Features

### 🎥 **Core Downloading**
- **Multi-format Support**: MP4, WebM, MKV, MP3, M4A, FLAC, OGG
- **Quality Selection**: Auto-best, 720p, 1080p, highest available
- **Subtitle Embedding**: Automatic subtitle download and embedding
- **Thumbnail Embedding**: Extract and embed video thumbnails
- **Cookie Support**: Authenticated downloads with browser cookies

### 🔌 **Capture Methods**
- **Browser Extensions**: Chrome & Firefox extensions for automatic capture
- **Proxy Interception**: mitmproxy integration for transparent capture
- **Headless Browser**: Playwright-powered fallback capture
- **Direct URL**: Manual URL input with drag & drop support

### 🖥️ **User Interface**
- **Modern Design**: Clean, intuitive PyQt6 interface
- **Theme Support**: Dark and light themes
- **Progress Tracking**: Real-time download progress with speed/ETA
- **Queue Management**: Add, pause, resume, and cancel downloads
- **History Tracking**: Complete download history with statistics
- **System Tray**: Minimize to tray with notifications

### ⚙️ **Advanced Features**
- **Concurrent Downloads**: Configurable simultaneous download limit
- **Format Probing**: Analyze available formats before downloading
- **FFmpeg Integration**: Advanced video processing and conversion
- **Database Storage**: SQLite-based settings and history
- **Logging System**: Comprehensive logging for troubleshooting

---

## 📦 Installation

### 📋 **Prerequisites**

- **Python 3.10+** 
- **FFmpeg** (for video processing)
- **Chrome/Firefox** (for browser extensions)

### 🚀 **Quick Install**

```bash
# Clone the repository
git clone https://github.com/risterz/VidHarvester.git
cd VidHarvester

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### 🔧 **FFmpeg Installation**

**Windows:**
```bash
# Using chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg
```

---

## 🔧 Usage

### 🚀 **Basic Usage**

1. **Launch Application**
   ```bash
   python run.py
   ```

2. **Download a Video**
   - Paste URL in the input field
   - Select format and quality
   - Click "Download" or press Enter

3. **Browser Extension Setup**
   - **Chrome**: Load `extensions/chrome/` as unpacked extension
   - **Firefox**: Load `extensions/firefox/manifest.json` as temporary add-on

### 🕷️ **Proxy Mode (Advanced)**

1. **Install mitmproxy**
   ```bash
   pip install mitmproxy
   ```

2. **Start Proxy Capture**
   ```bash
   mitmdump -s proxy/mitm_addon.py
   ```

3. **Configure Browser**
   - Set HTTP proxy to `127.0.0.1:8080`
   - Install mitmproxy certificate for HTTPS

4. **Enable in VidHarvester**
   - Right-click system tray icon
   - Select "Start Capture"

### ⚙️ **Configuration**

- **Output Directory**: Set default download location
- **Concurrent Downloads**: Control simultaneous downloads (1-10)
- **Themes**: Switch between dark and light modes
- **Cookies**: Import browser cookies for authenticated downloads

---

## 🛠️ Building

### 📦 **Windows Executable**

```bash
# Install build dependencies
pip install -r requirements-dev.txt

# Build using PowerShell
scripts\build_windows.ps1

# Or using Command Prompt
scripts\build_windows.bat
```

**Output**: `dist/VidHarvester/VidHarvester.exe`

### 📱 **One-File Executable**

```bash
pyinstaller VidHarvester-OneFile.spec
```

**Output**: `dist/VidHarvester-OneFile.exe`

### 🎁 **Windows Installer**

```bash
# Requires NSIS
makensis scripts\installer.nsi
```

**Output**: `VidHarvester-Setup-0.1.0.exe`

---

## 📁 Project Structure

```
VidHarvester/
├── 📂 src/vidharvester/           # Main application source
│   ├── 📂 capture/                # URL capture modules
│   ├── 📂 database/               # SQLite database management
│   ├── 📂 download/               # Download engine & queue
│   ├── 📂 gui/                    # PyQt6 user interface
│   └── 📂 utils/                  # Utility functions
├── 📂 extensions/                 # Browser extensions
│   ├── 📂 chrome/                 # Chrome extension
│   └── 📂 firefox/                # Firefox extension
├── 📂 proxy/                      # mitmproxy addon
├── 📂 scripts/                    # Build & packaging scripts
├── 📄 requirements.txt            # Python dependencies
└── 📄 run.py                      # Application entry point
```

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Runtime dependencies |
| `requirements-dev.txt` | Development dependencies |
| `pyproject.toml` | Project metadata & build config |
| `setup.cfg` | Code style & linting config |
| `VidHarvester.spec` | PyInstaller build specification |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🍴 Fork** the repository
2. **🌿 Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **💾 Commit** your changes: `git commit -m 'Add amazing feature'`
4. **📤 Push** to the branch: `git push origin feature/amazing-feature`
5. **🔄 Open** a Pull Request

### 📝 **Development Guidelines**

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure cross-platform compatibility

---

## 🐛 Troubleshooting

### Common Issues

**❌ "No module named 'vidharvester'"**
```bash
# Ensure you're running from the project root
python run.py
```

**❌ "FFmpeg not found"**
```bash
# Install FFmpeg and ensure it's in PATH
ffmpeg -version
```

**❌ "mitmproxy certificate error"**
```bash
# Install mitmproxy certificate
mitmdump  # Follow certificate installation prompts
```

### 📊 **Performance Tips**

- **Increase concurrent downloads** for faster batch processing
- **Use SSD storage** for improved I/O performance  
- **Enable hardware acceleration** in FFmpeg settings
- **Clear browser cache** if extension capture fails

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Powerful video downloading engine
- **[PyQt6](https://pypi.org/project/PyQt6/)** - Cross-platform GUI framework
- **[mitmproxy](https://mitmproxy.org/)** - HTTP/HTTPS proxy capabilities
- **[Playwright](https://playwright.dev/)** - Browser automation framework

---

<div align="center">

### ⭐ **If you find VidHarvester useful, please consider giving it a star!** ⭐

**[🐛 Report Bug](https://github.com/risterz/VidHarvester/issues)** • **[✨ Request Feature](https://github.com/risterz/VidHarvester/issues)** • **[💬 Discussions](https://github.com/risterz/VidHarvester/discussions)**

---

*Made with ❤️ by the VidHarvester Team*

</div>