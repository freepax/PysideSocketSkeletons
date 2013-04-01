import QtQuick 1.0

Rectangle {
    id: lineEdit

    /// default size and cosmetics
    height: 40; width: 100; radius: 4; gradient: lineGradient
    border.color: "red"; border.width: 1

    /// property aliases - the TextInput's text and text color
    property alias textColor: textInput.color
    property alias inputText: textInput.text

    property alias focusItem: textInput

    /// The clear text on accepted property
    property bool clearTextOnAccepted: false

    /// send messsage on TextInput's onAccepted signal
    signal sendMessage (string message)

    function set_focus() {
        textInput.forceActiveFocus()
        textInput.focus = true
    }

    onSendMessage: {
        /// clear text area after message signal with string is sent
        if (clearTextOnAccepted == true)
            textInput.text = ""
    }

    Gradient {
        id: lineGradient
        GradientStop { position: 0.0; color: "#123456"}
        GradientStop { position: 0.5; color: "#456789"}
        GradientStop { position: 1.0; color: "#6789ab"}
    }

    Component.onCompleted: {
        textInput.color = "black"
        textInput.text = ""
    }

    TextInput {
        id: textInput
        horizontalAlignment: TextInput.AlignLeft
        height: parent.height - 2; width: parent.width - 10
        anchors.centerIn: parent
        onAccepted: { lineEdit.sendMessage(text) }
    }
}
