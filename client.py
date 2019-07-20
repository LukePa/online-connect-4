import socket, sys, connect4logic


class GameClient(object):
    """Object player will use to talk to the server"""
    def __init__(self):
        self.gameBoard = connect4logic.Board()


    def enterDetails(self):
        address = input("Enter server address: ")
        port = input("Enter port: ")
        while not port.isdigit():
            port = input("Enter a valid port: ")
        port = int(port)
        roomName = input("Enter room name: ")
        return address, port, roomName


    def connector(self, address, port, roomName):
        """Creates connection between client and server"""
        try:
            print("Connecting...")
            self._sock = socket.socket()
            self._sock.connect((address, port))
            self._sock.sendall(roomName.encode())
            self._sock.settimeout(10)
            print("Connected.")
        except socket.timeout:
            input("Connection failed")
            sys.exit()


    def accessServer(self):
        address, port, roomName = self.enterDetails()
        self.connector(address, port, roomName)


    def recieveMessage(self):
        """Wait for message from the server"""
        while True:
            try:
                message = self._sock.recv(4096)
                messageDecoded = message.decode()
                return messageDecoded
            except socket.timeout:
                continue
            except ConnectionResetError:
                input("Connection closed, press enter to end")
                sys.exit()


    def waitForStart(self):
        """Wait for message from server saying 'start', this stops loop, indicated game starting, print all recieved"""
        exit = False
        while not exit:
            message = self.recieveMessage()
            if message.lower() == "start":
                exit = True
            else:
                print(messageDecoded)


    def yourTurn(self):
        """Runs if it is your turn"""


    def otherTurn(self):
        """Runs if its the other players turn"""


    def win(self):
        """Runs if you won"""


    def lose(self):
        """Run if you lose"""


    def gameloop(self):
        """Overall loop that makes game work"""
        colour = self.recieveMessage()
        exit = False
        while not exit:
            whosTurn = self.recieveMessage()
            if whosTurn == "yours":
                self.yourTurn()
            elif whosTurn == "other":
                self.otherTurn()

            winStatus = self.recieveMessage()
            if winStatus != "false":
                exit = True
                if winStatus == "won":
                    self.win()
                elif winStatus == "lose":
                    self.lose()
                break



def main():
    gameClient = GameClient()
    gameClient.accessServer(self)
    gameClient.waitForStart()
    gameClient.gameloop()


if __name__ == "__main__":
    main()