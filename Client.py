class Client():
    def __init__(self, username, password, socket):
        self.__username = username
        self.__password = password
        self.__socket = socket


    def username(self):
        return self.__username


    def setUsername(self, name):
        self.__username = name


    def setPassword(self, password):
        self.__password = password

    def password(self):
        return self.__password


    def close(self):
        if self.__socket != int(-1):
            self.__socket.close()
            self.socket = int(-1)

    def setSocket(self, socket):
        self.__socket = socket


    def socket(self):
        return self.__socket


    def write(self, message):
        self.__socket.write(message)
