readme.md

# CaptureStudio

A modern screen and camera recording application built with Python and Qt.

## Features

- Screen recording with multi-monitor support
- Camera capture with device selection
- Audio recording with device selection
- Modern, intuitive user interface
- Scene system for complex layouts
- Hardware-accelerated video processing
- Multiple output formats
- Customizable hotkeys
- Plugin system for effects

## Prerequisites

- Python 3.10 or higher
- Qt 6.5 or higher
- GStreamer 1.20 or higher with development files
- Git (for development)

### Windows

1. Install Python from [python.org](https://python.org)
2. Install Qt from [qt.io](https://qt.io)
3. Install GStreamer from [gstreamer.freedesktop.org](https://gstreamer.freedesktop.org)

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.10 python3.10-dev
sudo apt install qt6-base-dev qt6-declarative-dev
sudo apt install libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good
```

### macOS

```bash
brew install python@3.10
brew install qt@6
brew install gstreamer
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/capturestudio.git
cd capturestudio
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Development Setup

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
pytest
```

## Usage

1. Start the application:
```bash
python src/main.py
```

2. Select capture sources:
   - Choose screen region or window
   - Select camera device
   - Configure audio input

3. Configure output:
   - Set output format
   - Choose quality settings
   - Select destination folder

4. Start recording:
   - Use start/stop buttons
   - Or use configured hotkeys

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Documentation

- [User Guide](docs/user/README.md)
- [Development Guide](docs/development/DEVELOPMENT.md)
- [Architecture Overview](docs/development/ARCHITECTURE.md)
- [API Reference](docs/api/README.md)

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Qt for the GUI framework
- GStreamer for media processing
- Python community for tools and libraries
- Contributors and users

## Support

- [Issue Tracker](https://github.com/yourusername/capturestudio/issues)
- [Discussions](https://github.com/yourusername/capturestudio/discussions)
- [Documentation](https://capturestudio.readthedocs.io)