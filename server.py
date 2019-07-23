import socket, connect4logic, threading, time

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
            return 0
        self.sendMessage(colour.lower())

    def getSock(self):
        return self._sock

    def getMessage(self):
        """Wait until you get message from player and return it"""
        while True:
            try:
                message = self._sock.recv(4096)
                messageDecoded = message.decode()
                return messageDecoded
            except socket.timeout:
                continue
            except ConnectionResetError:
                return None

    def sendMessage(self, message):
        """Send a string to the player"""
        if type(message) != str:
            raise TypeError("Arg must be a string")
        if "&" in message:
            raise ValueError("Message cant contain '&'")
        else:
            message = message + "&"
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
                    otherPlayer = player
                    otherPlayer.sendMessage("other")

            while True:
                move = whosTurn.getMessage()
                columnNum = int(move)
                invalid = self.board.fullColumn(columnNum)
                if not invalid:
                    whosTurn.sendMessage("confirmed")
                    otherPlayer.sendMessage(move)
                    lastMove = self.board.placePiece(columnNum, whosTurn.getColour())
                    break
                else:
                    whosTurn.sendMessage("denied")


            win = self.board.checkWin(lastMove)
            if not win:
                for player in self._players:
                    player.sendMessage("false")
                whosTurn = otherPlayer
            else:
                whosTurn.sendMessage("won")
                otherPlayer.sendMessage("lose")
                break

                turn += 1


    def _start(self):
        """Starts the gameloop"""
        time.sleep(0.5)
        self._gameThread = threading.Thread(target = self._gameThreadMethod)
        for player in self._players:
            player.sendMessage("start")
        #Sleep for buffer so second player not overloaded
        print("A game has started")
        self._gameThread.start()



serverLoop()
