cmake_minimum_required(VERSION 3.16)
project(CaptureStudio VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Quick)

qt_standard_project_setup()

qt_add_executable(CaptureStudio
    src/main.py
    src/resources.qrc
)

qt_add_qml_module(CaptureStudio
    URI CaptureStudio
    VERSION 1.0
    QML_FILES
        src/qml/main.qml
        src/qml/components/AreaSelector.qml
        src/qml/components/FloatingToolbar.qml
    RESOURCES
        src/icons/display.svg
        src/icons/window.svg
        src/icons/area.svg
        src/icons/device.svg
        src/icons/camera.svg
        src/icons/microphone.svg
        src/icons/audio.svg
        src/icons/timer.svg
)

target_link_libraries(CaptureStudio
    PRIVATE Qt6::Core Qt6::Quick
) 