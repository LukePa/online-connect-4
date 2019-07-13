

class Board():
    """Represents a connect 4 board"""

    def __init__(self):
        board = []
        for i in range(7):
            board.append([None,None, None,None,None,None,])
        self._board = board


    def getPiece(self,x,y):
        if not self.onBoard(x,y):
            raise ValueError("Given coords not on board")
        return self._board[x][y]


    def getBoard(self):
        return self._board.copy()


    def fullColumn(self, column):
        """Checks if given column is full"""
        if type(column) != int:
            raise TypeError("Column must be an int")
        elif column > 6 or column < 0:
            raise ValueError("Column must be between 0-6 inclusive")
        column = self._board[column]
        if column[5] == None:
            return False
        else:
            return True


    def onBoard(self, x, y=0):
        """Given x and y coord returns true if its a valid coordinate"""
        if type(x) != int:
            raise TypeError("x must be an int")
        if type(y) != int:
            raise TypeError("y must be an int")
        if x < 0 or x > 6:
            return False
        if y < 0 or y > 5:
            return False
        return True


    def placePiece(self, columnVal, colour):
        """Places piece on board, returns coords piece landed at"""
        if type(columnVal) != int:
            raise TypeError("Column must be an int")
        elif not self.onBoard(columnVal):
            raise ValueError("Invalid column number")
        if type(colour) != str:
            raise TypeError("Colour must be a string")
        colour = colour.lower()
        if colour != "red" and colour != "yellow":
            raise ValueError("Colour must be 'red' or 'yellow'")
        if self.fullColumn(columnVal):
            raise RuntimeError("Tried to add piece to full column")
        else:
            column = self._board[columnVal]
            for i in range(len(column)):
                if column[i] == None:
                    column[i] = colour
                    rowVal = i
                    break
            return columnVal, rowVal


    def checkWin(self, x, y):
        """Given x and y coord, check if it involved in a win"""
        if not self.onBoard(x,y):
            raise ValueError("Given coord was not on board")
        currentPiece = self.getPiece(x,y)
        if currentPiece == None:
            return False
        #first value in tuple = left direction, second is right
        horizontal = ((-1,0),(1,0))
        diag1 = ((-1,+1),(1,-1))
        vertical = ((0,1),(0,-1))
        diag2 = ((1,-1),(-1,1))
        directions = (horizontal, vertical, diag1, diag2)
        for direction in directions:
            left = direction[0]
            right = direction[1]
            inRow = 1
            for i in range(1,4):
                if left != False:
                    lxcoord = x+(left[0]*i)
                    lycoord = y+(left[1]*i)
                    if self.onBoard(lxcoord, lycoord):
                        lpiece = self.getPiece(lxcoord,lycoord)
                        if currentPiece == lpiece:
                            inRow += 1
                        else:
                            left = False
                    else:
                        left = False

                if right != False:
                    rxcoord = x+(right[0]*i)
                    rycoord = y+(right[1]*i)
                    if self.onBoard(rxcoord,rycoord):
                        rpiece = self.getPiece(rxcoord,rycoord)
                        if currentPiece == rpiece:
                            inRow += 1
                        else:
                            right = False
                    else:
                        right = False


                if inRow >=  4:
                    return True

        return False


if __name__ == "__main__":
    board = Board()
    while True:
        b = board.getBoard()
        for i in range(5,-1,-1):
            m = ""
            for column in b:
                m += str(column[i]) + ", "
            print(m)
        x = input("X: ")
        colour = input("Colour: ")
        x, y = board.placePiece(int(x),colour)
        print(board.checkWin(x,y))