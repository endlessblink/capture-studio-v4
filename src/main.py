#!/usr/bin/env python3
"""
CaptureStudio Main Application

Stability Guidelines:
1. Resource Management:
   - Always import resources_rc
   - Use absolute paths with Path for QML files
   - Set up proper search paths for resources

2. QML Engine Setup:
   - Create QGuiApplication before QQmlEngine
   - Register all context properties before loading QML
   - Use QUrl.fromLocalFile for loading QML files

3. Error Handling:
   - Check engine.rootObjects() after loading QML
   - Use logger for debugging and error tracking
   - Handle application exit properly

4. Performance:
   - Initialize managers and heavy objects after GUI is loaded
   - Use Qt's event system for communication
   - Keep the main thread responsive
"""

import sys
from pathlib import Path
from PySide6.QtCore import QUrl, QDir
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from loguru import logger

# Import our capture manager
from capture.capture_manager import CaptureManager

# Import resources
import resources_rc

def main():
    # Set up logging
    logger.add("capturestudio.log", rotation="10 MB")
    logger.info("Starting CaptureStudio...")
    
    # Create the application instance
    logger.info("Creating QGuiApplication...")
    app = QGuiApplication(sys.argv)
    app.setApplicationName("CaptureStudio")
    app.setOrganizationName("CaptureStudio")
    
    # Create and register the capture manager
    logger.info("Creating CaptureManager...")
    capture_manager = CaptureManager()
    
    # Create the QML engine
    logger.info("Creating QML engine...")
    engine = QQmlApplicationEngine()
    
    # Set up the import paths for QML
    logger.info("Setting up QML import paths...")
    qml_dir = Path(__file__).parent / "qml"
    engine.addImportPath(str(qml_dir))
    
    # Register the capture manager with QML
    logger.info("Registering capture manager with QML...")
    engine.rootContext().setContextProperty("captureManager", capture_manager)
    
    # Load the main QML file
    qml_file = qml_dir / "main.qml"
    logger.info(f"Loading QML file: {qml_file}")
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    
    # Check if QML loaded successfully
    if not engine.rootObjects():
        logger.error("Failed to load QML")
        return -1
    
    logger.info("Starting event loop...")
    # Start the event loop
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 