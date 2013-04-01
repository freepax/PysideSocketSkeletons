import QtQuick 1.0

/// Need the LineEdit and PushButton
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
            height: background.height - (2 * rowHeight); width: textEdit.width
            color: "black"

            Flickable {
                id: flickable

                anchors.fill: parent
                contentWidth: textEdit.width; contentHeight: textEdit.height
                flickableDirection: Flickable.VerticalFlick
                clip: true

                /// set contentY correct when the text edit is updated with new stuff
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
                KeyNavigation.tab: sendButton.focusItem
                onSendMessage: model.sendMessageSignal(message)
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
