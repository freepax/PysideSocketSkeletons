import QtQuick 1.0


Rectangle {
    id: textLine

    property string text: "textLine"
    property color textColor: "purple"
    property color borderColor: "yellow"
    property int borderWidth: 2

    border.color: textLine.borderColor; border.width: textLine.borderWidth
    radius: 8; gradient: textLineGradient
    height: 50; width: 50;

    Gradient {
        id: textLineGradient
        GradientStop { position: 0.0; color: "#123456"}
        GradientStop { position: 0.5; color: "#456789"}
        GradientStop { position: 1.0; color: "#6789ab"}
    }

    Text { text: textLine.text; color: textLine.textColor; anchors.centerIn: parent }
}
