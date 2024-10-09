import pygame
from const import *
from Board import Board
from dragger import *
from Square import Square
class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    def show_bg(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if(row+col)%2==0:
                    #light green
                    color = (234,235,200)
                else:
                    #dark green
                    color = (119,154,80)
                rect = (col*SQSIZE, row*SQSIZE,SQSIZE,SQSIZE)
                # (x ,y , width , height)

                pygame.draw.rect(surface,color,rect)

                #danh so thu tu
                if col==0:
                    color = (119,154,80) if (row+col)%2==0 else (234,235,200)
                    label = pygame.font.SysFont('monospace', 18, bold=True).render(str(ROWS-row),1,color)
                    label_pos = (5,5+row*SQSIZE)
                    surface.blit(label,label_pos)
                if row==7:
                    color = (119,154,80) if (row+col)%2==0 else (234,235,200)
                    label = pygame.font.SysFont('monospace', 18, bold=True).render(str(Square.getAlphaCol(col)),1,color)
                    label_pos = (col *SQSIZE+SQSIZE-20,HEIGHT-20)
                    surface.blit(label,label_pos)


    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.square[row][col].has_piece():
                    piece= self.board.square[row][col].piece

                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture)
                        img_center = col*SQSIZE + SQSIZE//2, row*SQSIZE + SQSIZE//2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img,piece.texture_rect)
    def show_moves(self,surface):
        if self.dragger.dragging:
            piece= self.dragger.piece

            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.col)%2==0 else "#C84646"
                rect = (move.final.col *SQSIZE , move.final.row * SQSIZE , SQSIZE , SQSIZE)
                pygame.draw.rect(surface,color,rect)

    def show_last_move(self,surface):
        if self.board.last_move :
            ini = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [ini , final] :
                color = (244,247,116) if (pos.row+pos.col)%2==0 else (172,195,51)
                rect= (pos.col * SQSIZE , pos.row *SQSIZE ,SQSIZE , SQSIZE)
                pygame.draw.rect(surface,color,rect)


    def reset(self):
        self.__init__()