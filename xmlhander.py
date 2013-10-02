from PySide import QtXml

xml_header = str('<?xml version="1.0" encoding="iso-8859-1"?>')

class ServerXmlHandler(QtXml.QXmlDefaultHandler):
    def __init__(self):
        super(ServerXmlHandler, self).__init__()

        self.debug = False

        self.qNameMode = 'unset'

        self.errorMessage = str('')
        self.user = str('')
        self.password = str('')
        self.message = str('')
        self.documentStartTag = False


    def startElement(self, namespaceURI, localName, qName, attributes):

        if self.debug:
            print 'startElement TOP', qName

        if not self.documentStartTag and qName != 'chat':
            print 'DOCUMENT START NOT DETECTED'
            self.errorMessage = str('Document start tag not detected')
            return False

        if qName == 'chat':
            if self.debug:
                print 'startElement QNAME == chat'

            self.qNameMode = 'chat-start'
            self.documentStartTag = True

        if qName == 'content':
            self.qNameMode = 'content-start'
            self.user = attributes.value('user')
            self.type = attributes.value('type')
            if self.debug:
                print 'startElement QNAME == content, user, type:', self.user, self.type

        if qName == 'message':
            self.qNameMode = 'message-start', self.type
            if self.type == 'message':
                self.message = attributes.value('message')
            elif self.type == 'login':
                self.password = attributes.value('message')
                #print 'startElement type login', self.password
            elif self.type == 'request':
                self.message = attributes.value('message')
            elif self.type == 'user-list' or self.type == 'all-user-list':
                self.message = attributes.value('message')
            elif self.type == 'error':
                self.message = attributes.value('message')
                print 'error'
            else:
                print 'UNKNOWN MESSAGE TYPE ERROR'
                self.errorMessage = str('Unknown message type')
                return False

        return True


    def endElement(self, namespaceURI, localName, qName):

        if qName == 'chat':
            self.qNameMode = 'unset'
            self.documentStartTag = False

        elif qName == 'content':
            self.qNameMode = 'content-end'
            #print 'End of content'

        elif qName == 'message':
            self.qNameMode = 'message-end'
            #print 'End of message'

        else:
            print 'UNKNOWN QNAME END TAG ERROR'
            self.errorMessage = str('Unknown qName end tag')
            return False

        return True

    def fatalError(self, exception):
        print 'FATAL ERROR ENCOUNTERED'
        return False

    def errorString(self):
        print 'DEBUG errorString function', self.errorMessage
        return self.errorMessage

    def createChildItem(self, tagName):
        print 'DEBUG chreateChildItem function'
        return childItem

class UsernamePasswordXmlHandler(QtXml.QXmlDefaultHandler):
    def __init__(self):
        super(UsernamePasswordXmlHandler, self).__init__()

        self.debug = True

        self.qNameMode = 'unset'

        self.errorMessage = str('')
        self.list = {}
        self.documentStartTag = False

    def getlist(self):
        return self.list

    def startElement(self, namespaceURI, localName, qName, attributes):

        if self.debug:
            print 'startElement TOP', qName

        if not self.documentStartTag and qName != 'userpassword':
            print 'DOCUMENT START NOT DETECTED'
            self.errorMessage = str('Document start tag not detected')
            return False

        if qName == 'userpassword':
            if self.debug:
                print 'startElement QNAME == userpassword'

            self.qNameMode = 'userpass-start'
            self.documentStartTag = True

        if qName == 'user':
            self.qNameMode = 'userpass-user'
            username = attributes.value('name')
            password = attributes.value('password')
            print username, password

            if username != str('') and password != str(''):
                self.list[username] = password

        return True

    def endElement(self, namespaceURI, localName, qName):

        if qName == 'userpassword':
            self.qNameMode = 'unset'
            self.documentStartTag = False
        elif qName == 'user':
            self.qNameMode = 'content-end'
        else:
            print 'UNKNOWN QNAME END TAG ERROR'
            self.errorMessage = str('Unknown qName end tag')
            return False

        return True

    def fatalError(self, exception):
        print 'FATAL ERROR ENCOUNTERED'
        return False

    def errorString(self):
        print 'DEBUG errorString function', self.errorMessage
        return self.errorMessage

    def createChildItem(self, tagName):
        print 'DEBUG chreateChildItem function'
        return childItem
