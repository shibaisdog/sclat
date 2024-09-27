import pygame
load = 0 # 0 = choice / 1 = download / 2 = play
win,font,vid = None,None,None
def reset(size):
    global win,font
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode(size, pygame.RESIZABLE)
    font = pygame.font.Font(None, 25)