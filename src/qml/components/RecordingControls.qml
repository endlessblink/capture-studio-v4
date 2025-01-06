import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    color: "transparent"
    
    property bool isRecording: screenRecorder.recording
    
    RowLayout {
        anchors.centerIn: parent
        spacing: 20
        
        Button {
            text: isRecording ? "Stop Recording" : "Start Recording"
            highlighted: isRecording
            
            onClicked: {
                if (isRecording) {
                    screenRecorder.stop_recording()
                } else {
                    screenRecorder.start_recording()
                }
            }
        }
        
        Label {
            text: isRecording ? "Recording..." : "Ready"
            color: isRecording ? Material.color(Material.Red) : Material.foreground
        }
    }
} 