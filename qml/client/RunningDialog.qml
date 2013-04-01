import QtQuick 1.0

import "../lib"

Rectangle {
    id: background;

    color: "black"

    ChatGradients { id: cg }

    property int rowHeight: 30
    property int sendButtonWidth: 40

    Column {
        anchors.fill: parent

        Rectangle {
            height: background.height - (2 * rowHeight); width: textEdit.width //width: model.width()
            color: "black"

            Flickable {
                id: flickable

                anchors.fill: parent
                contentWidth: textEdit.width; contentHeight: textEdit.height
                flickableDirection: Flickable.VerticalFlick
                clip: true

                onContentHeightChanged: contentY = textEdit.paintedHeight - parent.height + textEdit.font.pixelSize + 10

                TextEdit {
                    id: textEdit;
                    wrapMode: TextEdit.Wrap;
                    readOnly: true; color: "steelblue"; text: model.text
                    KeyNavigation.tab: sendText.focusItem
                }
            }
        }

        Row {
            id: row
            height: rowHeight; width: model.width(); spacing: 2

            /// Input text
            LineEdit {
                id: sendText
                focus: true
                Component.onCompleted: { textColor = "red"; clearTextOnAccepted = true; set_focus() }
                width: background.width - sendButtonWidth - row.spacing; height: rowHeight - row.spacing
                onSendMessage: model.sendMessageSignal(message)
                KeyNavigation.tab: sendButton.focusItem

            }

            /// The send button
            PushButton {
                id: sendButton
                text: "Send"; textColor: "white";
                height: rowHeight - row.spacing; width: sendButtonWidth - row.spacing;
                autoGradient: false; gradient: cg.off
                onDown: gradient = cg.onn
                onUp:  gradient = cg.off
                KeyNavigation.tab: disconnectButton.focusItem
                onTrigger: { model.sendMessageSignal(sendText.inputText); sendText.inputText = "" }
            }

            //Component.onCompleted: { sendText.forceActiveFocus(); sendText.focus = true }
        }

        PushButton {
            id: disconnectButton
            text: "Disconnect"; textColor: "white"
            height: rowHeight; width: background.width;
            autoGradient: false; gradient: cg.off
            onDown: gradient = cg.onn
            onUp:  gradient = cg.off
            KeyNavigation.tab: sendText.focusItem
            onTrigger: model.disconnectSignal();
        }
    }
}

//Rectangle {
//    id: inputRectangle
//    border.color: "red"; border.width: 1
//    height: rowHeight;
//    width: background.width - sendButtonWidth;
//    radius: 4; color: "steelblue"

//    TextInput {
//        id: textInput; color: "red"
//        horizontalAlignment: TextInput.AlignLeft
        //height: parent.height - 2;
        //width: parent.width - 10
        //anchors.centerIn: parent
//        anchors.fill: parent
        //anchors.top: inputRectangle.top; anchors.bottom: inputRectangle.bottom
        //anchors.left: inputRectangle.left; anchors.right: inputRectangle.right
//        text: "Hi"
//        onAccepted: { model.sendMessageSignal(text) }
//    }
//}
