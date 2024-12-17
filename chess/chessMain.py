import pygame as p
import chessEngine

HEIGHT = WIDTH = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImage():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "bR", "bN", "bB", "bQ", "bK", "bp", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = chessEngine.GameState()

    loadImage()
    running = True
    validMoves = gs.getValidMoves()
    moveState = False#flag variable to call move only when needed and not at every frame

    sqSelected = ()#(row, col);last user click
    playerClicks = []#keep track of player clicks: two tuples
    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()#(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected==(row,col):#user selects the same square twice
                    sqSelected = () #unselect if selection same as previous selection
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)#append for 1st and 2nd clicks

                if len(playerClicks)==2:
                    if gs.board[playerClicks[0][0]][playerClicks[0][1]]!="--":
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(f"moving {move.getChessNotation()}")
                        print(f"player clicks before {playerClicks}")
                        # print(move)
                        # print(f"validMoves {validMoves}")
                        # print(f"movestate {moveState}")
                        if move in validMoves:
                            print(f"player clicks after {playerClicks}")
                            gs.makeMove(move)
                            moveState = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveState = True
        if moveState: #generate new set of validmoves once a validmoves has been made
            validMoves = gs.getValidMoves()
            # print(f"validMoves2 {validMoves}")
            moveState = False
        drawGameState(screen, gs) 
        clock.tick(MAX_FPS)
        p.display.flip()

def drawBoard(screen):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if (i+j)%2==0:
                color = 'white'
            else:
                color = 'grey'
            rect = p.Rect((i* SQ_SIZE , j*SQ_SIZE), (SQ_SIZE, SQ_SIZE))
            p.draw.rect(screen,color=p.Color(color), rect=rect)
            

def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece!="--":
                screen.blit(IMAGES[piece],(j* SQ_SIZE , i*SQ_SIZE))



def drawGameState(screen, gs):
    drawBoard(screen)

    drawPieces(screen, gs.board)

if __name__=="__main__":
    main()