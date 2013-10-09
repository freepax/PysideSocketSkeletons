#!/usr/bin/python

import time
from PySide import QtCore, QtGui, QtNetwork
from PySide import QtXml
from xmlhander import *

from Client import *
from UserDialog import *

DefaultPortNumber = int(54321)


## THE LOGIN DIALOG
class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)        

        # port label and port spin box
        portLabel = QtGui.QLabel('Portnumber')
        self.portSpin = QtGui.QSpinBox()
        self.portSpin.setRange(1000, 99999)
        self.portSpin.setValue(DefaultPortNumber)
        
        # the cancel button
        cancelButton = QtGui.QPushButton('Cancel')
        cancelButton.clicked.connect(self.cancelSlot)

        # the connect button (will have focus)
        connectButton = QtGui.QPushButton('&Connect', self)
        connectButton.clicked.connect(self.connectServer)
        connectButton.setAutoDefault(True)
        
        # the button layout - horizontal
        buttonBox = QtGui.QHBoxLayout()
        buttonBox.addWidget(cancelButton)
        buttonBox.addWidget(connectButton)

        # the main grid layout
        layout = QtGui.QGridLayout()
        layout.addWidget(portLabel,     0, 0, 1, 1)
        layout.addWidget(self.portSpin, 0, 1, 1, 1)
        layout.setRowStretch(2, 2)
        layout.addLayout(buttonBox,     3, 0, 1, 2)
        
        # set layout, geometry and window title
        self.setLayout(layout)
        self.setGeometry(320, 320, 250, 280)
        self.setWindowTitle('Login Dialog')


    # return 1 on connect
    def connectServer(self):
        self.done(1)

    # return negative on cancel
    def cancelSlot(self):
        self.done(-1)

    # provide the port number (ugh it's very acessable from parent)
    def portNumber(self):
        return self.portSpin.value()


