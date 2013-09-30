#!/usr/bin/env python

from PySide.QtCore import QUrl
from PySide.QtGui import QPushButton, QApplication
from PySide.QtDeclarative import QDeclarativeView

from PySide import QtGui, QtCore, QtNetwork

from xmlhander import *

#SendMessageFormatedString = str("<chat><content type=\"%s\" message=\"%s\" /></char>")

class UsernamePasswordModel(QtCore.QObject):
    __host = ""
    __port = ""

    def __init__(self, parent = None):
        super(UsernamePasswordModel, self).__init__(parent)

    connectSignal = QtCore.Signal(str, str)
    cancelSignal = QtCore.Signal()

    def setHost(self, host):
        self.__host = host

    def setPort(self, port):
        self.__port = port

    @QtCore.Slot(result=str)
    def hostName(self):
        return str(self.__host)

    @QtCore.Slot(result=str)
    def portNumber(self):
        return str(self.__port)



class LoggedInModel(QtCore.QObject):
    __width = int(200)
    __height = int(200)
    __text = str("")
    __lastMessage = str("")
    __sendMessage = str("")

    disconnectSignal = QtCore.Signal()

    def __init__(self, parent = None):
        super(LoggedInModel, self).__init__(parent)

    @QtCore.Slot(result=str)
    def getText(self):
        #print "getText", self.__text
        return self.__text

    def setText(self, t):
        #if t != self.__lastMessage and t != "":
        if t != "":
            self.__text = str(("%s\n%s") % (self.__text, t))
            self.__lastMessage = t

    onTextChanged = QtCore.Signal(str)
    text = QtCore.Property(str, getText, setText, notify=onTextChanged)

    def getMessage(self):
        print "getMessage", self.__message
        return self.__sendMessage

    def setMessage(self, t):
        print "setMessage", t
        if t != "":
            self.__sendMessage = t

    sendMessageSignal = QtCore.Signal(str)
    sendMessage = QtCore.Property(str, getMessage, setMessage, notify=sendMessageSignal)

    def clear(self):
        self.__text = str("")
        self.__lastMessage = str("")

    def setHeight(self, h):
        self.__hight = int(h)

    def setWidth(self, w):
        self.__width = int(w)

    @QtCore.Slot(result=int)
    def width(self):
        return self.__width

    @QtCore.Slot(result=int)
    def height(self):
        return self.__height



