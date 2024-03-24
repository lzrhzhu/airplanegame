import pygame
class Color():
    GREEN = (0,   255, 0  )
    RED   = (255,   0, 0  )
    BLACK = (0,     0, 0  )
    YELLOW= (255, 255, 0  )
    WHITE = (255, 255, 255)
    GRAY  = (128, 128, 128)

class GameEvent:
    # 设置定时器事件
    TIME_EVENT    = pygame.USEREVENT + 10

    #  产生补给包事件
    PACKET_EVENT  = pygame.USEREVENT + 100

    #通关C1事件
    CLEAR_BOSS_C1 = pygame.USEREVENT + 101


