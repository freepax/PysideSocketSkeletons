#!/usr/bin/env python

# Import stuff
import os
from PySide import QtGui, QtCore, QtNetwork


## Defaults
DefaultHost = "localhost"
DefaultPort = 54321


## The login widget
class LoginWidget(QtGui.QWidget):
	## Public signal
	openConnection = QtCore.Signal()

	def __init__(self, parent = None):
		super(LoginWidget, self).__init__(parent)

		##  Setup the GUI
		self.__initUI()

	def __initUI(self):
		## Host name label and line edit
		hostLabel = QtGui.QLabel('IP address:', self)
		self.__hostEdit = QtGui.QLineEdit(self)
		self.__hostEdit.setText(DefaultHost)

		## Portnumber label and spin box
		portLabel = QtGui.QLabel('Port number:', self)
		self.__portSpin = QtGui.QSpinBox(self)
		self.__portSpin.setRange(1000, 99999)
		self.__portSpin.setValue(DefaultPort)

		## The file label and the file edit with the log file name
		fileLabel = QtGui.QLabel('Filename')
		self.__fileEdit = QtGui.QLineEdit(self)
		self.createFilename()

		## The group box for the file edit
		self.__fileGroup = QtGui.QGroupBox('&Record file')
		self.__fileGroup.setCheckable(True)
		self.__fileGroup.setChecked(False)

		## The widgets for the group box must be in a layout
		groupBox = QtGui.QHBoxLayout()
		groupBox.addWidget(fileLabel)
		groupBox.addWidget(self.__fileEdit)

		## Set the groupBox layout as the groupBox layout
		self.__fileGroup.setLayout(groupBox)

		## Connect button - connected to the __connectHost function (slot)
		connectButton = QtGui.QPushButton('&Connect', self)
		connectButton.clicked.connect(self.__connectHost)
		
		## Quit button - connected to quit
		quitButton = QtGui.QPushButton('&Quit', self)
		quitButton.clicked.connect(quit)

		## Place the quit and connect button in a horizontal layout
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(quitButton)
		hbox.addWidget(connectButton)

		## The layout
		grid = QtGui.QGridLayout()
		grid.addWidget(hostLabel,         0, 0, 1, 1)
		grid.addWidget(self.__hostEdit,   0, 1, 1, 1)
		grid.addWidget(portLabel,         1, 0, 1, 1)
		grid.addWidget(self.__portSpin,   1, 1, 1, 1)
		grid.addWidget (self.__fileGroup, 2, 0, 1, 2)
		grid.setRowStretch(3, 2)
		grid.addLayout(hbox,              5, 0, 1, 2)

		## Set grid as layout
		self.setLayout(grid)

		## Set window title
		self.setWindowTitle('Recorder')


	## Emit the connect signal
	def __connectHost(self):
		## Emit the openConnection signal
		self.openConnection.emit()


	## Set host name on line edit
	def setHostName(self, host):
		self.__hostEdit.setText(host)


	## Set port number on spin box
	def setPortNumber(self, port):
		self.__portSpin.setValue(port)


	## Provide the host name
	def hostName(self):
		return self.__hostEdit.text()


	## Provide the port number
	def portNumber(self):
		return self.__portSpin.value()


	## Provide the logfile name
	def logfileName(self):
		return self.__fileEdit.text()


	## Log to file if fileGroupe is checked
	def logToFile(self):
		return self.__fileGroup.isChecked()


	## create a new filename for the log file
	def createFilename(self):
		## Create a filename based on the date and time
		import DateTimeFileName
		tdfn = DateTimeFileName.DateTimeFileName()
		self.__fileEdit.setText(tdfn.fileName())


