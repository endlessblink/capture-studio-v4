import QtQuick
import QtQuick.Controls
import QtQuick.Window

Window {
    id: root
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
    color: "#80000000"
    
    property rect selectedArea: Qt.rect(0, 0, 0, 0)
    signal areaSelected(rect area)
    signal selectionCancelled
    
    Rectangle {
        id: selectionRect
        visible: false
        color: "transparent"
        border.color: "#00A0FF"
        border.width: 2
        
        // Size info label
        Rectangle {
            color: "#00A0FF"
            height: 25
            width: sizeLabel.width + 20
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.margins: 5
            radius: 4
            
            Label {
                id: sizeLabel
                anchors.centerIn: parent
                text: Math.round(parent.parent.width) + " × " + Math.round(parent.parent.height)
                color: "white"
            }
        }
    }
    
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        
        property point startPoint
        
        onPressed: {
            if (mouse.button === Qt.RightButton) {
                root.selectionCancelled()
                root.close()
                return
            }
            
            startPoint = Qt.point(mouse.x, mouse.y)
            selectionRect.x = mouse.x
            selectionRect.y = mouse.y
            selectionRect.width = 0
            selectionRect.height = 0
            selectionRect.visible = true
        }
        
        onPositionChanged: {
            if (pressed && mouse.button === Qt.LeftButton) {
                var x = Math.min(startPoint.x, mouse.x)
                var y = Math.min(startPoint.y, mouse.y)
                var width = Math.abs(mouse.x - startPoint.x)
                var height = Math.abs(mouse.y - startPoint.y)
                
                selectionRect.x = x
                selectionRect.y = y
                selectionRect.width = width
                selectionRect.height = height
            }
        }
        
        onReleased: {
            if (mouse.button === Qt.LeftButton) {
                if (selectionRect.width > 10 && selectionRect.height > 10) {
                    root.selectedArea = Qt.rect(
                        selectionRect.x, selectionRect.y,
                        selectionRect.width, selectionRect.height
                    )
                    root.areaSelected(root.selectedArea)
                    root.close()
                } else {
                    selectionRect.visible = false
                }
            }
        }
    }
    
    Component.onCompleted: {
        setX(0)
        setY(0)
        showFullScreen()
    }
} 