import sys
from pathlib import Path
import pytest
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

@pytest.fixture
def app(qapp):
    return qapp

@pytest.fixture
def engine(app):
    engine = QQmlApplicationEngine()
    yield engine
    engine.deleteLater()

def test_qml_loads(app, engine):
    # Get the path to main.qml
    qml_file = Path(__file__).parent.parent / "src" / "qml" / "main.qml"
    assert qml_file.exists(), f"QML file not found at {qml_file}"
    
    # Load the QML file
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    
    # Check if QML loaded successfully
    assert engine.rootObjects(), "Failed to load QML file"
    
    # Verify the main window title
    root_object = engine.rootObjects()[0]
    assert root_object.title() == "CaptureStudio"

def test_window_properties(app, engine):
    qml_file = Path(__file__).parent.parent / "src" / "qml" / "main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    
    root_object = engine.rootObjects()[0]
    
    # Test window dimensions
    assert root_object.width() == 1280
    assert root_object.height() == 720
    
    # Test visibility
    assert root_object.isVisible() == True 