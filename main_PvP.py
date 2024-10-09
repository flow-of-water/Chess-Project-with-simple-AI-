import pygame
import sys

from const import *
from game import Game
from Square import Square
from move import Move
import chess

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("CHESS PROJECT: PvsP")
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            if dragger.dragging:
                dragger.update_blit(screen)
            for event in pygame.event.get() :
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY//SQSIZE
                    clicked_col = dragger.mouseX//SQSIZE

                    if board.square[clicked_row][clicked_col].has_piece():
                        piece = board.square[clicked_row][clicked_col].piece

                        board.calc_moves(piece, board.CHboard , board.XY_to_chesssquare(clicked_row,clicked_col) , clicked_row,clicked_col)

                        dragger.save_ini(event.pos)
                        dragger.drag_piece(piece)

                        #show
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #show
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        ini = Square(dragger.ini_row,dragger.ini_col)
                        final = Square(released_row,released_col)
                        move = Move(ini,final)

                        if board.valid_move(dragger.piece,move):
                            board.move(dragger.piece,move)
                            #show
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
            if (board.CHboard.is_checkmate() or board.CHboard.is_stalemate() or board.CHboard.is_seventyfive_moves()):
                Label =""
                if board.CHboard.outcome() == None:
                    Label = "draw"
                elif board.CHboard.outcome().winner == chess.WHITE:
                    Label = "white won"
                elif board.CHboard.outcome().winner == chess.BLACK:
                    Label = "black won"
                else :
                    Label = "draw"
                base_font = pygame.font.Font(None, 100)
                text_surface0 = base_font.render(Label, True, (255,255,255))
                screen.blit(text_surface0, (200, 200))

            pygame.display.update()

# main = Main()
# main.mainloop()
