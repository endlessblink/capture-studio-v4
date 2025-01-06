requirements-dev.txt

# Development tools
pyinstaller>=5.13.0  # Application packaging
python-dotenv>=1.0.0  # Environment management
loguru>=0.7.0  # Better logging

# Debugging
debugpy>=1.6.7  # Python debugger
memory_profiler>=0.61.0  # Memory profiling
line_profiler>=4.1.1  # Line-by-line profiling

# Testing extras
pytest-mock>=3.11.1  # Mocking support
pytest-benchmark>=4.0.0  # Performance testing
pytest-timeout>=2.1.0  # Test timeouts
pytest-xdist>=3.3.1  # Parallel testing

# Documentation extras
sphinx-autodoc-typehints>=1.24.0  # Type hint support in docs
sphinx-copybutton>=0.5.2  # Copy button for code blocks
sphinx-design>=0.5.0  # Enhanced doc components

# Code quality extras
bandit>=1.7.5  # Security checks
flake8>=6.1.0  # Style guide enforcement
flake8-bugbear>=23.7.10  # Additional error checks
pytype>=2023.8.22  # Static type checker

# Git hooks
pre-commit>=3.3.3  # Pre-commit framework
commitizen>=3.6.0  # Commit message formatting

# Build tools
build>=1.0.3  # PEP 517 package builder
twine>=4.0.2  # Package upload
check-manifest>=0.49  # Package manifest verification