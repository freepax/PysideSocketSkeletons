from PySide import QtCore, QtGui


class UserDialog(QtGui.QDialog):
    def __init__(self, cl, text, parent=None):
        super(UserDialog, self).__init__(parent)

        textLabel = QtGui.QLabel(str('<b>%s</b>' % text))
        mainbox = QtGui.QVBoxLayout()
        mainbox.addWidget(textLabel)

        vbox = QtGui.QVBoxLayout()
        entry = 1

        for client in cl:
            userLabel = QtGui.QLabel(str('%d. <b>%s</b>' % (entry, client.username())))
            vbox.addWidget(userLabel)
            entry += 1


        widget = QtGui.QWidget()
        widget.setLayout(vbox)

        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidget(widget)
        mainbox.addWidget(scrollArea)

        closeButton = QtGui.QPushButton('&Close')
        closeButton.clicked.connect(self.closeDialog)
        mainbox.addWidget(closeButton)

        self.setLayout(mainbox)
        self.resize(270, 400)

        self.setWindowTitle(text)

    def closeDialog(self):
        self.done(0)
