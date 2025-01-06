import QtQuick
import QtQuick.Controls

ToolButton {
    id: control
    
    property string tooltipText: ""
    
    ToolTip {
        id: buttonToolTip
        parent: control
        text: control.tooltipText
        visible: control.hovered
        delay: 500
        timeout: 5000
        y: -height - 8
        x: (parent.width - width) / 2
    }
} 