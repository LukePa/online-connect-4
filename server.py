import socket, connect4logic, threading

PORT = 7890

def serverLoop():
    """Loops continuously and handles joinging clients"""
    roomDict = {}
    sock = socket.socket()
    sock.bind(("", PORT))
    sock.listen(5)
    print("Server started")
    while True:
        conn, addr = sock.accept()
        player = Player(conn)
        roomName = player.getMessage()
        if roomName not in roomDict.keys():
            roomDict[roomName] = Gameroom()
            roomDict[roomName].addPlayer(player)
        elif roomName in roomDict.keys():
            if not roomDict[roomName].isFull():
                roomDict[roomName].addPlayer(player)
            else:
                player.sendMessage("Room is full")
                
            

class Player(object):

    def __init__(self, sock):
        self._colour = None
        self._sock = sock
        print("Player created")

    def getColour(self):
        return self._colour

    def setColour(self, colour):
        if colour.lower() == "red":
            self._colour = "red"
        elif colour.lower() == "yellow":
            self._colour = "yellow"
        else:
            raise ValueError("Argument must be 'red' or 'yellow'")

    def getSock(self):
        return self._sock

    def getMessage(self):
        """Wait until you get message from player and return it"""
        message = self._sock.recv(4096)
        messageDecoded = message.decode()
        return messageDecoded

    def sendMessage(self, message):
        """Send a string to the player"""
        if type(message) != str:
            raise TypeError("Arg must be a string")
        else:
            self._sock.sendall(message.encode())
        
    

class Gameroom(object):

    def __init__(self):
        #players is list of player objects
        self._players = []
        print("Room created")


    def isFull(self):
        if len(self._players) > 1:
            return True

    def checkToStart(self):
        """Checks if enough players are in room, starts if true"""
        if len(self._players) == 2:
            self._start()
        else:
            for player in self._players:
                player.sendMessage("Waiting for more players...")

    def addPlayer(self, player):
        """Adds player to game room"""
        if type(player) != Player:
            raise TypeError("Arg must be a player object")
        elif self.isFull():
            raise RuntimeError("Added player to full room")
        else:
            self._players.append(player)
            player.sendMessage("Added to gameroom...")
        self.checkToStart()


    def _gameThreadMethod(self):
        """Runs as thread, handles gameloop that players interact with"""
        self._players[0].setColour("red")
        self._players[1].setColour("yellow")
        for player in self._players:
            player.sendMessage(player.getColour())
        whosTurn = self._players[0]
        exit = False
        turn = 0
        lastMove = ()
        self.board = connect4logic.Board()

        while not exit:
            for player in self._players:
                if whosTurn == player:
                    player.sendMessage("yours")
                else:
                    player.sendMessage("other")

            while True:
                move = whosTurn.getMessage()
                columnNum = int(move)
                isValid = self.board.fullColumn(columnNum)
                if isValid:
                    whosTurn.sendMessage("confirmed")
                    lastMove = self.board.placePiece(columnNum, whosTurn.getColour())
                    break
                else:
                    whosTurn.sendMessage("denied")

            if self._players[0] == whosTurn:
                self._players[1].sendMessage(str(columnNum))
            else:
                self._players[0].sendMessage(str(columnNum))

            win = self.board.checkWin(lastMove)
            if not win:
                for player in self._players:
                    player.sendMessage("false")
                if whosTurn == self._players[0]:
                    whosTurn = self._players[1]
                else:
                    whosTurn = self._players[0]
            else:
                if whosTurn == self._players[0]:
                    loser = self._players[1]
                    winner = self._playrs[0]
                else:
                    loser = self._players[0]
                    winner = self._players[1]
                winner.sendMessage("won")
                loser.sendMessage("lose")

            turn += 1


    def _start(self):
        """Starts the gameloop"""
        self._gameThread = threading.Thread(target = self._gameThreadMethod)
        for player in self._players:
            player.sendMessage("start")
        print("A game has started")
        self._gameThread.start()



serverLoop()