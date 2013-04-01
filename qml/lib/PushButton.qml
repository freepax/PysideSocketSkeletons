import QtQuick 1.0


Rectangle {
    id: button
    radius: 8; height: 50; width: 100; gradient: buttonIdleGradien
    border.color: "yellow"; border.width: 2

    signal trigger
    signal down
    signal up
    signal keyPressed (int key)

    property alias text: buttonText.text
    property alias textColor: buttonText.color
    property alias focusItem: button

    property bool autoGradient: true

    Keys.onPressed: {
        if (event.key == Qt.Key_Return) {
            button.trigger()
            button.keyPressed(event.key)
            event.accepted = true;
        }
        else {
            button.keyPressed(event.key)
        }
    }

    Gradient {
        id: buttonIdleGradien
        GradientStop { position: 0.0; color: "#aaffff"} GradientStop { position: 0.5; color: "#aaaaaa"} GradientStop { position: 1.0; color: "#aa1111"}
    }

    Gradient {
        id: buttonPressedGradient
        GradientStop { position: 0.0; color: "#aa1111"} GradientStop { position: 0.5; color: "#aaaaaa"} GradientStop { position: 1.0; color: "#aaffff"}
    }

    Gradient {
        id: buttonHoverGradient
        GradientStop { position: 0.0; color: "#aa1111"} GradientStop { position: 0.5; color: "#aaaaaa"} GradientStop { position: 1.0; color: "#aaffff"}
    }

    Text { id: buttonText; text: button.text; anchors.centerIn: parent }

    MouseArea {
        id: mouseArea
        anchors.fill: parent;

        /// When mouse button is pressed down
        onPressed: {
            if (autoGradient == true)
                button.gradient = buttonPressedGradient
            button.down()
        }

        /// When mouse button is released
        onReleased: {
            if (autoGradient == true)
                button.gradient = buttonIdleGradien
            button.up()
        }

        /// The 'click' behavior
        onClicked: button.trigger()
    }
}
