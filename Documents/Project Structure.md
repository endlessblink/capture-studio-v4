Project Structure.md

# CaptureStudio Project Structure

```
capturestudio/
├── src/                        # Source code
│   ├── ui/                    # UI components
│   │   ├── components/       # Reusable UI components
│   │   │   ├── buttons/     # Button components
│   │   │   ├── controls/    # Control components
│   │   │   └── widgets/     # Widget components
│   │   ├── views/           # Application views
│   │   │   ├── main/       # Main window view
│   │   │   ├── settings/   # Settings views
│   │   │   └── capture/    # Capture views
│   │   ├── themes/          # Theme definitions
│   │   │   ├── dark/       # Dark theme
│   │   │   └── light/      # Light theme
│   │   └── bindings/        # Python-QML bindings
│   │
│   ├── capture/              # Capture system
│   │   ├── screen/          # Screen capture
│   │   ├── camera/          # Camera capture
│   │   ├── audio/           # Audio capture
│   │   └── devices/         # Device management
│   │
│   ├── processing/           # Media processing
│   │   ├── pipeline/        # GStreamer pipeline
│   │   ├── effects/         # Video/audio effects
│   │   ├── encoding/        # Media encoding
│   │   └── output/          # Output management
│   │
│   ├── core/                 # Core functionality
│   │   ├── config/          # Configuration
│   │   ├── utils/           # Utilities
│   │   ├── logging/         # Logging system
│   │   └── plugins/         # Plugin system
│   │
│   └── main.py              # Application entry point
│
├── tests/                     # Test files
│   ├── unit/                # Unit tests
│   │   ├── ui/             # UI tests
│   │   ├── capture/        # Capture tests
│   │   └── processing/     # Processing tests
│   │
│   ├── integration/         # Integration tests
│   │   ├── capture/        # Capture integration
│   │   └── processing/     # Processing integration
│   │
│   └── fixtures/            # Test fixtures
│
├── docs/                      # Documentation
│   ├── user/                # User documentation
│   │   ├── getting_started/ # Getting started guide
│   │   ├── features/       # Feature documentation
│   │   └── troubleshooting/ # Troubleshooting guide
│   │
│   ├── development/         # Development documentation
│   │   ├── setup/          # Setup guide
│   │   ├── architecture/   # Architecture docs
│   │   └── api/           # API documentation
│   │
│   └── design/             # Design documentation
│       ├── ui/            # UI design docs
│       └── assets/        # Design assets
│
├── resources/                 # Application resources
│   ├── icons/               # Application icons
│   ├── images/              # Image resources
│   ├── styles/              # Style resources
│   └── translations/        # Translation files
│
├── tools/                     # Development tools
│   ├── build/               # Build scripts
│   ├── packaging/           # Packaging tools
│   └── scripts/             # Utility scripts
│
├── .github/                   # GitHub configuration
│   ├── workflows/           # GitHub Actions
│   └── ISSUE_TEMPLATE/      # Issue templates
│
├── .vscode/                   # VSCode configuration
│   └── settings.json        # Editor settings
│
├── .gitignore                # Git ignore rules
├── .pre-commit-config.yaml   # Pre-commit config
├── LICENSE                   # License file
├── MANIFEST.in               # Package manifest
├── pyproject.toml            # Project metadata
├── README.md                 # Project readme
├── requirements.txt          # Core dependencies
└── requirements-dev.txt      # Development dependencies
```

## Directory Details

### Source Code (`src/`)

- `ui/`: User interface components
  - Modern, responsive design using Qt Quick/QML
  - Reusable components for consistency
  - Theme support for customization

- `capture/`: Media capture implementation
  - Screen capture with multi-monitor support
  - Camera capture with device selection
  - Audio capture with device management

- `processing/`: Media processing system
  - GStreamer pipeline management
  - Video/audio effect processing
  - Output format handling

- `core/`: Core application functionality
  - Configuration management
  - Utility functions
  - Logging system
  - Plugin architecture

### Tests (`tests/`)

- `unit/`: Unit test suite
  - Component-level testing
  - Mock-based testing
  - Coverage reporting

- `integration/`: Integration tests
  - System-level testing
  - End-to-end scenarios
  - Performance testing

### Documentation (`docs/`)

- `user/`: End-user documentation
  - Getting started guide
  - Feature documentation
  - Troubleshooting help

- `development/`: Developer documentation
  - Setup instructions
  - Architecture overview
  - API reference

### Resources (`resources/`)

- Application assets
- Localization files
- Theme resources
- Icon sets

### Tools (`tools/`)

- Build automation
- Packaging scripts
- Development utilities
- CI/CD tools

## Key Files

- `pyproject.toml`: Project configuration
- `requirements.txt`: Core dependencies
- `requirements-dev.txt`: Development dependencies
- `.pre-commit-config.yaml`: Code quality checks
- `MANIFEST.in`: Package manifest
- `LICENSE`: Project license

## Development Guidelines

1. Follow directory structure
2. Keep modules focused
3. Write comprehensive tests
4. Update documentation
5. Maintain clean architecture