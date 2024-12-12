

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

    @staticmethod
    def getRookMovesOneColor(r, c, moves, board, color):
        tempR = r
        if r - 1 >=0:
            while board[r-1][c]=="--":
                m = Move((tempR,c), (r-1,c), board)
                moves.add(m)
                r = r -1 
                if r - 1< 0:
                    break
        if r - 1 >=0:
            if board[r-1][c][0]==color:
                moves.add(Move((tempR,c), (r-1,c), board))
        r = tempR
        if r + 1 <= 7: 
            while board[r+1][c]=="--":
                m = Move((tempR,c), (r+1,c), board)
                moves.add(m)
                r = r +1 
                if r+ 1 > 7:
                    break
        if r + 1 <= 7: 
            if board[r+1][c][0]==color:
                moves.add(Move((tempR,c), (r+1,c), board))
        r = tempR
        tempC = c
        if c - 1 >= 0:
            while board[r][c-1]=="--":
                moves.add(Move((r,tempC),(r,c-1), board))
                c = c - 1
                if c - 1 < 0:
                    break
        if c - 1 >= 0:
            if board[r][c-1][0]==color:
                moves.add(Move((tempR,c), (r,c-1), board))
        c = tempC
        if c + 1 <= 7:
            print(f"r,c+1 {(r,c+1)}")
            while board[r][c+1]=="--":
                moves.add(Move((r,tempC),(r,c+1), board))
                c = c + 1
                if c + 1 > 7:
                    break
        if c + 1 <= 7:
            if board[r][c+1][0]==color:
                moves.add(Move((tempR,c), (r,c+1), board))
 
        
    def getRookMoves(self, r, c, moves):
        if self.whiteToMove: #white rooks
            GameState.getRookMovesOneColor(r, c, moves, self.board, "b")
        else: #black rooks
            GameState.getRookMovesOneColor(r, c, moves, self.board, "w")

    @staticmethod
    def knightMoveBoard(r1, c1, r2, c2, moves, board, color):
        if board[r2][c2]=="--":
            moves.add(Move((r1,c1), (r2, c2), board))
        elif board[r2][c2][0]==color:
            moves.add(Move((r1,c1), (r2, c2), board))

    def getKnightMovesSingleColor(self, r, c, moves, color):
        if r - 2 >=0:
            if c + 1 <= 7:
                GameState.knightMoveBoard(r, c, r -2, c + 1,moves,self.board, color)
            if c - 1 >= 0:
                GameState.knightMoveBoard(r, c, r -2, c - 1,moves,self.board, color)
        if r + 2 <=7:
            if c + 1 <= 7:
                GameState.knightMoveBoard(r, c, r +2, c + 1,moves,self.board, color)
                
            if c - 1 >= 0:
                GameState.knightMoveBoard(r, c, r +2, c - 1,moves,self.board, color)
        if c - 2 >=0:
            if r + 1 <= 7:
                GameState.knightMoveBoard(r, c, r + 1, c - 2,moves,self.board, color)
            if r - 1 >= 0:
                GameState.knightMoveBoard(r, c, r - 1, c - 2,moves,self.board, color)
        if c + 2 <=7:
            if r + 1 <= 7:
                GameState.knightMoveBoard(r, c, r + 1, c + 2,moves,self.board, color)
            if r - 1 >= 0:
                GameState.knightMoveBoard(r, c, r - 1, c + 2,moves,self.board, color)

    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
            self.getKnightMovesSingleColor(r, c, moves, "b")
        else:
            self.getKnightMovesSingleColor(r, c, moves, "w")

    def bishopMoveBoard(self, r, c, moves, color):
        i = 1
        if r-i>=0 and c+i<=7:
            while self.board[r-i][c+i]=="--":
                moves.add(Move((r,c), (r-i, c+i), self.board))
                print(f"appending3 {(r-i, c+i)}")
                i += 1
                if r-i<0 or c+i>7:
                    break
        if r-i>=0 and c+i<=7:
            if self.board[r-i][c+i][0]==color:
                moves.add(Move((r,c), (r-i, c+i), self.board))
            
        i = 1
        if c-i>=0 and r+i<=7:
            while self.board[r+i][c-i]=="--":
                moves.add(Move((r,c), (r+i, c-i), self.board))
                print(f"appending4 {(r+i, c-i)}")
                i += 1
                if c-i<0 or r+i>7:
                    break
        if c-i>=0 and r+i<=7:
            if self.board[r+i][c-i][0]==color:
                moves.add(Move((r,c), (r+i, c-i), self.board))
            
        i = 1
        if c-i>=0 and r-i>=0:
            while self.board[r-i][c-i]=="--":
                moves.add(Move((r,c), (r-i, c-i), self.board))
                print(f"appending5 {(r-i, c-i)}")
                i += 1
                if c-i<0 or r-i<0:
                    break
        if c-i>=0 and r-i>=0:
            if self.board[r-i][c-i][0]==color:
                moves.add(Move((r,c), (r-i, c-i), self.board))
        i = 1
        if c+i<=7 and r+i<=7:
            while self.board[r+i][c+i]=="--":
                moves.add(Move((r,c), (r+i, c+i), self.board))
                print(f"appending6 {(r+i, c+i)}")
                print(f"r,c,i {(r,c),i}")
                i += 1
                if c+i>7 or r+i>7:
                    break
        if c+i<=7 and r+i<=7:
            if self.board[r+i][c+i][0]==color:
                moves.add(Move((r,c), (r+i, c+i), self.board))


    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
            self.bishopMoveBoard(r, c, moves,"b")
        else:
            self.bishopMoveBoard(r, c, moves,"w")


    def getQueenMoves(self, r, c, moves):
        pass


    def getKingMoves(self, r, c, moves):
        pass