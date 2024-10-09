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
        pygame.display.set_caption("CHESS PROJECT: AIvsAI")
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

        AI1 = None
        AI2 = None
        AICOLOR = chess.WHITE
        Run = False
        Run2 = True
        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            pygame.time.delay(800)


            if dragger.dragging:
                dragger.update_blit(screen)
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()

                if AI1 == None or AI2==None:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                        print(2)
                        if AI1==None:
                            AI1 = 2
                        else :
                            AI2 = 2
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                        print(3)
                        if AI1==None:
                            AI1 = 3
                        else :
                            AI2 = 3
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                        print(4)
                        if AI1==None:
                            AI1 = 4
                        else :
                            AI2 = 4
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                        print(5)
                        if AI1==None:
                            AI1 = 5
                        else :
                            AI2 = 5
                else:
                    Run = True
                    break

            if Run and Run2:
                AI = AI1 if (AICOLOR==chess.WHITE) else AI2
                CHmove = self.playEngineMove(AI,AICOLOR)
                print(CHmove)
                AI_ini_X ,Ai_ini_Y = board.chesssquare_to_XY(CHmove.from_square)
                AI_final_X, Ai_final_Y = board.chesssquare_to_XY(CHmove.to_square)
                AI_ini = Square(AI_ini_X,Ai_ini_Y)
                AI_final = Square(AI_final_X,Ai_final_Y)

                TMPpiece = board.square[AI_ini_X][Ai_ini_Y].piece
                print("AI turn ",Move(AI_ini,AI_final))
                print(CHmove.uci())
                board.move(TMPpiece,Move(AI_ini,AI_final))

                AICOLOR = chess.WHITE if (AICOLOR==chess.BLACK) else chess.BLACK
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                #pygame.time.delay(400)

                if(board.CHboard.is_checkmate() or board.CHboard.is_stalemate() or board.CHboard.is_seventyfive_moves()):
                    Run=False
                    Run2 =False


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
