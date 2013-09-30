import QtQuick 1.0

/// Need the TextLabel, LineEdit and PushButton
import "../lib"


Rectangle {
    id: window
    height: 200; width: 200
    color: "black"

    ChatGradients { id: cg }

    /// Emit the model.connectSignal with host name and port number
    function connect_to_server() {
        model.connectSignal(hostEdit.inputText, portEdit.inputText)
    }

    /// Grid element with
    function gridElementWidth() {
        return (grid.width / grid.columns) - grid.spacing
    }

    /// Grid element height
    function gridElementHeight() {
        return 35
    }

    Grid {
        id: grid
        columns: 2; rows: 8; spacing: 2
        anchors.fill: parent

        /// User name text label
        TextLabel { height: gridElementHeight(); width: gridElementWidth(); text: "User"; textColor: "yellow"; borderColor: "white"; borderWidth: 2 }

        /// Port number line edit
        LineEdit {
            id: userEdit
            Component.onCompleted: { textColor = "black"; inputText = model.userName(); set_focus() }
            width: gridElementWidth(); height: gridElementHeight(); radius: 8
            border.color: "green"; border.width: 2
            KeyNavigation.tab: portEdit.focusItem
            onSendMessage: connect_to_server()
        }

        /// Password text label
        TextLabel { height: gridElementHeight(); width: gridElementWidth(); text: "Password"; textColor: "yellow"; borderColor: "white"; borderWidth: 2 }

        /// Password line edit
        LineEdit {
            id: passwordEdit
            Component.onCompleted: { textColor = "black"; inputText = model.passWord(); set_focus() }
            width: gridElementWidth(); height: gridElementHeight(); radius: 8
            border.color: "green"; border.width: 2
            KeyNavigation.tab: portEdit.focusItem
            onSendMessage: connect_to_server()
        }

        /// Hostname text label
        TextLabel { height: gridElementHeight(); width: gridElementWidth(); text: "Host"; textColor: "yellow"; borderColor: "white"; borderWidth: 2 }

        /// Hostname line edit
        LineEdit {
            id: hostEdit
            Component.onCompleted: { textColor = "black"; inputText = model.hostName(); set_focus() }
            width: gridElementWidth(); height: gridElementHeight(); radius: 8
            border.color: "green"; border.width: 2
            KeyNavigation.tab: portEdit.focusItem
            onSendMessage: connect_to_server()
        }

        /// Port number text label
        TextLabel { height: gridElementHeight(); width: gridElementWidth(); text: "Port"; textColor: "white"; borderColor: "purple"; borderWidth: 2 }

        /// Port number line edit
        LineEdit {
            id: portEdit
            Component.onCompleted: { textColor = "black"; inputText = model.portNumber(); set_focus() }
            width: gridElementWidth(); height: gridElementHeight(); radius: 8
            border.color: "green"; border.width: 2
            KeyNavigation.tab: connectButton.focusItem
            onSendMessage: connect_to_server()
        }

        /// Spacers (one column)
        //Rectangle { color: "black"; height: grid.height - (3 * gridElementHeight()) - (grid.spacing * grid.rows); width: (grid.width / grid.columns) }
        //Rectangle { color: "black"; height: grid.height - (gridElementHeight()) - (grid.spacing * grid.rows); width: (grid.width / grid.columns) }

        /// Quit button
        PushButton {
            id: quitButton
            text: "Quit"; textColor: "white"
            height: gridElementHeight(); width: gridElementWidth();
            autoGradient: false; gradient: cg.off
            onDown: gradient = cg.onn
            onUp:  gradient = cg.off
            KeyNavigation.tab: hostEdit.focusItem
            onTrigger: model.cancelSignal()
        }

        /// Connect button
        PushButton {
            id: connectButton
            text: "Connect"; textColor: "white"
            height: gridElementHeight(); width: gridElementWidth();
            autoGradient: false; gradient: cg.rad
            onDown: gradient = cg.onn
            onUp:  gradient = cg.rad
            KeyNavigation.tab: quitButton.focusItem
            onTrigger: connect_to_server()
            //onKeyPressed: console.log("Connect button hit", key)
        }
    }
}
