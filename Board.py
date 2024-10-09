from const import *
from Square import Square
from piece import *
import chess
from move import *

class Board:
    def __init__(self):
        self.square = [[0, 0, 0, 0, 0, 0, 0, 0]
                       for col in range(COLS)]
        self.last_move=None
        self._create()
        self._add_piece("white")
        self._add_piece("black")


        self.CHboard = chess.Board()


    def XY_to_chesssquare(self,row,col):
        return chess.square(col , 7-row)
    def chesssquare_to_XY(self,square):
        col = chess.square_file(square)
        row = chess.square_rank(square)
        row = 7-row
        return (row,col)
    def legal_moves_of_piece(self,CHboard, CHsquare):
        piece = CHboard.piece_at(CHsquare)
        if piece is None:
            return []
        return [move for move in CHboard.legal_moves if move.from_square == CHsquare]

    def calc_moves(self,piece,CHboard,CHsquare,row,col):

        Legal_move = self.legal_moves_of_piece(CHboard,CHsquare)
        for i in Legal_move:
            sq = i.to_square
            row2,col2 = self.chesssquare_to_XY(sq)
            ini = Square(row,col)
            final = Square(row2,col2)
            move = Move(ini,final)
            piece.add_move(move)




    def _create(self):
        for row in range(ROWS):
            for col in range(COLS) :
                self.square[row][col] = Square(row,col)

    def _add_piece(self,color) :
        row_pawn , row_other = (6,7) if color =='white'else (1,0)

        for col in range(COLS):
            self.square[row_pawn][col] = Square(row_pawn,col,Pawn(color))

        self.square[row_other][1] = Square(row_other,1,Knight(color))
        self.square[row_other][6] = Square(row_other,6,Knight(color))

        self.square[row_other][2] = Square(row_other,1,Bishop(color))
        self.square[row_other][5] = Square(row_other,6,Bishop(color))

        self.square[row_other][0] = Square(row_other,0,Rook(color))
        self.square[row_other][7] = Square(row_other,7,Rook(color))

        self.square[row_other][3] = Square(row_other,3,Queen(color))
        self.square[row_other][4] = Square(row_other,4,King(color))

    def move(self,piece,move):
        ini = move.initial
        final = move.final

        en_passant_check = True if (self.square[final.row][final.col].piece == None) else False

        #update move on console
        self.square[ini.row][ini.col].piece = None
        self.square[final.row][final.col].piece = piece





        # update modune chess board

        #Pawn Promotion
        if self.check_promotion(piece,final):
            CHmove = self.find_queen_promotion(self.CHboard.legal_moves,final)
            self.CHboard.push(CHmove)
        # Castling
        elif isinstance(piece,King) and piece.moved==False and final.row==0 and (final.col==2 and self.square[0][0].piece.moved==False) :
            CHpiece = self.CHboard.piece_at( self.XY_to_chesssquare(ini.row,ini.col) )
            CHmove = self.find_queenside_castling(self.CHboard.legal_moves,CHpiece)
            self.CHboard.push(CHmove)
            #update Rook
            self.square[0][0].piece = None
            self.square[0][3].piece = Rook(piece.color)
            self.square[0][3].piece.moved=True
        elif isinstance(piece,King) and piece.moved==False and final.row==0 and (final.col==6 and self.square[0][7].piece.moved==False):
            CHpiece = self.CHboard.piece_at(self.XY_to_chesssquare(ini.row, ini.col))
            CHmove = self.find_castling(self.CHboard.legal_moves,CHpiece)
            self.CHboard.push(CHmove)
            #update Rook
            self.square[0][7].piece = None
            self.square[0][5].piece = Rook(piece.color)
            self.square[0][5].piece.moved=True

        elif isinstance(piece,King) and piece.moved==False and final.row==7 and (final.col==2 and self.square[7][0].piece.moved==False) :
            CHpiece = self.CHboard.piece_at(self.XY_to_chesssquare(ini.row, ini.col))
            CHmove = self.find_queenside_castling(self.CHboard.legal_moves,CHpiece)
            self.CHboard.push(CHmove)
            #update Rook
            self.square[7][0].piece = None
            self.square[7][3].piece = Rook(piece.color)
            self.square[7][3].piece.moved=True
        elif isinstance(piece,King) and piece.moved==False and final.row==7 and (final.col==6 and self.square[7][7].piece.moved==False):
            CHpiece = self.CHboard.piece_at(self.XY_to_chesssquare(ini.row, ini.col))
            CHmove = self.find_castling(self.CHboard.legal_moves,CHpiece)
            self.CHboard.push(CHmove)
            #update Rook
            self.square[7][7].piece = None
            self.square[7][5].piece = Rook(piece.color)
            self.square[7][5].piece.moved=True
        #En passante
        elif isinstance(piece,Pawn) and ini.col!=final.col and en_passant_check :
            CHmove = self.find_en_passant(self.CHboard.legal_moves, ini,final)
            self.CHboard.push(CHmove)

            plus = 1 if piece.color=='white' else -1
            self.square[final.row+plus][final.col].piece = None

        # Other move
        else :
            CHmove = self.find_move(self.CHboard.legal_moves,ini,final)
            self.CHboard.push(CHmove)
            print("move : ",CHmove , " Piece: " ,self.CHboard.piece_at(self.XY_to_chesssquare(final.row,final.col)))
        print(self.CHboard.legal_moves)

        # Blit update
        piece.moved = True
        piece.moves = []
        self.last_move = move
    def valid_move(self,piece,move):
        return move in piece.moves
    def check_promotion(self,piece,final):
        if (final.row==0 or final.row==7) and isinstance(piece,Pawn)==True:
            self.square[final.row][final.col].piece = Queen(piece.color)
            return True
        return False

    def find_queen_promotion(self,moves,final):
        for move in moves:
            # Kiểm tra xem nước đi có phải là phong cấp hậu không
            if move.promotion == chess.QUEEN and move.to_square == self.XY_to_chesssquare(final.row,final.col):
                return move
        return None

    def find_queenside_castling(self,moves,piece):
        if piece.piece_type == chess.KING:
            for move in moves:
                from_square = move.from_square
                to_square = move.to_square
                if ((from_square == chess.E1 and to_square == chess.C1) or (from_square == chess.E8 and to_square == chess.C8)):
                    return move
            return None
        return None
    def find_castling(self,moves,piece):
        if piece.piece_type == chess.KING:
            for move in moves:
                from_square = move.from_square
                to_square = move.to_square
                if ((from_square == chess.E1 and to_square == chess.G1) or (from_square == chess.E8 and to_square == chess.G8)):
                    return move
            return None
        return None

    def find_en_passant(self,moves,ini,final):
        X_ini = ini.row
        Y_ini = ini.col

        X_final = final.row
        Y_final = final.col

        for move in moves:
            X1,Y1 = self.chesssquare_to_XY(move.from_square)
            X2,Y2 = self.chesssquare_to_XY(move.to_square)
            if X1==X_ini and Y1==Y_ini and X2==X_final and Y2==Y_final:
                return move
        return None
    def find_move(self,moves,ini,final):
        X_ini = ini.row
        Y_ini = ini.col

        X_final = final.row
        Y_final = final.col

        for move in moves:
            X1,Y1 = self.chesssquare_to_XY(move.from_square)
            X2,Y2 = self.chesssquare_to_XY(move.to_square)
            if X1==X_ini and Y1==Y_ini and X2==X_final and Y2==Y_final:
                return move
        return None