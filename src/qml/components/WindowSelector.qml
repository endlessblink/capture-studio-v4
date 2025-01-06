import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

Window {
    id: root
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
    color: "#80000000"
    
    property var selectedWindow: null
    signal windowSelected(var windowInfo)
    signal selectionCancelled
    
    ListView {
        id: windowList
        anchors.centerIn: parent
        width: 400
        height: Math.min(contentHeight, 500)
        model: captureManager.availableWindows
        spacing: 8
        clip: true
        
        delegate: Rectangle {
            width: windowList.width
            height: 60
            color: "#2C2C2C"
            radius: 4
            border.color: mouseArea.containsMouse ? "#A0A0A0" : "transparent"
            border.width: 1
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 12
                
                Image {
                    Layout.preferredWidth: 44
                    Layout.preferredHeight: 44
                    source: modelData.icon || ""
                    sourceSize.width: 44
                    sourceSize.height: 44
                }
                
                Label {
                    Layout.fillWidth: true
                    text: modelData.title || ""
                    color: "#FFFFFF"
                    elide: Text.ElideRight
                    font.pixelSize: 14
                }
            }
            
            MouseArea {
                id: mouseArea
                anchors.fill: parent
                hoverEnabled: true
                onClicked: {
                    root.selectedWindow = modelData
                    root.windowSelected(modelData)
                    root.close()
                }
            }
        }
    }
    
    // Close on Escape key
    Item {
        focus: true
        Keys.onEscapePressed: {
            root.selectionCancelled()
            root.close()
        }
    }
    
    Component.onCompleted: {
        setX(0)
        setY(0)
        showFullScreen()
    }
} 