import pygame
import sys

from const import *
from game import Game
from Square import Square
from move import Move
import chess
import chessEngine as ce
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("CHESS PROJECT: PvsAI")
        self.game = Game()
        self.color = None
        self.AICOLOR = None
    def playEngineMove(self, maxDepth, color):
        engine = ce.Engine(self.game.board.CHboard, maxDepth, color)
        return engine.getBestMove()
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
                if self.color == None:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                        self.color='b'
                        print("Choose black")
                        AICOLOR = chess.WHITE if self.color == 'b' else chess.BLACK
                        # AI move
                        CHmove = self.playEngineMove(4, chess.WHITE)
                        AI_ini_X, Ai_ini_Y = board.chesssquare_to_XY(CHmove.from_square)
                        AI_final_X, Ai_final_Y = board.chesssquare_to_XY(CHmove.to_square)
                        AI_ini = Square(AI_ini_X, Ai_ini_Y)
                        AI_final = Square(AI_final_X, Ai_final_Y)

                        TMPpiece = board.square[AI_ini_X][Ai_ini_Y].piece
                        print("AI turn ", Move(AI_ini, AI_final))
                        print(CHmove.uci())
                        board.move(TMPpiece, Move(AI_ini, AI_final))

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        self.color='w'
                        print("Choose white")
                        AICOLOR = chess.WHITE if self.color == 'b' else chess.BLACK

                elif event.type == pygame.MOUSEBUTTONDOWN:
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

                            if(board.CHboard.is_checkmate() or board.CHboard.is_stalemate() or board.CHboard.is_seventyfive_moves()):
                                break


                            #AI Move
                            CHmove = self.playEngineMove(4,AICOLOR)
                            AI_ini_X ,Ai_ini_Y = board.chesssquare_to_XY(CHmove.from_square)
                            AI_final_X, Ai_final_Y = board.chesssquare_to_XY(CHmove.to_square)
                            AI_ini = Square(AI_ini_X,Ai_ini_Y)
                            AI_final = Square(AI_final_X,Ai_final_Y)

                            TMPpiece = board.square[AI_ini_X][Ai_ini_Y].piece
                            print("AI turn ",Move(AI_ini,AI_final))
                            print(CHmove.uci())
                            board.move(TMPpiece,Move(AI_ini,AI_final))

                            if(board.CHboard.is_checkmate() or board.CHboard.is_stalemate() or board.CHboard.is_seventyfive_moves()):
                                break

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
