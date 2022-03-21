"""
    This is our main driver file. It will be responsible for handling user input and displaying the current GameState object
"""

import pygame as p
import ChessEngine


WIDTH = HEIGHT = 640 #400 is another option
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

"""
    Initialize a global dictionary of images. This will be called exactly once in the main
"""
def load_images():
    # IMAGES['wp'] will return the actual image of the piece
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))


"""
    Draw squares on the board. Top left square is always light.
"""
def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) %2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
    Draw pieces on the board
"""
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # Empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
    Responsible for all graphics within a current game state
"""
def draw_game_state(screen, gs):
    draw_board(screen) # Draw squares on the board
    # add in piece highlighting or move suggestions later
    draw_pieces(screen,gs.board) # Draw pieces on top of those square



"""
    The main driver for our code. This will handle user input and updating the graphics
"""
def main():
    
    p.init()
    
    screen = p.display.set_mode((WIDTH, HEIGHT))
    
    clock = p.time.Clock()
    
    screen.fill(p.Color("white"))
    
    gs = ChessEngine.GameState()
    
    load_images() # Only done once, before the while loop
    
    running = True

    sqSelected = () # no square is selected initially, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of player clicks (two tuples: [(6,4), (4,4)])

    while running:
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): # the user clicked the same square twice
                    sqSelected = () # deselecting
                    playerClicks = [] # clear selected clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                
                if len(playerClicks) == 2: # after thr second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #reset user clicks
                    playerClicks = []

        draw_game_state(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        




if __name__ == "__main__":
    main()
