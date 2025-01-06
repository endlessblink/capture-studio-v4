from PySide6.QtCore import QObject, Signal, Slot, Property, QRect, QPoint
from PySide6.QtGui import QScreen, QGuiApplication, QPixmap, QImage, QWindow
import numpy as np
import cv2
from pathlib import Path
import time
from loguru import logger
import platform
import os
import ctypes
from typing import List, Dict

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

class CaptureManager(QObject):
    recordingChanged = Signal(bool)
    captureComplete = Signal(str)  # Emits path to captured file
    errorOccurred = Signal(str)
    availableWindowsChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._recording = False
        self._video_writer = None
        self._capture_area = None
        self._selected_window = None
        self._fps = 30
        self._output_path = None
        self._available_windows = []
        self._update_window_list()
        logger.info("CaptureManager initialized")
        
    @Property(bool, notify=recordingChanged)
    def recording(self):
        logger.debug(f"Recording property accessed, value: {self._recording}")
        return self._recording
        
    @Property('QVariantList', notify=availableWindowsChanged)
    def availableWindows(self):
        return self._available_windows
        
    def _update_window_list(self):
        """Update the list of available windows."""
        if platform.system() == 'Windows':
            self._available_windows = []
            
            def callback(hwnd, _):
                if ctypes.windll.user32.IsWindowVisible(hwnd):
                    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        title = ctypes.create_unicode_buffer(length + 1)
                        ctypes.windll.user32.GetWindowTextW(hwnd, title, length + 1)
                        rect = ctypes.wintypes.RECT()
                        if ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                            self._available_windows.append({
                                'handle': hwnd,
                                'title': title.value,
                                'rect': QRect(rect.left, rect.top, 
                                            rect.right - rect.left,
                                            rect.bottom - rect.top)
                            })
                return True

            enum_windows = ctypes.windll.user32.EnumWindows
            enum_windows(WNDENUMPROC(callback), 0)
            
            self.availableWindowsChanged.emit()
        
    @Slot('QVariant')
    def set_capture_area(self, area):
        """Set the area to capture. If None or invalid, captures full screen."""
        if area and isinstance(area, QRect) and area.isValid():
            self._capture_area = area
            self._selected_window = None
        else:
            self._capture_area = None
            self._selected_window = None
        logger.info(f"Capture area set to: {self._capture_area}")
        
    @Slot('QVariant')
    def set_selected_window(self, window_info):
        """Set the window to capture."""
        if window_info and isinstance(window_info, dict):
            self._selected_window = window_info
            self._capture_area = window_info['rect']
        else:
            self._selected_window = None
            self._capture_area = None
        logger.info(f"Selected window set to: {self._selected_window}")
        
    def _grab_screen(self) -> QPixmap:
        """Capture the current screen or selected area."""
        screen = QGuiApplication.primaryScreen()
        if self._selected_window:
            # Update window position in case it moved
            rect = ctypes.wintypes.RECT()
            if ctypes.windll.user32.GetWindowRect(
                self._selected_window['handle'],
                ctypes.byref(rect)
            ):
                self._capture_area = QRect(
                    rect.left, rect.top,
                    rect.right - rect.left,
                    rect.bottom - rect.top
                )
        
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