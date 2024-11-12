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

    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running = False
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