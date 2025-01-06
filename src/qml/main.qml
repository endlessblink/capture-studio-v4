import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import "components"

Window {
    id: root
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
    color: "transparent"
    width: 1280
    height: 720
    visible: false
    
    Rectangle {
        id: background
        anchors.fill: parent
        color: "#2C2C2C"
        radius: 8
    }
    
    // Properties
    property bool isRecording: captureManager.recording
    
    // Floating toolbar
    FloatingToolbar {
        id: toolbar
        visible: true
        isRecording: root.isRecording
        
        Component.onCompleted: {
            var screen = Qt.application.screens[0]
            x = (screen.width - width) / 2
            y = screen.height - height - 100
            show()
        }
        
        onModeChanged: function(mode) {
            if (mode === "area") {
                var selector = areaSelector.createObject(null)
                selector.show()
            } else if (mode === "display") {
                captureManager.set_capture_area(null)
            }
        }
        
        onRecordingToggled: function(start) {
            if (start) {
                captureManager.start_recording(null)
            } else {
                captureManager.stop_recording()
            }
        }
    }
    
    // Area selector component
    Component {
        id: areaSelector
        AreaSelector {
            onAreaSelected: function(area) {
                captureManager.set_capture_area(area)
            }
            onSelectionCancelled: {
                captureManager.set_capture_area(null)
            }
        }
    }
    
    Connections {
        target: captureManager
        
        function onErrorOccurred(error) {
            console.error(error)
        }
        
        function onCaptureComplete(path) {
            console.log("Capture saved to: " + path)
        }
        
        function onRecordingChanged(recording) {
            root.isRecording = recording
        }
    }
} 