## The connected widget
class ConnectedWidget(QtGui.QWidget):
	## Public signals
	closeConnection = QtCore.Signal()
	sendMessage = QtCore.Signal(str)

	def __init__(self, parent = None):
		super(ConnectedWidget, self).__init__(parent)

		self.__initUI()


	def __initUI(self):
		## Create the text edit - this is where all chat messages will go
		self.__textEdit = QtGui.QTextEdit()
		self.__textEdit.setReadOnly(True)

		## Create the chat line edit and connect the returnPressed signal
		self.__lineEdit = QtGui.QLineEdit(self)
		self.__lineEdit.returnPressed.connect(self.__sendSlot)

		## Create the send button and connect the clicked signal
		sendButton = QtGui.QPushButton('&Send')
		sendButton.clicked.connect(self.__sendSlot)

		## Layout for the send edit and send button
		buttonBox = QtGui.QHBoxLayout()
		buttonBox.addWidget(self.__lineEdit)
		buttonBox.addWidget(sendButton)

		## The disconnect button - connected to the disconnect function (slot)
		disconnectButton = QtGui.QPushButton('&Disconnect', self)
		disconnectButton.clicked.connect(self.__disconnect)

		## The grid layout
		grid = QtGui.QGridLayout(self)
		grid.addWidget(self.__textEdit,  0, 0, 2, 4)
		grid.setRowStretch(1, 2)
		grid.addLayout(buttonBox,        3, 0, 1, 4)
		grid.addWidget(disconnectButton, 4, 0, 1, 1)

		## Set grid as layout
		self.setLayout(grid)

		## Show widget
		self.show()

	## Send message
	def __sendSlot(self):
		## Check that the string is not empty
		if self.__lineEdit.text() == "" or self.__lineEdit.text() == '\n':
			return

		## Emit the send message signal
		self.sendMessage.emit(self.__lineEdit.text())

		## Clear the line edit
		self.__lineEdit.clear()


	## Disconnect
	def __disconnect(self):
		## Emit the closeConnection signal
		self.closeConnection.emit()


	## Clear the text edit
	def clearTextEdit(self):
		self.__textEdit.clear()


	## Append text to the text edit
	def appendTextEdit(self, text):
		if text != "" or text != '\n':
			self.__textEdit.append(text)


