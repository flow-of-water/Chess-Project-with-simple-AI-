class Square :

    def __init__(self,row ,col, piece=None):
        self.row=row
        self.col=col
        self.piece = piece

    def has_piece(self):
        return self.piece!=None

    def __eq__(self,other):
        return (self.row == other.row and self.col == other.col)

    @staticmethod
    def getAlphaCol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]
