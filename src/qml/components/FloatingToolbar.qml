/*
  Stability Guidelines:
  1. Keep the basic Window structure:
     - Use Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
     - Transparent background with solid Rectangle inside
  2. Use only stable imports:
     - QtQuick
     - QtQuick.Controls (not .Material)
     - QtQuick.Layouts
     - QtQuick.Window
  3. Use proper resource paths:
     - "qrc:/icons/..." for all resources
  4. Avoid:
     - Material theme
     - DropShadow and other graphical effects
     - Dynamic colors
*/

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

Window {
    id: root
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
    color: "transparent"
    width: toolbarLayout.implicitWidth + 20
    height: toolbarLayout.implicitHeight + 20

    // Properties for capture modes
    property bool isDisplayMode: true
    property bool isWindowMode: false
    property bool isAreaMode: false
    property bool isDeviceMode: false
    property bool isCameraEnabled: false
    property bool isMicrophoneEnabled: false
    property bool isSystemAudioEnabled: false
    property bool isRecording: false

    // Signals
    signal modeChanged(string mode)
    signal cameraToggled(bool enabled)
    signal microphoneToggled(bool enabled)
    signal systemAudioToggled(bool enabled)
    signal settingsClicked()
    signal recordingToggled(bool start)

    Rectangle {
        id: background
        anchors.fill: parent
        color: "#2C2C2C"
        radius: 8

        // Draggable area
        MouseArea {
            anchors.fill: parent
            property point clickPos: "0,0"
            
            function handleMousePressed(mouseX, mouseY) {
                clickPos = Qt.point(mouseX, mouseY)
            }
            
            function handleMouseMoved(mouseX, mouseY) {
                var delta = Qt.point(mouseX - clickPos.x, mouseY - clickPos.y)
                root.x += delta.x
                root.y += delta.y
            }
            
            onPressed: function(mouse) {
                handleMousePressed(mouse.x, mouse.y)
            }
            
            onPositionChanged: function(mouse) {
                handleMouseMoved(mouse.x, mouse.y)
            }
        }

        RowLayout {
            id: toolbarLayout
            anchors.centerIn: parent
            spacing: 8

            // Display/Screen selection
            ToolButton {
                icon.source: "qrc:/icons/display.svg"
                icon.color: isDisplayMode ? "#00A0FF" : "#808080"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                enabled: !isRecording
                onClicked: {
                    isDisplayMode = true
                    isWindowMode = false
                    isAreaMode = false
                    isDeviceMode = false
                    modeChanged("display")
                }
            }

            // Window selection
            ToolButton {
                icon.source: "qrc:/icons/window.svg"
                icon.color: isWindowMode ? "#00A0FF" : "#808080"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                enabled: !isRecording
                onClicked: {
                    isDisplayMode = false
                    isWindowMode = true
                    isAreaMode = false
                    isDeviceMode = false
                    modeChanged("window")
                }
            }

            // Area selection
            ToolButton {
                icon.source: "qrc:/icons/area.svg"
                icon.color: isAreaMode ? "#00A0FF" : "#808080"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                enabled: !isRecording
                onClicked: {
                    isDisplayMode = false
                    isWindowMode = false
                    isAreaMode = true
                    isDeviceMode = false
                    modeChanged("area")
                }
            }

            // Device selection
            ToolButton {
                icon.source: "qrc:/icons/device.svg"
                icon.color: isDeviceMode ? "#00A0FF" : "#808080"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                enabled: !isRecording
                onClicked: {
                    isDisplayMode = false
                    isWindowMode = false
                    isAreaMode = false
                    isDeviceMode = true
                    modeChanged("device")
                }
            }

            Rectangle {
                width: 1
                height: 24
                color: "#404040"
                Layout.alignment: Qt.AlignVCenter
            }

            // Record/Stop button
            ToolButton {
                id: recordButton
                icon.source: isRecording ? "qrc:/icons/stop.svg" : "qrc:/icons/record.svg"
                icon.color: isRecording ? "#FF4444" : "#44FF44"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                onClicked: recordingToggled(!isRecording)
            }

            Rectangle {
                width: 1
                height: 24
                color: "#404040"
                Layout.alignment: Qt.AlignVCenter
            }

            // Camera toggle
            ToolButton {
                icon.source: "qrc:/icons/camera.svg"
                icon.color: isCameraEnabled ? "#00A0FF" : "#808080"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                enabled: false
                onClicked: {
                    isCameraEnabled = !isCameraEnabled
                    cameraToggled(isCameraEnabled)
                }
            }

            // Microphone toggle
            ToolButton {
                icon.source: "qrc:/icons/microphone.svg"
                icon.color: isMicrophoneEnabled ? "#00A0FF" : "#808080"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                enabled: false
                onClicked: {
                    isMicrophoneEnabled = !isMicrophoneEnabled
                    microphoneToggled(isMicrophoneEnabled)
                }
            }

            // System audio toggle
            ToolButton {
                icon.source: "qrc:/icons/audio.svg"
                icon.color: isSystemAudioEnabled ? "#00A0FF" : "#808080"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                enabled: false
                onClicked: {
                    isSystemAudioEnabled = !isSystemAudioEnabled
                    systemAudioToggled(isSystemAudioEnabled)
                }
            }

            Rectangle {
                width: 1
                height: 24
                color: "#404040"
                Layout.alignment: Qt.AlignVCenter
            }

            // Settings menu
            ToolButton {
                icon.source: "qrc:/icons/timer.svg"
                icon.color: "#808080"
                icon.width: 24
                icon.height: 24
                background: Rectangle {
                    color: "transparent"
                    border.color: parent.hovered ? "#A0A0A0" : "transparent"
                    border.width: 1
                    radius: 4
                }
                enabled: !isRecording
                onClicked: settingsClicked()
            }
        }
    }
} 