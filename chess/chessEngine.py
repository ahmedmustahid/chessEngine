

class Move:

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,"f": 5,"g": 6,"h": 7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __hash__(self):
        return hash(self.moveID)

    def __repr__(self):
        return self.getChessNotation()

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol)+self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col]+self.rowsToRanks[row]


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp",],
            ["--","--","--","--","--","--","--","--",],
            ["--","--","--","--","--","--","--","--",],
            ["--","--","--","--","--","--","--","--",],
            ["--","--","--","--","--","--","--","--",],
            ["wp", "wp","wp","wp","wp","wp","wp","wp",],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.movefunctions = {"p": self.getPawnMoves,"R":self.getRookMoves,
                                "N":self.getKnightMoves, "B":self.getBishopMoves,
                                "Q":self.getQueenMoves, "K":self.getKingMoves}
        self.whiteToMove = True
        self.movelog = []

    def makeMove(self, move: Move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.movelog)!=0:
            move = self.movelog.pop()
            self.board[move.endRow][move.endCol], self.board[move.startRow][move.startCol] = move.pieceCaptured, move.pieceMoved
            self.whiteToMove = not self.whiteToMove

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()


    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = set()
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn =='w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.movefunctions[piece](r, c, moves)
        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawns
            if self.board[r-1][c]=="--":
                moves.add(Move((r,c), (r-1,c), self.board)) 
                if r==6 and self.board[r-2][c]=="--":
                    moves.add(Move((r,c), (r-2,c), self.board))
            
            if c - 1 >= 0: #left black
                if self.board[r-1][c-1][0]=="b":
                    moves.add(Move((r,c), (r-1, c-1), self.board))
            if c + 1 <= 7:
                if self.board[r-1][c+1][0]=="b":
                    moves.add(Move((r,c), (r-1, c+1), self.board))
        
        else:
            if self.board[r+1][c]=="--":
                moves.add(Move((r,c), (r+1, c), self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.add(Move((r,c), (r+2, c), self.board))
            if c - 1 >=0:
                if self.board[r+1][c-1][0]=="w":
                    moves.add(Move((r,c),(r+1, c-1), self.board))
            if c + 1 <= 7:
                if self.board[r+1][c+1][0]=="w":
                    moves.add(Move((r,c),(r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(1,0),(-1,0),(0,1),(0,-1)]#up, down, right, left
        enemycolor = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1, 8):
                r2 = r + direction[0] * i
                c2 = c + direction[1] * i
                if 0 <= r2 < 8 and 0 <= c2 < 8:
                    if self.board[r2][c2]=="--":
                        moves.add(Move((r, c), (r2, c2), self.board))
                    elif self.board[r2][c2][0]==enemycolor:
                        moves.add(Move((r, c), (r2, c2), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getKnightMoves(self, r, c, moves):
        directions = [(2, 1), (-2, 1), (-2, -1), (2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]
        nonenemycolor = "w" if self.whiteToMove else "b"
        for direction in directions:
            r2 = r + direction[0]
            c2 = c + direction[1]
            if 0 <= r2 < 8 and 0<= c2 < 8:
                if self.board[r2][c2][0]!=nonenemycolor:
                    moves.add(Move((r,c), (r2,c2), self.board))


    def getBishopMoves(self, r, c, moves):
        directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
        enemycolor = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(8):
                r2 = r + direction[0] * i
                c2 = c + direction[1] * i
                if 0<= r2 <8 and 0<= c2 <8:
                    if self.board[r2][c2]=="--":
                        moves.add(Move((r,c),(r2,c2), self.board))
                    elif self.board[r2][c2][0]==enemycolor:
                        moves.add(Move((r,c),(r2,c2), self.board))
                        break
                else:
                    break


    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
        directions += [(1,0),(-1,0),(0,1),(0,-1)]#up, down, right, left
        nonenemycolor = "w" if self.whiteToMove else "b"
        for d in directions:
            r2 = r + d[0]
            c2 = c + d[1]
            if 0<= r2 < 8 and 0<= c2 < 8:
                if self.board[r2][c2][0]!=nonenemycolor:
                    moves.add(Move((r,c), (r2, c2), self.board))
