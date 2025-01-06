import pytest
from PySide6.QtGui import QGuiApplication

@pytest.fixture(scope="session")
def qapp():
    """Create a QGuiApplication instance for the entire test session."""
    app = QGuiApplication.instance()
    if app is None:
        app = QGuiApplication([])
    yield app 