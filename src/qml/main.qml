import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import "components"

ApplicationWindow {
    id: mainWindow
    visible: false
    width: 1280
    height: 720
    title: qsTr("CaptureStudio")
    
    // Properties
    property bool isRecording: captureManager.recording
    
    // Floating toolbar
    FloatingToolbar {
        id: toolbar
        visible: true
        isRecording: mainWindow.isRecording
        
        Component.onCompleted: {
            // Position the toolbar in the center of the screen
            var screen = Qt.application.screens[0]
            x = (screen.width - width) / 2
            y = screen.height - height - 100
            show()
        }
        
        onModeChanged: function(mode) {
            if (mode === "area") {
                var selector = areaSelector.createObject(null)
                selector.show()
            } else if (mode === "window") {
                var windowSelector = windowSelectorComponent.createObject(null)
                windowSelector.show()
            } else if (mode === "display") {
                captureManager.set_capture_area(null)
                captureManager.set_selected_window(null)
            }
        }
        
        onRecordingToggled: function(start) {
            if (start) {
                captureManager.start_recording(null)
            } else {
                captureManager.stop_recording()
            }
        }
        
        onSettingsClicked: {
            settingsDialog.open()
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
    
    // Window selector component
    Component {
        id: windowSelectorComponent
        
        WindowSelector {
            onWindowSelected: function(windowInfo) {
                captureManager.set_selected_window(windowInfo)
            }
            onSelectionCancelled: {
                captureManager.set_selected_window(null)
            }
        }
    }
    
    // Settings dialog
    Dialog {
        id: settingsDialog
        title: qsTr("Settings")
        width: 400
        height: 300
        anchors.centerIn: parent
        
        ColumnLayout {
            anchors.fill: parent
            spacing: 20
            
            Label {
                text: qsTr("Recording Settings")
                font.bold: true
                font.pixelSize: 16
            }
            
            Item {
                Layout.fillHeight: true
            }
        }
        
        standardButtons: Dialog.Ok | Dialog.Cancel
    }
    
    // Error dialog
    Dialog {
        id: errorDialog
        title: qsTr("Error")
        width: 400
        
        property alias text: errorLabel.text
        
        Label {
            id: errorLabel
            width: parent.width
            wrapMode: Text.WordWrap
        }
        
        standardButtons: Dialog.Ok
    }
    
    // Capture complete dialog
    Dialog {
        id: captureCompleteDialog
        title: qsTr("Capture Complete")
        width: 400
        
        property alias text: completeLabel.text
        
        Label {
            id: completeLabel
            width: parent.width
            wrapMode: Text.WordWrap
        }
        
        standardButtons: Dialog.Ok
    }
    
    Connections {
        target: captureManager
        
        function onErrorOccurred(error) {
            errorDialog.text = error
            errorDialog.open()
        }
        
        function onCaptureComplete(path) {
            captureCompleteDialog.text = qsTr("Saved to: ") + path
            captureCompleteDialog.open()
        }
        
        function onRecordingChanged(recording) {
            mainWindow.isRecording = recording
        }
    }
} 