class Application(QtGui.QDialog):
    __height = int(250)
    __width = int(200)

    __hostname = str('localhost')
    __portnumber = int(54321)

    ## the client socket
    __socket = QtNetwork.QTcpSocket()

    __seconds = int(0)

    __messages = int(0)

    __user = str("espen")

    def __init__(self, parent = None):
        super(Application, self).__init__(parent)

        self.handler = DocumentXmlHandler()

        ## Set values for the store/restore settings system
        QtCore.QCoreApplication.setOrganizationName("EMR")
        QtCore.QCoreApplication.setOrganizationDomain("code.rutger.no")
        QtCore.QCoreApplication.setApplicationName("QmlChatClient")

        ## create settings
        self.__settings = QtCore.QSettings()
        hostname = self.__settings.value("QmlChatClient/hostname")
        if hostname != None:
            self.__hostname = hostname
        portnumber = self.__settings.value("QmlChatClient/portnumber")
        if portnumber != None:
            self.__portnumber = portnumber

        ## Connect the socket's signals to our slots
        self.__socket.connected.connect(self.__socketConnected)
        self.__socket.disconnected.connect(self.__socketDisconnected)
        self.__socket.error.connect(self.__socketError)
        self.__socket.readyRead.connect(self.__readyRead)
        #self.__socket.stateChanged.connect(self.__socketStateChanged)

        userpassModel = UsernamePasswordModel()
        userpassModel.setHost(self.__hostname)
        userpassModel.setPort(int(self.__portnumber))

        userpassModel.connectSignal.connect(self.__connectToSystem)
        userpassModel.cancelSignal.connect(self.quitSlot)

        self.loginView = QDeclarativeView()
        self.loginView.rootContext().setContextProperty("model", userpassModel)
        self.loginView.setSource(QUrl('qml/client/LoginDialog.qml'))
        self.loginView.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        self.loggedInModel = LoggedInModel()
        self.loggedInModel.disconnectSignal.connect(self.__disconnectFromHost)
        self.loggedInModel.setHeight(self.__height)
        self.loggedInModel.setWidth(self.__width)
        self.loggedInModel.sendMessageSignal.connect(self.__sendMessage)


        self.loggedInView = QDeclarativeView()
        self.loggedInView.rootContext().setContextProperty("model", self.loggedInModel)
        self.loggedInView.setSource(QUrl('qml/client/RunningDialog.qml'))
        self.loggedInView.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        self.stackedWidget = QtGui.QStackedWidget()
        self.stackedWidget.addWidget(self.loginView)
        self.stackedWidget.addWidget(self.loggedInView)
        self.stackedWidget.setCurrentWidget(self.loginView)

        self.stackedWidget.setWindowTitle('Qml Chat Client')
        self.stackedWidget.setGeometry(300, 300, self.__width, self.__height)
        self.stackedWidget.show()


    def __connectToSystem(self, hostname, portnumber):
        self.__hostname = hostname
        self.__portnumber = portnumber
        #print "ConnectToSystem hostname", self.__hostname, "portnumber", self.__portnumber

       	## Try to connect to the server
        try:
            self.__socket.connectToHost(self.__hostname, int(self.__portnumber))
        except:
            text = 'Failed to connect to %s on port %d' % (self.__hostname, int(self.__portnumber))
            print text
            
            ## remove file created above
            #os.unlink(self.__loginWidget.logfileName())

    def quitSlot(self):
        print "quitSlot"
        exit()


    def __socketConnected(self):
        ## successfully logged in, write hostname and port number to settings
        self.__settings.setValue("ChatClient/hostname", self.__hostname)
        self.__settings.setValue("ChatClient/portnumber", self.__portnumber)

       	## Reset seconds and messages
        self.__seconds = 0
        self.__messages = 0

        ## Start timer that displays seconds and number of messages
        #self.__timer.start(1000)

        self.stackedWidget.setCurrentWidget(self.loggedInView)


    def __disconnectFromHost(self):
        ## Disconnect from server
        self.__socket.disconnectFromHost()


    def __socketDisconnected(self):
        ## we,re disconnected, stop the timer
        #self.__timer.stop()

       	## Create new file name - it will be displayed when current widget beocmes loginWidget in the next statement
        #self.__loginWidget.createFilename()

        ## Set login widget as current widget
        self.stackedWidget.setCurrentWidget(self.loginView)

        ## Clear dialog text
        self.loggedInModel.clear()


    ## Send the message
    def __sendMessage(self, text):
        print "sendMessage", text
        message = str('<chat><content user=\"%s\" type=\"message\"></content><message message=\"%s\"></message></chat>' % (self.__user, text))
        self.__socket.write(message)


    ## Data is ready for reading
    def __readyRead(self):
        ## Read the size of data available, return if no data
        size = self.__socket.bytesAvailable()
        if size == 0:
            return

       	## Read data
        data = str(self.__socket.read(size))

        ## Initialize xml reader
        reader = QtXml.QXmlSimpleReader()
        reader.setContentHandler(self.handler)
        reader.setErrorHandler(self.handler)

        ## xml input source
        xmlInputSource = QtXml.QXmlInputSource()
        xmlInputSource.setData(data)

        print 'DEBUG DATA', xmlInputSource.data()

        ## Parse xml file
        if reader.parse(xmlInputSource) == False:
            print "Pars xml error:", self.handler.errorString()
            return False

        ## skip empty strings
        if self.handler.message == "" or self.handler.message == '\n' or self.handler.message == '\l\c':
            print 'Empty string'
            return

        if self.handler.user == self.__user:
            data = str("%s: %s" % ("me", self.handler.message))
        else:
            data = str("%s: %s" % (self.handler.user, self.handler.message))

        #print "__readyRead:", data
        self.loggedInModel.setText(str(data))
        self.loggedInModel.onTextChanged.emit(str(data))

       	## Emit the write message signal
        #self.__writeMessageSignal.emit(data)

       	## Count the message
        self.__messages += 1



    ## The state of the socket has changed
    def __socketStateChanged(self, state):
       	print "MainWidget::socketStateChanged state", str(state)


    ## Manage socket errors
    def __socketError(self, error):
        QtGui.QMessageBox.critical(self, "Chat Client", "Socket Error: %s" % self.__socket.errorString())
        return


if __name__ == '__main__':
    app = QApplication([])
    application = Application()
    app.exec_()
