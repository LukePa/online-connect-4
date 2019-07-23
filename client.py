import socket, sys, pygame, connect4logic


class GameClient(object):
    """Object player will use to talk to the server"""

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
        message = ""
        while True:
            try:
                char = self._sock.recv(1)
                charDecoded = char.decode()
                if charDecoded != "&":
                    message += charDecoded
                else:
                    return message
            except socket.timeout:
                message = ""
                continue
            except ConnectionResetError:
                input("Connection closed, press enter to end")
                sys.exit()


    def sendMessage(self, message):
        """Send message to server"""
        if type(message) != str:
            raise TypeError("Message must be a string")
        try:
            self._sock.sendall(message.encode())
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
                print(message)


    def yourTurn(self):
        """Runs if it is your turn"""
        while True:
            move = self.getInputMove()
            self.sendMessage(move)
            response = self.recieveMessage()
            if response == "confirmed":
                self.doMove(int(move), self._colour)
                break
            elif response == "denied":
                continue


    def otherTurn(self):
        """Runs if its the other players turn"""
        move = self.recieveMessage()
        self.doMove(int(move), self._otherColour)


    def getInputMove(self):
        move = input("Move: ")
        return move


    def doMove(self, columnNum, colour):
        move = self.gameBoard.placePiece(columnNum, colour)
        #self.renderer.moveAnimation(move, colour)


    def win(self):
        """Runs if you won"""
        return None

    def lose(self):
        """Run if you lose"""
        return None


    def initialise(self):
        self.gameBoard = connect4logic.Board()
        self.renderer = Renderer()

    def gameloop(self):
        """Overall loop that makes game work"""
        self.initialise()
        self._colour = self.recieveMessage()
        if self._colour == "red":
            self._otherColour = "yellow"
        else:
            self._otherColour = "red"
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.renderer.testRender(self.gameBoard)
            self.renderer.renderBoard(self.gameBoard)
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
                else:
                    sys.exit()



class Renderer(object):
    def __init__(self):
        self.TILESIZE = 60
        self.HEIGHT = self.TILESIZE * 6
        self.WIDTH = self.TILESIZE * 7
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.CRIMSON = (220, 20, 60)
        self.BLUE = (0, 0, 255)
        self._surface = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption("Connect 4")


    def renderBackground(self, backgroundColour):
        self._surface.fill(backgroundColour)


    def renderPieces(self, redColour, yellowColour, board):
        for x in range(7):
            for y in range (6):
                piece = board.getPiece(x, y)
                if piece == None:
                    continue
                elif piece.lower() == "red":
                    colour = redColour
                elif piece.lower() == "yellow":
                    colour = yellowColour
                else:
                    continue
                xPosition = (x * self.TILESIZE) + self.TILESIZE//2
                yPosition = (abs(5-y) *self.TILESIZE) + self.TILESIZE//2
                pygame.draw.circle(self._surface, colour, (xPosition, yPosition), self.TILESIZE//2)


    def renderBoard(self, board):
        self.renderBackground(self.GREEN)
        self.renderPieces(self.CRIMSON, self.YELLOW, board)
        pygame.display.update()


    def testRender(self, board):
        if type(board) != connect4logic.Board:
            raise TypeError("board must be board object")
        print(board)


def main():
    pygame.init()
    gameClient = GameClient()
    gameClient.accessServer()
    gameClient.waitForStart()
    gameClient.gameloop()


if __name__ == "__main__":
    main()
