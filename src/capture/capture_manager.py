from PySide6.QtCore import QObject, Signal, Slot, Property, QRect
from PySide6.QtGui import QScreen, QGuiApplication, QPixmap, QImage
import numpy as np
import cv2
from pathlib import Path
import time
from loguru import logger
import platform
import os
import ctypes

class CaptureManager(QObject):
    recordingChanged = Signal(bool)
    captureComplete = Signal(str)  # Emits path to captured file
    errorOccurred = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._recording = False
        self._video_writer = None
        self._capture_area = None
        self._fps = 30
        self._output_path = None
        logger.info("CaptureManager initialized")
        
    @Property(bool, notify=recordingChanged)
    def recording(self):
        logger.debug(f"Recording property accessed, value: {self._recording}")
        return self._recording
        
    @Slot('QVariant')
    def set_capture_area(self, area):
        """Set the area to capture. If None or invalid, captures full screen."""
        if area and isinstance(area, QRect) and area.isValid():
            self._capture_area = area
        else:
            self._capture_area = None
        logger.info(f"Capture area set to: {self._capture_area}")
        
    def _grab_screen(self) -> QPixmap:
        """Capture the current screen or selected area."""
        screen = QGuiApplication.primaryScreen()
        if self._capture_area and self._capture_area.isValid():
            return screen.grabWindow(0, self._capture_area.x(), 
                                   self._capture_area.y(),
                                   self._capture_area.width(), 
                                   self._capture_area.height())
        return screen.grabWindow(0)
        
    def _qimage_to_numpy(self, qimage):
        """Convert QImage to numpy array."""
        # Convert the QImage to RGB888 format
        img_rgb = qimage.convertToFormat(QImage.Format_RGB888)
        width = img_rgb.width()
        height = img_rgb.height()
        
        # Create a numpy array from the QImage data using buffer protocol
        ptr = img_rgb.constBits()
        # Create a memoryview and get its size
        view = memoryview(ptr).tobytes()
        
        # Reshape the raw data into an image array
        arr = np.frombuffer(view, dtype=np.uint8).reshape((height, width, 3))
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        
    def _ensure_output_directory(self, path):
        """Ensure the output directory exists."""
        output_dir = Path(path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
    @Slot(str, result=None)
    def start_recording(self, output_path: str = None):
        """Start screen recording."""
        logger.info("Start recording called")
        if self._recording:
            logger.info("Already recording, ignoring start request")
            return
            
        try:
            if not output_path:
                output_path = str(Path.home() / f"CaptureStudio_Recording_{int(time.time())}.avi")
                
            self._output_path = output_path
            self._ensure_output_directory(output_path)
                
            # Get screen dimensions
            screen = QGuiApplication.primaryScreen()
            if self._capture_area and self._capture_area.isValid():
                width = self._capture_area.width()
                height = self._capture_area.height()
            else:
                geometry = screen.geometry()
                width = geometry.width()
                height = geometry.height()
                
            logger.info(f"Setting up recording with dimensions: {width}x{height}")
            
            # Try different codecs if the first one fails
            codecs = ['DIVX', 'XVID', 'MJPG']
            for codec in codecs:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*codec)
                    test_path = str(Path(output_path).with_suffix('.avi'))
                    self._video_writer = cv2.VideoWriter(
                        test_path, fourcc, self._fps, (width, height)
                    )
                    if self._video_writer.isOpened():
                        self._output_path = test_path
                        break
                except Exception as e:
                    logger.warning(f"Codec {codec} failed: {str(e)}")
                    if self._video_writer:
                        self._video_writer.release()
                    continue
            
            if not self._video_writer or not self._video_writer.isOpened():
                raise Exception("Failed to initialize video writer with any supported codec")
            
            self._recording = True
            logger.info("Recording started successfully")
            self.recordingChanged.emit(True)
            logger.info(f"Started recording to {self._output_path}")
            
            # Start the recording loop in a separate thread
            from threading import Thread
            self._recording_thread = Thread(target=self._record_loop)
            self._recording_thread.daemon = True  # Make thread daemon so it doesn't block program exit
            self._recording_thread.start()
            
        except Exception as e:
            logger.error(f"Error starting recording: {str(e)}")
            self.errorOccurred.emit(str(e))
            self._cleanup()
            
    def _record_loop(self):
        """Main recording loop."""
        logger.info("Recording loop started")
        frames_written = 0
        try:
            while self._recording:
                # Capture frame
                pixmap = self._grab_screen()
                image = pixmap.toImage()
                
                try:
                    # Convert QImage to numpy array and write frame
                    frame = self._qimage_to_numpy(image)
                    
                    if self._video_writer and self._video_writer.isOpened():
                        self._video_writer.write(frame)
                        frames_written += 1
                    else:
                        raise Exception("Video writer closed unexpectedly")
                except Exception as e:
                    logger.error(f"Error processing frame: {str(e)}")
                    raise
                
                # Control FPS
                time.sleep(1/self._fps)
                
        except Exception as e:
            logger.error(f"Error in recording loop: {str(e)}")
            self.errorOccurred.emit(str(e))
        finally:
            logger.info(f"Recording loop ended. Frames written: {frames_written}")
            self._cleanup()
            if frames_written > 0:
                self.captureComplete.emit(self._output_path)
            
    @Slot(result=None)
    def stop_recording(self):
        """Stop screen recording."""
        logger.info("Stop recording called")
        if not self._recording:
            logger.info("Not recording, ignoring stop request")
            return
            
        try:
            self._recording = False
            if self._recording_thread:
                logger.info("Waiting for recording thread to finish...")
                self._recording_thread.join(timeout=5.0)  # Wait up to 5 seconds
            self._cleanup()
            logger.info("Recording stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping recording: {str(e)}")
            self.errorOccurred.emit(str(e))
            self._cleanup()
            
    def _cleanup(self):
        """Clean up resources."""
        if self._video_writer:
            self._video_writer.release()
            self._video_writer = None
        self._recording = False
        self.recordingChanged.emit(False)
        logger.info("Cleanup completed") 