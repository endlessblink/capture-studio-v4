from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtGui import QScreen, QGuiApplication
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from pathlib import Path
import time
from loguru import logger
import platform

class ScreenRecorder(QObject):
    recordingChanged = Signal(bool)
    errorOccurred = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._recording = False
        self._pipeline = None
        self._mainloop = None
        
        # Initialize GStreamer
        Gst.init(None)
        
    @Property(bool, notify=recordingChanged)
    def recording(self):
        return self._recording
        
    @Slot()
    def start_recording(self, output_path: str = None):
        if self._recording:
            return
            
        try:
            screen = QGuiApplication.primaryScreen()
            geometry = screen.geometry()
            
            if not output_path:
                output_path = str(Path.home() / f"CaptureStudio_{int(time.time())}.mp4")
            
            # Create GStreamer pipeline for screen recording
            if platform.system() == "Windows":
                pipeline_str = (
                    "gdiscreencapsrc ! "
                    "videorate ! video/x-raw,framerate=30/1 ! "
                    "videoconvert ! "
                    "vp8enc cpu-used=8 threads=4 deadline=1 ! "
                    "webmmux ! "
                    f"filesink location={output_path.replace('.mp4', '.webm')}"
                )
            else:
                pipeline_str = (
                    f"ximagesrc display-name={screen.name()} use-damage=false ! "
                    f"video/x-raw,framerate=30/1 ! "
                    "videoconvert ! "
                    "x264enc tune=zerolatency speed-preset=ultrafast ! "
                    "mp4mux ! "
                    f"filesink location={output_path}"
                )
            
            logger.info(f"Using pipeline: {pipeline_str}")
            self._pipeline = Gst.parse_launch(pipeline_str)
            
            # Start the pipeline
            ret = self._pipeline.set_state(Gst.State.PLAYING)
            if ret == Gst.StateChangeReturn.FAILURE:
                raise Exception("Failed to start pipeline")
                
            self._recording = True
            self.recordingChanged.emit(True)
            logger.info(f"Started recording to {output_path}")
            
        except Exception as e:
            logger.error(f"Error starting recording: {str(e)}")
            self.errorOccurred.emit(str(e))
            self._cleanup()
            
    @Slot()
    def stop_recording(self):
        if not self._recording:
            return
            
        try:
            # Send EOS event
            self._pipeline.send_event(Gst.Event.new_eos())
            
            # Wait for EOS message
            bus = self._pipeline.get_bus()
            msg = bus.timed_pop_filtered(
                Gst.CLOCK_TIME_NONE,
                Gst.MessageType.EOS | Gst.MessageType.ERROR
            )
            
            if msg.type == Gst.MessageType.ERROR:
                err, debug = msg.parse_error()
                raise Exception(f"Pipeline error: {err.message}")
                
            # Stop the pipeline
            self._pipeline.set_state(Gst.State.NULL)
            logger.info("Stopped recording")
            
        except Exception as e:
            logger.error(f"Error stopping recording: {str(e)}")
            self.errorOccurred.emit(str(e))
            
        finally:
            self._cleanup()
            
    def _cleanup(self):
        if self._pipeline:
            self._pipeline.set_state(Gst.State.NULL)
            self._pipeline = None
        self._recording = False
        self.recordingChanged.emit(False) 