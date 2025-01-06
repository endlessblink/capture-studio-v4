contributing.md

# Contributing to CaptureStudio

## Development Environment Setup

### Required Software
- Python 3.10+
- GStreamer 1.20+ with development files
- Qt 6.5+ (installed via PySide6)
- Git
- Visual Studio Code (recommended)

### Recommended VS Code Extensions
- Python
- Pylance
- Qt for Python
- QML
- GitLens
- Python Test Explorer
- mypy Type Checker

### Code Style
We use several tools to maintain code quality:
- black for code formatting
- pylint for linting
- mypy for type checking
- pre-commit for git hooks

### Setting Up Pre-commit Hooks
```bash
pre-commit install
```

## Development Workflow

### 1. Creating a New Feature
1. Create a new branch from main:
```bash
git checkout -b feature/your-feature-name
```

2. Follow the feature implementation pattern:
   - Write tests first (TDD approach)
   - Implement the feature
   - Add documentation
   - Update QML/UI if needed
   - Run tests and type checking

3. Commit your changes:
```bash
git add .
git commit -m "feat: your feature description"
```

### 2. Code Organization
- Keep modules focused and small
- Follow the MVVM pattern
- Use dependency injection
- Keep UI logic separate from business logic

### 3. QML/UI Development
- Use Qt Quick/QML for all UI components
- Follow Material Design guidelines
- Support both light and dark themes
- Ensure responsive layouts
- Use Qt's property binding system

### 4. Testing
- Write unit tests for all new features
- Include integration tests for UI components
- Test on all supported platforms
- Maintain 80%+ code coverage

### 5. Documentation
- Document all public APIs
- Include docstrings with type hints
- Add comments for complex logic
- Update README.md when needed
- Document QML components

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Run code quality checks:
```bash
black .
pylint src tests
mypy src
pytest
```

4. Create a Pull Request with:
   - Clear description
   - Screenshots for UI changes
   - Test coverage report
   - List of major changes

## Release Process

1. Version Bump
   - Update version in `src/config.py`
   - Update CHANGELOG.md
   - Create version commit

2. Testing
   - Run full test suite
   - Test on all platforms
   - Verify documentation

3. Release
   - Create GitHub release
   - Build installers
   - Update download links

## Debugging Tips

### GStreamer Pipeline Debugging
```bash
# Enable GStreamer debug output
export GST_DEBUG=4
```

### Qt/QML Debugging
- Use Qt Creator for QML debugging
- Enable Qt Quick debugging in VS Code
- Use Qt's logging categories

### Common Issues
- GStreamer plugin missing
- Qt/QML binding issues
- Platform-specific capture problems
- Memory leaks in capture pipeline

## Performance Optimization

### Profiling
- Use cProfile for Python code
- Use Qt Creator for QML profiling
- Monitor memory usage
- Check CPU utilization

### Best Practices
- Use Qt Quick where possible
- Implement lazy loading
- Cache expensive operations
- Use hardware acceleration

## Security Considerations

- Validate all user input
- Handle device permissions properly
- Secure storage of user preferences
- Safe file handling
- Protected system API access