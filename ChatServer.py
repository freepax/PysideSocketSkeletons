#!/usr/bin/env python

import time
from PySide import QtCore, QtGui, QtNetwork


DefaultPortNumber = int(54321)


class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)        
        self.__initUI()
        
    def __initUI(self):
        # port label and port spin box
        portLabel = QtGui.QLabel('Portnumber')
        self.__portSpin = QtGui.QSpinBox()
        self.__portSpin.setRange(1000, 99999)
        self.__portSpin.setValue(DefaultPortNumber)
        
        # the cancel button
        cancelButton = QtGui.QPushButton('Cancel')
        cancelButton.clicked.connect(self.__cancelSlot)

        # the connect button (will have focus)
        connectButton = QtGui.QPushButton('&Connect', self)
        connectButton.clicked.connect(self.__connectSlot)
        connectButton.setAutoDefault(True)
        
        # the button layout - horizontal
        buttonBox = QtGui.QHBoxLayout()
        buttonBox.addWidget(cancelButton)
        buttonBox.addWidget(connectButton)

        # the main grid layout
        layout = QtGui.QGridLayout()
        layout.addWidget(portLabel,       0, 0, 1, 1)
        layout.addWidget(self.__portSpin, 0, 1, 1, 1)
        layout.setRowStretch(2, 2)
        layout.addLayout(buttonBox,       3, 0, 1, 2)
        
        # set layout, geometry and window title
        self.setLayout(layout)
        self.setGeometry(320, 320, 250, 280)
        self.setWindowTitle('Login Dialog')


    # return 1 on connect
    def __connectSlot(self):
        self.done(1)

    # return negative on cancel
    def __cancelSlot(self):
        self.done(-1)

    # provide the port number (ugh it's very acessable from parent)
    def portNumber(self):
        return self.__portSpin.value()


# the main window
class MainWindow(QtGui.QMainWindow):
    __portNumber = int(0)
    __clientList = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # initialize the server
        self.__tcpServer = QtNetwork.QTcpServer()
        self.__tcpServer.newConnection.connect(self.__incomingConnection)

        # setup the UI
        self.__initUI()
        
    def __initUI(self):
        # connect and exit action
        self.__connectAction = QtGui.QAction('&Connect', self)
        self.__connectAction.setShortcut('Ctrl+C')
        self.__connectAction.triggered.connect(self.__start)

        exitAction = QtGui.QAction('&Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.__quitSlot)

        # the menubar with menus and actions
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.__connectAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # the text edit (the main widget)
        self.__textEdit = QtGui.QTextEdit()
        self.__textEdit.setReadOnly(True)
        self.__textEdit.setEnabled(False)

        # set the text edit as central wigdet
        self.setCentralWidget(self.__textEdit)

        # set geometry, window title and show the main window
        self.setGeometry(300, 300, 250, 280)
        self.setWindowTitle('Chat Server')
        self.show()


    # handle new incoming connections
    def __incomingConnection(self):
        tcpClient = self.__tcpServer.nextPendingConnection()
        tcpClient.readyRead.connect(self.__readyRead)
        tcpClient.disconnected.connect(self.__closeConnection)
        tcpClient.write(str("welcome"))

        self.__clientList.append(tcpClient)
        self.__textEdit.append(str("Adding client %d" % len(self.__clientList)))


    # Start the server
    def __start(self):
        # run the login dialog
        loginDialog = LoginDialog()

        # if it returns '1', try to start server
        if loginDialog.exec_() == 1:
            print "Setting up server"
            self.__portNumber = loginDialog.portNumber()

            # listen
            if not self.__tcpServer.listen(QtNetwork.QHostAddress.Any, self.__portNumber):
                QtGui.QMessageBox.critical(self, "Chat server", " Unable to start server %s." % self.__tcpServer.errorString())
                self.__stop()
                return        

            if self.__tcpServer.isListening() == True:
                self.__textEdit.setEnabled(True)
                self.__textEdit.setText("Server listening on port %d" % self.__portNumber)
                self.__connectAction.setText('&Disconnect')
                self.__connectAction.setShortcut('Ctrl+D')
                self.__connectAction.triggered.disconnect(self.__start)
                self.__connectAction.triggered.connect(self.__stop)

    # call this slot to stop the server
    def __stop(self):
        if self.__tcpServer.isListening() == True:
            # close all connected clients
            for l in self.__clientList:
                if l.state() == QtNetwork.QAbstractSocket.ConnectedState:
                    l.close()

            # stop server
            self.__tcpServer.close()

            #  reset the connectAction
            self.__connectAction.setText('&Connect')
            self.__connectAction.setShortcut('Ctrl+C')
            self.__connectAction.triggered.disconnect(self.__stop)
            self.__connectAction.triggered.connect(self.__start)

        # reset the text edit
        self.__textEdit.setEnabled(False)
        self.__textEdit.clear()
        self.__textEdit.setText('Server is down')

    # handle incoming data
    def __readyRead(self):
        client = 1
        bytesAvaliable = 0

        for l in self.__clientList:
            bytesAvaliable = l.bytesAvailable()

            if bytesAvaliable > 0:
                message = l.read(bytesAvaliable)

                # skip empty strings
                if message == "" or message == '\n' or message == '\l\c':
                    return

                # handle only one client per signal
                break

            client += 1

        # format string to send
        text = str("Client %d say: %s" % (client, message))
        print text

        self.__textEdit.append(text)

        # write text to all connected clients
        for l in self.__clientList:
            l.write(text)


    # remove the client that closed the connection from the list of connected clients
    def __closeConnection(self):
        count = 0
        for l in self.__clientList:
            if l.state() == QtNetwork.QAbstractSocket.UnconnectedState:
                self.__textEdit.append(str("Client %d disconnected" % count))
                self.__clientList.pop(count)
                break
            count += 1

        for l in self.__clientList:
            l.write(str("Client %d disconnected" % count))


    # disconncted all clients, stop server and exit
    def __quitSlot(self):
        self.__stop()
        exit()


### The main ###
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
