import pygame
import Button
import main_PvsAI
import main_PvP
import main_AIvAI

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 550

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("CHESS MENU")

font = pygame.font.SysFont("arialblack", 60)
TEXT_COL = (255,255,255)


Ok_img = pygame.image.load("main.png").convert_alpha()
Ok_button1 = Button.Button(500,200,Ok_img,0.35)
Ok_button2 = Button.Button(500,310,Ok_img,0.35)
Ok_button3 = Button.Button(500,420,Ok_img,0.35)

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True , text_col)
    screen.blit(img,(x,y))

Runn = True
while Runn:
    screen.fill((52,78,91))

    if   Ok_button1.draw(screen) :
        main = main_PvP.Main()
        main.mainloop()
    elif Ok_button2.draw(screen) :
        main = main_PvsAI.Main()
        main.mainloop()
    elif Ok_button3.draw(screen) :
        main = main_AIvAI.Main()
        main.mainloop()

    draw_text("Please choose the game mode", pygame.font.SysFont("arialblack", 40), TEXT_COL, 100, 100)
    draw_text("PvP",font,TEXT_COL,200,200)
    draw_text("PvAI", font, TEXT_COL, 200, 310)
    draw_text("AIvAI", font, TEXT_COL, 200, 420)

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            Runn = False
    pygame.display.update()

pygame.quit()
