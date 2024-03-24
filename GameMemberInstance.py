import pygame
class SpritesContainer:
    gameSprites = []
    enemies = []
    playerBullets = []
    enemiesBullets = []
    packets = []
    player  = None
    @classmethod
    def init(cls, player):
        cls.gameSprites    = pygame.sprite.Group()
        cls.enemies        = pygame.sprite.Group()
        cls.playerBullets  = pygame.sprite.Group()
        cls.enemiesBullets = pygame.sprite.Group()
        cls.packets        = pygame.sprite.Group()
        cls.player         = player
        cls.gameSprites.add(player)
        return

    @classmethod
    def addEnemies(cls, enemies):
        cls.enemies.add(enemies)
        cls.gameSprites.add(enemies)
        return
    @classmethod
    def addPlayerBullets(cls, bullets):
        cls.playerBullets.add(bullets)
        cls.gameSprites.add(bullets)
        return
    @classmethod
    def addEnemiesBullets(cls, bullets):
        cls.enemiesBullets.add(bullets)
        cls.gameSprites.add(bullets)
        return
    @classmethod
    def addPackets(cls, packets):
        cls.packets.add(packets)
        cls.gameSprites.add(packets)
        return