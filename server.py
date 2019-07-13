import socket, connect4logic

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

    def _start(self):
        """Starts the gameloop"""
        print("A game has started")
        for player in self._players:
            player.sendMessage("start")



serverLoop()