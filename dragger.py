import pygame
from const import *
class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.ini_row = 0
        self.ini_col = 0

    #Blit method
    def update_blit(self, surface):
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)
    #Other method
    def update_mouse(self,pos) :
        self.mouseX , self.mouseY = pos


    def save_ini(self,pos):
        self.ini_row = pos[1]//SQSIZE
        self.ini_col = pos[0]//SQSIZE

    def drag_piece(self,piece):
        self.piece = piece
        self.dragging=True

    def undrag_piece(self):
        self.piece=None
        self.dragging=False
