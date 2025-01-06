# CaptureStudio

A modern screen and camera recording application built with Python and Qt.

## Features

- Modern UI using Qt Quick/QML
- Screen capture functionality
- Camera capture support
- Audio recording
- Scene system for multiple layouts
- Hardware-accelerated recording
- Cross-platform compatibility

## Requirements

- Anaconda or Miniconda
- Python 3.10 or higher
- GStreamer (installed via conda)
- PySide6 (installed via conda)
- PyGObject (installed via conda)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/capturestudio.git
cd capturestudio
```

2. Initialize conda (Windows only, first time setup):
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
conda init powershell
# Close PowerShell and open a new window
```

3. Create and activate conda environment:
```bash
conda env create -f environment.yml
conda activate capturestudio
```

The environment.yml file includes all necessary dependencies including:
- PySide6 for the GUI
- GStreamer and its plugins for video processing
- PyGObject for GStreamer Python bindings
- Development tools (pytest, black, mypy)

## Running the Application

```bash
python src/main.py
```

## Development

- Follow PEP 8 guidelines
- Use type hints
- Run tests with pytest
- Format code with black
- Check types with mypy

### Development Commands

```bash
# Run tests
pytest

# Format code
black .

# Type checking
mypy src/

# Run the application in development mode
python src/main.py
```

## License

MIT License - see LICENSE file for details 