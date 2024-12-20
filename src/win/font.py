import pygame

List = {}

def get(size:int):
    if not (str(size) in List):
        try:
            List[str(size)] = pygame.font.Font("./asset/NanumBarunpenB.ttf", size)
        except FileNotFoundError:
            List[str(size)] = pygame.font.Font(None, size)
    return List[str(size)]