# THE MAIN WINDOW
class MainWindow(QtGui.QMainWindow):
    client_list = []
    loginSocket = int(-1)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.login_socket = int(-1)

        # initialize the server
        self.tcpServer = QtNetwork.QTcpServer()
        self.tcpServer.newConnection.connect(self.incomingConnection)

        ## Initialize xml reader
        handler = UsernamePasswordXmlHandler()
        reader = QtXml.QXmlSimpleReader()
        reader.setContentHandler(handler)
        reader.setErrorHandler(handler)

        filename = 'userpass.xml'

        file = QtCore.QFile(filename)
        if file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            print 'reading fileName', filename
            xmlInputSource = QtXml.QXmlInputSource(file)

            ## Parse xml file
            if reader.parse(xmlInputSource) == False:
                message = str('XML parse error:')
                print 'PARSE ERROR', message

        ## Set dictionary of user names and password
        self.userNamePassword = handler.getlist()

        ## Set reader handler to 
        self.handler = ServerXmlHandler()
        self.reader = QtXml.QXmlSimpleReader()
        self.reader.setContentHandler(self.handler)
        self.reader.setErrorHandler(self.handler)
        self.xmlInputSource = QtXml.QXmlInputSource()

        # connect and exit action
        self.connectAction = QtGui.QAction('&Connect', self)
        self.connectAction.setShortcut('Ctrl+C')
        self.connectAction.triggered.connect(self.startServer)

        exitAction = QtGui.QAction('&Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.quitServer)

        # the menubar with menus and actions
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.connectAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # list of users
        userListAction = QtGui.QAction('ALL &Users', self)
        userListAction.setShortcut('Ctrl+U')
        userListAction.triggered.connect(self.showUsers)

        onlineAction = QtGui.QAction('Online &users', self)
        onlineAction.setShortcut('Ctrl+L')
        onlineAction.triggered.connect(self.loggedInUsers)

        systemMenu = menuBar.addMenu('&System')
        systemMenu.addAction(userListAction)
        systemMenu.addAction(onlineAction)

        # the text edit (the main widget)
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setEnabled(False)

        # set the text edit as central wigdet
        self.setCentralWidget(self.textEdit)

        # set geometry, window title and show the main window
        self.setGeometry(300, 300, 250, 280)
        self.setWindowTitle('Chat Server')
        self.show()


    def showUsers(self):
        #dialog = UserDialog(['espen'])
        l = []
        for i in self.userNamePassword:
            c = Client(i, self.userNamePassword[i], 0)
            l.append(c)
        dialog = UserDialog(l, 'All users')
        dialog.exec_()


    def loggedInUsers(self):
        print 'loggedInUsers'
        dialog = UserDialog(self.client_list, 'Logged in users')
        dialog.exec_()


    # handle new incoming connections
    def incomingConnection(self):
        self.login_socket = self.tcpServer.nextPendingConnection()
        self.login_socket.readyRead.connect(self.readyRead)
        self.login_socket.disconnected.connect(self.closeConnection)


    ## Start the server
    def startServer(self):
        ## run the login dialog
        loginDialog = LoginDialog()

        ## if it returns '1', try to start server
        if loginDialog.exec_() == 1:
            ## listen
            if not self.tcpServer.listen(QtNetwork.QHostAddress.Any, loginDialog.portNumber()):
                QtGui.QMessageBox.critical(self, "Chat server", " Unable to start server %s." % self.tcpServer.errorString())
                self.stopServer()
                return        

            ## If listening, update gui and reconnect stop/start
            if self.tcpServer.isListening() == True:
                self.textEdit.setEnabled(True)
                self.textEdit.setText("Server listening on port %d" % loginDialog.portNumber())
                self.connectAction.setText('&Disconnect')
                self.connectAction.setShortcut('Ctrl+D')
                self.connectAction.triggered.disconnect(self.startServer)
                self.connectAction.triggered.connect(self.stopServer)


    ## stop the server
    def stopServer(self):
        """ stopServer: close all client connections and shut down the servier
        """
        if self.tcpServer.isListening() == True:

            ## close all connected clients
            for client in self.client_list:
                if client.socket().state() == QtNetwork.QAbstractSocket.ConnectedState:
                    client.socket().disconnected.disconnect(self.closeConnection)
                    client.close()

            ## Empty client list
            self.client_list = []

            ## stop server
            self.tcpServer.close()

            ## reset the connectAction
            self.connectAction.setText('&Connect')
            self.connectAction.setShortcut('Ctrl+C')
            self.connectAction.triggered.disconnect(self.stopServer)
            self.connectAction.triggered.connect(self.startServer)

        ## reset the text edit
        self.textEdit.setEnabled(False)
        self.textEdit.clear()
        self.textEdit.setText('Server is down')


    ## open incomming login query
    def openLogin(self):
        if self.login_socket.bytesAvailable() > 0:
            message = self.login_socket.read(self.login_socket.bytesAvailable())
            self.xmlInputSource.setData(message)
            #print 'DEBUG DATA', self.xmlInputSource.data()

            ## Parse xml file
            if self.reader.parse(self.xmlInputSource) == False:
                message = str('XML parse error:' % self.handler.errorString())
                self.textEdit.append(message)
                self.closeLogin(message)
                return False
            
            if self.handler.type == 'login':
                #print 'DEBUG user', self.handler.user, ' password', self.handler.password

                ## check if user exists
                if self.userNamePassword.__contains__(str(self.handler.user)) == False:
                    self.closeLogin('user dont exists')
                    return

                ## check that password is correct
                if self.userNamePassword[self.handler.user] != self.handler.password:
                    self.closeLogin('wrong password')
                    return

                ## check if user is already connected
                for c in self.client_list:
                    if c.username() == self.handler.user:
                        self.closeLogin('user already exists')
                        return

                ## NEW CLIENT ACCEPTED
                message = str("%s logged in" % self.handler.user)
                self.textEdit.append(message)
                self.sendSystemMessage(message)

                c = Client(self.handler.user, self.userNamePassword[self.handler.user], self.login_socket)
                c.socket().disconnected.connect(self.closeConnection)
                c.socket().write(str('<chat><content user=\"server\" type=\"login\"></content><message message=\"success\"></message></chat>'))
                self.client_list.append(c)

        ## set the login socket back to negative
        self.login_socket = int(-1)


    def closeLogin(self, message):
        message = str('<chat><content user=\"server\" type=\"login\"></content><message message=\"%s\"></message></chat>' % message)
        self.login_socket.write(message)
        self.login_socket.close()
        self.login_socket = int(-1)


    # handle incoming data
    def readyRead(self):
        ## if socket is not -1, this is a new client connection
        if self.login_socket != int(-1):
            self.openLogin()
            return

        ## not login request
        for client in self.client_list:
            if client.socket().bytesAvailable() > 0:
                message = client.socket().read(client.socket().bytesAvailable())

                ## xml input source
                self.xmlInputSource.setData(message)
                #print 'DEBUG DATA', self.xmlInputSource.data()

                ## Parse xml file
                if self.reader.parse(self.xmlInputSource) == False:
                    message = str('XML pars error: %s' % self.handler.errorString())
                    self.textEdit.append(message)
                    self.sendClientErrorMessage(client.socket(), message)
                    return False

                ## check that user is exists
                if self.userNamePassword.__contains__(str(self.handler.user)) == False:
                    message =  str('SHOULD NOT HAPPEND Invalid user')
                    self.sendClientErrorMessage(client.socket(), message)
                    client.close()
                    return

                if self.handler.type == 'message':
                    ## skip empty strings
                    if self.handler.message == "" or self.handler.message == '\n' or self.handler.message == '\l\c':
                        print 'Empty string'
                        return

                    text = self.handler.message
                    text = text.replace('&', '&amp;')
                    text = text.replace('<', '&lt;')
                    text = text.replace('>', '&gt;')

                    self.sendMessage(self.handler.user, text)

                    text = str("%s: %s" % (self.handler.user, self.handler.message))
                    print text
                    self.textEdit.append(text)

                elif self.handler.type == 'request':                                  ## REQUEST
                    if self.handler.message == 'user-list':                           ## USER LIST
                        text = str('')
                        for c in self.client_list:
                            text += str('%s, ' % c.username())

                        self.sendSystemMessageToClient(client, 'user-list', text)

                    if self.handler.message == 'all-user-list':                       ## ALL USER LIST
                        text = str('')
                        for c in self.userNamePassword:
                            text += str('%s, ' % c)

                        self.sendSystemMessageToClient(client, 'all-user-list', text)

                ## handle only one client per signal
                return


    def sendClientErrorMessage(self, socket, message):
        text = str('<chat><content user=\"INTRUDER\" type=\"error\"></content><message message=\"%s\"></message></chat>' % (message))
        socket.write(text)


    def sendMessage(self, user, message):
        text = str('<chat><content user=\"%s\" type=\"message\"></content><message message=\"%s\"></message></chat>' % (user, message))
        for client in self.client_list:
            client.write(text)


    def sendSystemMessage(self, message):
        text = str('<chat><content user=\"server\" type=\"message\"></content><message message=\"%s\"></message></chat>' % (message))
        for client in self.client_list:
            client.write(text)


    def sendSystemMessageToClient(self, client, messagetype, message):
        text = str('<chat><content user=\"server\" type=\"%s\"></content><message message=\"%s\"></message></chat>' % (messagetype, message))
        client.write(text)


    # remove the client that closed the connection from the list of connected clients
    def closeConnection(self):
        message = str('')

        if self.login_socket != int(-1):
            self.login_socket = int(-1)
            return

        for client in self.client_list:
            if client.socket().state() == QtNetwork.QAbstractSocket.UnconnectedState:
                message = str('%s logged out' % client.username())
                self.client_list.remove(client)
                break

        if message != str(''):
            self.textEdit.append(message)
            self.sendSystemMessage(message)


    ## disconncted all clients, stop server and exit
    def quitServer(self):
        self.stopServer()
        exit()


### The main ###
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
