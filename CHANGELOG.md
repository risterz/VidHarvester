# Changelog

All notable changes to VidHarvester will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup and architecture
- Core video downloading functionality
- PyQt6 user interface with modern design
- Multiple capture methods (extensions, proxy, direct)
- Browser extensions for Chrome and Firefox
- mitmproxy integration for transparent capture
- Queue management with concurrent downloads
- Database storage for settings and history
- Theme support (dark/light modes)
- System tray integration
- Build scripts for Windows executables

### Features
- **Multi-format support**: MP4, WebM, MKV, MP3, M4A, FLAC, OGG
- **Quality selection**: Auto-best, 720p, 1080p, highest available
- **Advanced options**: Subtitle embedding, thumbnail extraction
- **Cookie support**: Authenticated downloads
- **Progress tracking**: Real-time progress with speed/ETA
- **Fallback capture**: Playwright-powered headless browser
- **Cross-platform**: Windows, Linux, macOS support

### Technical Details
- Built with Python 3.10+ and PyQt6
- Uses yt-dlp as the download engine
- SQLite database for persistence
- Multi-threaded architecture for performance
- Comprehensive error handling and logging

---

## Version History

### [0.1.0] - 2024-08-17

#### 🎉 Initial Release

**Core Features:**
- Complete video downloading application
- Modern PyQt6 GUI with dark/light themes
- Browser extension integration (Chrome/Firefox)
- Proxy-based capture via mitmproxy
- Queue management with progress tracking
- Format selection and quality options
- Settings persistence and download history

**Capture Methods:**
- Browser extensions for automatic URL capture
- HTTP proxy interception with mitmproxy
- Playwright fallback for complex sites
- Direct URL input with drag & drop

**Advanced Features:**
- Concurrent download management
- Cookie support for authenticated sites
- Subtitle and thumbnail embedding
- System tray integration with notifications
- Cross-platform build scripts

**Technical Implementation:**
- Python 3.10+ with modern async/await patterns
- PyQt6 for cross-platform GUI
- yt-dlp for robust video extraction
- SQLite for local data storage
- Threading for non-blocking operations

---

## Future Roadmap

### Planned Features
- [ ] **Auto-update system** for seamless updates
- [ ] **Playlist support** for batch downloads
- [ ] **Download scheduling** with cron-like functionality
- [ ] **Cloud storage integration** (Google Drive, Dropbox)
- [ ] **Mobile app companion** for remote control
- [ ] **Plugin architecture** for extensibility
- [ ] **Advanced filtering** and search in history
- [ ] **Statistics dashboard** with download analytics

### Technical Improvements
- [ ] **Performance optimization** for large queues
- [ ] **Memory usage optimization** for long-running sessions
- [ ] **Network retry logic** with exponential backoff
- [ ] **Bandwidth limiting** and QoS controls
- [ ] **Multi-language support** (i18n)
- [ ] **Accessibility improvements** (a11y)
- [ ] **Unit test coverage** expansion
- [ ] **CI/CD pipeline** setup

---

*This changelog is maintained by the VidHarvester development team.*