## The main window
class MainWidget(QtGui.QMainWindow):
	## Internal write message (logfile) signal
	__writeMessageSignal = QtCore.Signal(str)

	## messages count the totlal number of messages
	__messages = 0

	## Seconds connected
	__seconds = 0

	## the client socket
	__socket = QtNetwork.QTcpSocket()

	def __init__(self):
		super(MainWidget, self).__init__()

		## Set values for the store/restore settings system
		QtCore.QCoreApplication.setOrganizationName("EMRutger")
		QtCore.QCoreApplication.setOrganizationDomain("rutger.no")
		QtCore.QCoreApplication.setApplicationName("ChatClient")

		## create settings
		self.__settings = QtCore.QSettings()

		self.__initUI()

	def __initUI(self):
		## Create the connect action
		self.__connectAction = QtGui.QAction('&Connect', self)
		self.__connectAction.setShortcut('Ctrl+C')
		self.__connectAction.triggered.connect(self.__connectToSystem)

		## Create he quit action
		quitAction = QtGui.QAction('&Quit', self)
		quitAction.setShortcut('Ctrl+Q')
		quitAction.triggered.connect(self.__quitSlot)

		## create the menu bar, the file menu and add the actions
		menuBar = self.menuBar()
		fileMenu = menuBar.addMenu('&File')
		fileMenu.addAction(self.__connectAction)
		fileMenu.addSeparator()
		fileMenu.addAction(quitAction)

		## Connect the socket's signals to our slots
		self.__socket.connected.connect(self.__socketConnected)
		self.__socket.disconnected.connect(self.__socketDisconnected)
		self.__socket.error.connect(self.__socketError)
		self.__socket.readyRead.connect(self.__readyRead)
		self.__socket.stateChanged.connect(self.__socketStateChanged)

		## create the login widget - connect it to the connectToSystem slot
		self.__loginWidget = LoginWidget(self)
		self.__loginWidget.openConnection.connect(self.__connectAction.triggered)

		## read host name from settings
		hostName = self.__settings.value("chatClient/hostname")
		if hostName != None:
			self.__loginWidget.setHostName(str(hostName))

		## read port number from settings
		portNumber = self.__settings.value("chatClient/portnumber")
		if portNumber != None:
			self.__loginWidget.setPortNumber(int(portNumber))
			
		## create the connected widget - connect it to the disconnectFromHost slot
		self.__connectedWidget = ConnectedWidget(self)
		self.__connectedWidget.closeConnection.connect(self.__connectAction.triggered)
		self.__connectedWidget.sendMessage.connect(self.__sendMessage)

		## create the stacked widget and populate it with the login and disconnect widgets
		self.__stackedWidget = QtGui.QStackedWidget(self)
		self.__stackedWidget.addWidget(self.__loginWidget)
		self.__stackedWidget.addWidget(self.__connectedWidget)

		## set the login widget as current wigdet
		self.__stackedWidget.setCurrentWidget(self.__loginWidget)

		## the timer - updates the status bar with connections status (secs and messages)
		self.__timer = QtCore.QTimer()
		self.__timer.timeout.connect(self.__timeout)

		## Connect the write message signal
		self.__writeMessageSignal.connect(self.__writeMessage)

		## display 'Disconnected' on the status bar
		self.statusBar().showMessage('Disconnected')

		## set the stacked widget as central widget
		self.setCentralWidget(self.__stackedWidget)

		## move the app (to 300, 300) and resize (to 280, 400)
		self.setGeometry(300, 300, 280, 400)

		## set window title and show
		self.setWindowTitle('Chat Client')
		self.show()

	def __quitSlot(self):
		## close connection if connected
		if self.__socket:
			self.__socket.disconnectFromHost()

		## exit the application
		exit()

	def __connectToSystem(self):
		## Try to open log file
		if self.__loginWidget.logToFile():
			try:
				self.file = open(self.__loginWidget.logfileName(), 'w')
			except:
				self.statusBar().showMessage('Failed to open file')
				return

			## The logfile is sucessfully opened
			self.statusBar().showMessage('Opened file successfully')
		
		## Try to connect to the server
		try:
			self.__socket.connectToHost(self.__loginWidget.hostName(), self.__loginWidget.portNumber())
		except:
			text = 'Failed to connect to %s on port %d' % (self.__loginWidget.hostName(), self.__loginWidget.portNumber())
			self.statusBar().showMessage(text)

			## remove file created above
			os.unlink(self.__loginWidget.logfileName())


	def __socketConnected(self):
		## successfully logged in, write hostname and port number to settings
		self.__settings.setValue("chatClient/hostname", self.__loginWidget.hostName())
		self.__settings.setValue("chatClient/portnumber", self.__loginWidget.portNumber())

		## The connect action: disconnect it from connetToSystem, change text and connect it to disconnectFromHost
		self.__connectAction.triggered.disconnect(self.__connectToSystem)
		self.__connectAction.setText('Dis&connect')
		self.__connectAction.triggered.connect(self.__disconnectFromHost)

		## Reset seconds and messages
		self.__seconds = 0
		self.__messages = 0

		## Start timer that displays seconds and number of messages
		self.__timer.start(1000)

		## Set connected widget as current widget
		self.__stackedWidget.setCurrentWidget(self.__connectedWidget)


	def __disconnectFromHost(self):
		## Disconnect from server
		self.__socket.disconnectFromHost()


	def __socketDisconnected(self):
		## we,re disconnected, stop the timer
		self.__timer.stop()

		## Create new file name - it will be displayed when current widget beocmes loginWidget in the next statement
		self.__loginWidget.createFilename()

		## Set login widget as current widget
		self.__stackedWidget.setCurrentWidget(self.__loginWidget)

		## Clear the text edit (make it ready for next session)
		self.__connectedWidget.clearTextEdit()

		## Reconnect signals and reset text on action to 'Connected'
		self.__connectAction.triggered.disconnect(self.__disconnectFromHost)
		self.__connectAction.setText('&Connect')
		self.__connectAction.triggered.connect(self.__connectToSystem)


	## Send the message
	def __sendMessage(self, text):
		self.__socket.write(str(text))


	## Data is ready for reading
	def __readyRead(self):
		## Read the size of data available, return if no data
		size = self.__socket.bytesAvailable()
		if size == 0:
			return

		## Read data
		data = str(self.__socket.read(size))
		self.__connectedWidget.appendTextEdit(data)

		## Emit the write message signal
		self.__writeMessageSignal.emit(data)

		## Count the message
		self.__messages += 1


	def __writeMessage(self, data):
		## Write result to file, include a newline and force flush
		if self.__loginWidget.logToFile():
			self.file.write(data)
			self.file.write('\n')
			self.file.flush()


	## The state of the socket has changed
	def __socketStateChanged(self, state):
		#self.statusBar().showMessage(str(state))
		#print "MainWidget::socketStateChanged state", str(state)

		if (state == QtNetwork.QAbstractSocket.UnconnectedState):
			self.statusBar().showMessage("UnconnectedState")
		if (state == QtNetwork.QAbstractSocket.HostLookupState):
			self.statusBar().showMessage("HostLookupState")
		if (state == QtNetwork.QAbstractSocket.ConnectingState):
			self.statusBar().showMessage("ConnectingState")
		if (state == QtNetwork.QAbstractSocket.ConnectedState):
			self.statusBar().showMessage("ConnectedState")
		if (state == QtNetwork.QAbstractSocket.BoundState):
			self.statusBar().showMessage("BoundState")
		if (state == QtNetwork.QAbstractSocket.ClosingState):
			self.statusBar().showMessage("ClosingState")
		if (state == QtNetwork.QAbstractSocket.ListeningState):
			self.statusBar().showMessage("ListeningState")


	## Manage socket errors
	def __socketError(self, error):
		QtGui.QMessageBox.critical(self, "Chat Client", "Socket Error: %s" % self.__socket.errorString())
		return

		errorMessage = "No error"
		if error == QtNetwork.QAbstractSocket.ConnectionRefusedError:
			errorMessage = "Connection Refused Error"
		elif error == QtNetwork.QAbstractSocket.RemoteHostClosedError:
			errorMessage = "Remote Host Closed Error"
		elif error == QtNetwork.QAbstractSocket.HostNotFoundError:
			errorMessage = "Host Not Found Error"
		elif error == QtNetwork.QAbstractSocket.SocketAccessError:
			errorMessage = "Socket Access Error"
		elif error == QtNetwork.QAbstractSocket.SocketResourceError:
			errorMessage = "Socket Resource Error"
		elif error == QtNetwork.QAbstractSocket.SocketTimeoutError:
			errorMessage = "Socket Timeout Error"
		elif error == QtNetwork.QAbstractSocket.DatagramTooLargeError:
			errorMessage = "Datagram Too Large Error"
		elif error == QtNetwork.QAbstractSocket.NetworkError:
			errorMessage = "Network Error"
		elif error == QtNetwork.QAbstractSocket.AddressInUseError:
			errorMessage = "Address In Use Error"
		elif error == QtNetwork.QAbstractSocket.SocketAddressNotAvailableError:
			errorMessage = "Socket Address Not Available Error"
		elif error == QtNetwork.QAbstractSocket.UnsupportedSocketOperationError:
			errorMessage = "Unsupported Socket Operation Error"
		elif error == QtNetwork.QAbstractSocket.ProxyAuthenticationRequiredError:
			errorMessage = "Proxy Authentication Required Error"
		elif error == QtNetwork.QAbstractSocket.SslHandshakeFailedError:
			errorMessage = "Ssl Handshake Failed Error"
		elif error == QtNetwork.QAbstractSocket.UnfinishedSocketOperationError:
			errorMessage = "Unfinished Socket Operation Error"
		elif error == QtNetwork.QAbstractSocket.ProxyConnectionRefusedError:
			errorMessage = "Proxy Connection Refused Error"
		elif error == QtNetwork.QAbstractSocket.ProxyConnectionClosedError:
			errorMessage = "Proxy Connection Closed Error"
		elif error == QtNetwork.QAbstractSocket.ProxyConnectionTimeoutError:
			errorMessage = "Proxy Connection Timeout Error"
		elif error == QtNetwork.QAbstractSocket.ProxyNotFoundError:
			errorMessage = "Proxy Not Found Error"
		elif error == QtNetwork.QAbstractSocket.ProxyProtocolError:
			errorMessage = "Proxy Protocol Error"
		elif error == QtNetwork.QAbstractSocket.UnknownSocketError:
			errorMessage = "Unknown Socket Error"
		else:
			errorMessage = "Unsupported error - should not occure"

		print "MainWidget::socetError: %s %s" % (errorMessage, self.__socket.errorString())


	## Timer timeout
	def __timeout(self):
		## The timer timeout, update the status bar
		self.__seconds += 1 
		self.statusBar().showMessage('Connected %d secs : %d messages' % (self.__seconds, self.__messages))


if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	mainWidget = MainWidget()
	sys.exit(app.exec_())
