# Contributing to VidHarvester

🎉 **Thank you for your interest in contributing to VidHarvester!** 🎉

We welcome contributions from everyone. Here's how you can help make VidHarvester better.

## 🤝 How to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When you create a bug report, please include:

- **Clear description** of the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)
- **Log files** if available

### ✨ Suggesting Features

We love feature suggestions! Please:

- **Check existing issues** for similar suggestions
- **Describe the feature** clearly and concisely
- **Explain the use case** and why it would be beneficial
- **Consider implementation** if you have ideas

### 💻 Code Contributions

#### Getting Started

1. **Fork** the repository
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/VidHarvester.git
   cd VidHarvester
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
5. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

##### Code Style
- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep line length under **88 characters**
- Use **meaningful variable names**

##### Code Quality
- Run linting before submitting:
  ```bash
  flake8 src/
  isort src/
  ```
- Add **tests** for new features
- Ensure **existing tests** pass
- Update **documentation** as needed

##### Commit Messages
- Use **clear, descriptive** commit messages
- Start with a **verb** (Add, Fix, Update, etc.)
- Keep first line under **50 characters**
- Add detailed description if needed

Example:
```
Add support for custom output filename templates

- Implement template parsing with placeholders
- Add validation for invalid template strings
- Update GUI to show template preview
- Add tests for template functionality
```

#### Testing

- **Run tests** before submitting:
  ```bash
  python -m pytest tests/
  ```
- **Add tests** for new functionality
- **Update tests** if you modify existing code
- Ensure **cross-platform compatibility**

#### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update README.md** with details of changes if applicable
5. **Submit the pull request** with:
   - Clear title describing the change
   - Detailed description of what was changed
   - Reference to any related issues
   - Screenshots for UI changes

## 📋 Development Setup

### Directory Structure
```
src/vidharvester/
├── capture/          # URL capture functionality
├── database/         # Database management
├── download/         # Download engine
├── gui/             # PyQt6 user interface
└── utils/           # Utility functions
```

### Key Technologies
- **PyQt6**: GUI framework
- **yt-dlp**: Video downloading engine
- **SQLite**: Database storage
- **mitmproxy**: Proxy functionality
- **Playwright**: Browser automation

### Running from Source
```bash
# Start the application
python run.py

# Run with debug logging
PYTHONPATH=src python -m vidharvester.app
```

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

- **🔧 New Features**: Additional capture methods, UI improvements
- **🐛 Bug Fixes**: Stability improvements, edge case handling
- **📚 Documentation**: Code comments, user guides, tutorials
- **🧪 Testing**: Unit tests, integration tests, manual testing
- **🌍 Internationalization**: Translations for different languages
- **♿ Accessibility**: Making the app more accessible
- **🎨 UI/UX**: Design improvements, usability enhancements

## 📝 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

## 💬 Questions?

If you have questions about contributing:

- 💬 **Start a discussion** in GitHub Discussions
- 🐛 **Open an issue** for bugs or feature requests
- 📧 **Contact the maintainers** if needed

---

**Thank you for helping make VidHarvester better!** 🚀
