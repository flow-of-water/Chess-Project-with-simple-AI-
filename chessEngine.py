import chess as ch
import random as rd


class Engine:

    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth

    def getBestMove(self):
        return self.engine(None, 1)

    def evalFunct(self):
        compt = 0
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOpportunity() + 3 * rd.random() * rd.random()
        return compt

    def mateOpportunity(self):
        if (self.board.legal_moves.count() == 0):
            if (self.board.turn == self.color and self.board.is_checkmate()):
                return -999
            elif (self.board.turn != self.color and self.board.is_checkmate()):
                return 999
            else :
                return 0
        else:
            return 0



    def squareResPoints(self, square):
        pieceValue = 0
        if (self.board.piece_type_at(square) == ch.PAWN):
            pieceValue = 1
        elif (self.board.piece_type_at(square) == ch.ROOK):
            pieceValue = 5
        elif (self.board.piece_type_at(square) == ch.BISHOP):
            pieceValue = 3.5
        elif (self.board.piece_type_at(square) == ch.KNIGHT):
            pieceValue = 3
        elif (self.board.piece_type_at(square) == ch.QUEEN):
            pieceValue = 9

        if (self.board.color_at(square) != self.color):
            return -pieceValue
        else:
            return pieceValue

    def engine(self, candidate, depth):

        if (depth == self.maxDepth or self.board.legal_moves.count() == 0):
            return self.evalFunct()

        else:
            moveList = list(self.board.legal_moves)

            newCandidate = None
            if (depth % 2 != 0):
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")

            for i in moveList:

                self.board.push(i)

                value = self.engine(newCandidate, depth + 1)

                # AI turn
                if (value > newCandidate and depth % 2 != 0):
                    if (depth == 1):
                        move = i
                    newCandidate = value
                # humarn turn
                elif (value < newCandidate and depth % 2 == 0):
                    newCandidate = value

                # Cat tia Alpha-Beta
                #(if previous move was made by AI)
                if (candidate != None
                        and value < candidate
                        and depth % 2 == 0):
                    self.board.pop()
                    break
                # (if previous move was made by human )
                elif (candidate != None
                      and value > candidate
                      and depth % 2 != 0):
                    self.board.pop()
                    break

                self.board.pop()

            if (depth > 1):
                # return value of a move in the tree
                return newCandidate
            else:
                # return the move (for root of tree)
                return move



