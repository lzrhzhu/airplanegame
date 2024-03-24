import random
import pygame
from Constant import *
from GameMemberInstance import *
from math import sin, cos, pi

class RegionTime:
    regionWidth  = 800
    regionHeight = 600
    FPS          = 60

    @classmethod
    def xPixel(cls, x_unit):
        return int( cls.regionWidth * x_unit)
    @classmethod
    def yPixel(cls, y_unit):
        return int( cls.regionHeight * y_unit)
    @classmethod
    def positionPixel(cls, x_unit, y_unit):
        return int(cls.regionWidth * x_unit),  int(cls.regionHeight * y_unit)
    @classmethod
    def displacement_per_frame(cls, vx_unit, vy_unit):
        return int(cls.regionWidth * vx_unit/cls.FPS), int(cls.regionHeight * vy_unit/cls.FPS)
    @classmethod
    def dy_per_frame(cls, vy_unit):
        return int(cls.regionHeight *vy_unit/cls.FPS)
    @classmethod
    def dx_per_frame(cls, vx_unit):
        return int(cls.regionWidth * vx_unit/cls.FPS)
    @classmethod
    def displacementonTime_speed_heading(cls, speed_unit, heading_deg):
        vx_unit = speed_unit * sin(heading_deg * pi / 180)
        vy_unit = speed_unit * cos(heading_deg * pi / 180)
        vx_pixel = vx_unit * cls.regionWidth
        vy_pixel = vy_unit * cls.regionHeight
        return vx_pixel / cls.FPS, vy_pixel / cls.FPS
# 定义补给包
class SupplyPack(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.speed = RegionTime.dy_per_frame(0.1)
        self.dy_per_frame= RegionTime.dy_per_frame(0.2) # the direction of velocity is on the y direction
        self.type = type
        if self.type == 1:  # 增加武器
            packet_image = pygame.image.load(".\game-pic/MachineGun.png").convert_alpha()
            packet_image = pygame.transform.scale(packet_image, RegionTime.positionPixel(0.05, 0.05))  # 调整图像尺寸为(50, 50)
            packet_image.set_colorkey((255, 255, 255))  # 设置白色为透明颜色
            self.image = packet_image
        elif self.type == 2:  # 增加子弹威力
            packet_image = pygame.image.load(".\game-pic/bullet.png").convert_alpha()
            packet_image = pygame.transform.scale(packet_image, RegionTime.positionPixel(0.05, 0.05))  # 调整图像尺寸为(50, 50)
            packet_image.set_colorkey((255, 255, 255))  # 设置白色为透明颜色
            self.image = packet_image
        elif self.type == 3:  # 补给包
            packet_image = pygame.image.load(".\game-pic/medicalKit.png").convert_alpha()
            packet_image = pygame.transform.scale(packet_image, RegionTime.positionPixel(0.05, 0.05))  # 调整图像尺寸为(50, 50)
            packet_image.set_colorkey((255, 255, 255))  # 设置白色为透明颜色
            self.image = packet_image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.centery += self.speed
        if pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pixel, y_pixel, heading_deg, speed_unit, power, color=Color.WHITE):
        super().__init__()
        self.x_pixel, self.y_pixel = x_pixel, y_pixel
        self.power = power
        self.color = color
        self.dx_pixel, self.dy_pixel = RegionTime.displacementonTime_speed_heading\
            (speed_unit, heading_deg)
        self.image = pygame.transform.rotate(pygame.Surface(RegionTime.positionPixel(0.005, 0.01)), heading_deg)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.x_pixel, self.y_pixel
        return
    def update(self):
        self.rect.x += self.dx_pixel
        self.rect.y += self.dy_pixel
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > RegionTime.regionHeight:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > RegionTime.regionWidth:
            self.kill()

# 定义玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed_unit = 0.5  # 以 height, width 为单位的速度
        self.bullet_level = 1
        self.bullet_power = 1
        self.bullet_speed_unit = - 0.8  # 以 height 为单位的速度
        self.displacement_pixel = RegionTime.displacement_per_frame(self.speed_unit, self.speed_unit)
        self.health = 100
        self.image = pygame.transform.scale(pygame.image.load(".\game-pic/player.png").convert_alpha(),\
                                            RegionTime.positionPixel(0.05, 0.05))  # 调整图像尺寸为(50, 50)
        self.image.set_colorkey((255, 255, 255))  # 设置白色为透明颜色
        self.rect = self.image.get_rect(center=RegionTime.positionPixel(0.5, 0.95))
        self.bullet_displacement_pixel = RegionTime.displacement_per_frame(0, self.bullet_speed_unit)[1]  # 设置以单位

    def singleBulltes_1(self):
        new_bullet = Bullet(self.rect.centerx, self.rect.top,
                            0, self.bullet_speed_unit, self.bullet_power)
        return new_bullet
    def doubleBullets_2(self):
        new_bullet1 = Bullet(self.rect.left, self.rect.top,
                             0, self.bullet_speed_unit, self.bullet_power)
        new_bullet2 = Bullet(self.rect.right, self.rect.top,
                             0, self.bullet_speed_unit, self.bullet_power)
        return [new_bullet1, new_bullet2]
    def tripleBullets_3(self):
        new_bullet1 = Bullet(self.rect.centerx, self.rect.top,
                             -8, self.bullet_speed_unit, self.bullet_power)
        new_bullet2 = Bullet(self.rect.centerx, self.rect.top,
                             0, self.bullet_speed_unit, self.bullet_power)
        new_bullet3 = Bullet(self.rect.centerx, self.rect.top,
                             8, self.bullet_speed_unit, self.bullet_power)
        return [new_bullet1, new_bullet2, new_bullet3]
    def buckshot_4(self):
        new_bullet1 = Bullet(self.rect.centerx, self.rect.top,
                             -14, self.bullet_speed_unit, self.bullet_power)
        new_bullet2 = Bullet(self.rect.centerx, self.rect.top,
                             -8, self.bullet_speed_unit, self.bullet_power)
        new_bullet3 = Bullet(self.rect.centerx, self.rect.top,
                             0, self.bullet_speed_unit, self.bullet_power)
        new_bullet4 = Bullet(self.rect.centerx, self.rect.top,
                             8, self.bullet_speed_unit, self.bullet_power)
        new_bullet5 = Bullet(self.rect.centerx, self.rect.top,
                             14, self.bullet_speed_unit, self.bullet_power)

        return [new_bullet1, new_bullet2, new_bullet3, new_bullet4, new_bullet5]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.keyMoveLeft()
        if keys[pygame.K_RIGHT]:
            self.keyMoveRight()
        if keys[pygame.K_UP]:
            self.keyMoveUp()
        if keys[pygame.K_DOWN]:
            self.keyMoveDown()
        if keys[pygame.K_SPACE]:
            self.keyFire()

        return
    def keyMoveLeft(self):
        self.rect.x -= self.displacement_pixel[0]
        if self.rect.left < 0:
            self.rect.left = 0
    def keyMoveRight(self):
        self.rect.x += self.displacement_pixel[0]
        if self.rect.right > RegionTime.regionWidth:
            self.rect.right = RegionTime.regionWidth
    def keyMoveUp(self):
        self.rect.y -= self.displacement_pixel[1]
        if self.rect.top < 0:
            self.rect.top = 0
    def keyMoveDown(self):
        self.rect.y += self.displacement_pixel[1]
        if self.rect.bottom > RegionTime.regionHeight:
            self.rect.bottom = RegionTime.regionHeight

    def keyFire(self):
        bullets = []
        if self.bullet_level == 1:
            bullets.append(self.singleBulltes_1())
        elif self.bullet_level == 2:
            bullets.append(self.doubleBullets_2())
        elif self.bullet_level == 3:
            bullets.append(self.tripleBullets_3())
        elif self.bullet_level == 4:
            bullets.append(self.buckshot_4())
        SpritesContainer.addPlayerBullets(bullets)
        return

    def hitsbyEnemies(self, enemies):
        for enemy in enemies:
            self.health -= enemy.power
        return

    def hitsbyBullets(self, bullets):
        for bullet in bullets:
            self.health -= bullet.power
        return

    def increaseSpeed(self, increase):
        self.bullet_speed_unit -= increase
        return
# 定义敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, dx_unit, dy_unit, dvx_unit, dvy_unit):
        super().__init__()
        self.fitImage()
        self.rect.centerx = random.randint(int(0.1*RegionTime.regionWidth),
                                           int(RegionTime.regionWidth*0.9))
        self.rect.centery = - RegionTime.regionHeight / 10
        self.dxPerFrame, self.dyPerFrame = RegionTime.displacement_per_frame(dx_unit, dy_unit)
        self.dvxPerFrame, self.dvyPerFrame = RegionTime.displacement_per_frame(dvx_unit, dvy_unit)
        self.health = health
        self.power = None
        return

    def update(self):
        self.dxPerFrame += self.dvxPerFrame
        self.dyPerFrame += self.dvyPerFrame
        self.rect.x     += self.dxPerFrame
        self.rect.y     += self.dyPerFrame

        if (self.rect.y > RegionTime.regionHeight
                or self.rect.x > RegionTime.regionWidth
                or self.rect.x < 0):
            self.kill()   #  从下左右三个方向运动出屏幕该飞机将移除
        self.bullet()

    def hitsby(self, bullets):
        for bullet in bullets:
            self.health -= bullet.power
            if self.health <= 0:
                self.kill()
                self.dropRewards()

    def fitImage(self):
        pass

    def bullet(self):
        pass

    def dropRewards(self):
        pass


class F16(Enemy):
    def __init__(self):
        super().__init__(1, 0, 0.6, 0, 0.05)
        self.power =10
    def bullet(self):
        return

    def fitImage(self):
        self.image =  pygame.transform.scale(\
            pygame.image.load(".\game-pic/F16.png").convert_alpha(),
            RegionTime.positionPixel(0.05, 0.05))
        self.rect = self.image.get_rect()

class F15(Enemy):
    def __init__(self):
        super().__init__(5, 0.0, 0.40, random.uniform(-0.02, 0.02), 0.03)
        self.power = 20
    def fitImage(self):
        image = pygame.transform.scale(
            pygame.image.load(".\game-pic/F15.png").convert_alpha(),
            RegionTime.positionPixel(0.05, 0.05))
        image.set_colorkey((255, 255, 255))
        self.image = image
        self.rect = self.image.get_rect()

    def bullet(self):
        return


class F22(Enemy):
    def __init__(self):
        super().__init__(20, 0.0, 0.2, 0.00, 0.01)
        self.timeCount = 0
        self.enemiesBullets = SpritesContainer.enemiesBullets
        self.game_spirits   = SpritesContainer.gameSprites
        self.power = 30
    def fitImage(self):
        image = pygame.image.load(".\game-pic/F22.png").convert_alpha()
        image = pygame.transform.scale(image, (40, 40))
        image.set_colorkey((255, 255, 255))
        self.image = image
        self.rect = self.image.get_rect()

    def bullet(self):
        if self.alive() == False:
            return
        self.timeCount += 1
        timeDuration = self.timeCount / RegionTime.FPS
        bullets = []
        if timeDuration > 2:
            self.timeCount = 0
            for i in range(0, 5):
                bullet = Bullet(self.rect.centerx, self.rect.top,
                                random.uniform(-90, 90.0), 0.3, 1, Color.RED)
                bullets.append(bullet)
        SpritesContainer.addEnemiesBullets(bullets)

    def dropRewards(self):
        packetEvent = pygame.event.Event(GameEvent.PACKET_EVENT, {})
        packetEvent.attr1 = self.rect.centerx
        packetEvent.attr2 = self.rect.centery
        pygame.event.post(packetEvent)

class BOSS_C1(Enemy):
    def __init__(self):
        super().__init__(3000, 0.0, 0.03, 0.00, 0.00)
        self.rect.centery = RegionTime.regionHeight/10
        self.bullets = SpritesContainer.enemiesBullets
        self.spirits = SpritesContainer.gameSprites
        self.timeCount = 0

    def fitImage(self):
        B = pygame.image.load(".\game-pic/BOSS_C1.png").convert_alpha()
        B = pygame.transform.scale(B, RegionTime.positionPixel(0.1, 0.1))
        B.set_colorkey((255, 255, 255))
        self.image = B
        self.rect = self.image.get_rect()

    def bullet(self):
        if self.alive() == False:
            return
        self.timeCount += 1
        timeDuration = self.timeCount / RegionTime.FPS
        bullets = []
        if timeDuration > 0.5:
            self.timeCount = 0
            for i in range(0, 50):  # 发射50发子弹
                bullets.append(Bullet(self.rect.centerx, self.rect.top, \
                                      random.uniform(-90, 90.0), \
                                      0.3, 1, Color.RED))
        SpritesContainer.addEnemiesBullets(bullets)
        return

    def dropRewards(self):
        pass_c1 = pygame.event.Event(GameEvent.CLEAR_BOSS_C1, {})
        pygame.event.post(pass_c1)
        return

def Generate_0_20(count):
    # 每秒两架 F16
    enemies = [F16(), F16(), F16()]
    if count % 2 == 0:  # 2秒1架F15
        enemies.append(F15())
    if count % 4 == 0:  # 4秒1加F22
        enemies.append(F22())
    SpritesContainer.addEnemies(enemies)
    return


def Generate_20_50(count):
    enemies = [F16(), F16(), F16(), F16(), F16()]  # 每秒5架F16
    if count % 2 == 0:  # 3秒1架F15
        enemy = F15()
        enemies.append(enemy)
    # 5秒1架F22
    if count % 8 == 0:
        enemy = F22()
        enemies.append(enemy)
    SpritesContainer.addEnemies(enemies)

def Generate_50_60(count):
    SpritesContainer.addEnemies([F22(), F22()])
    return

def Generate_BOSS_C1():
    SpritesContainer.addEnemies(BOSS_C1())


def Generate_Packet(x, y):
    rv = random.uniform(0.0, 1.0)
    property = None
    if rv < 0.6:
        property = 1
    elif rv < 0.8:
        property = 2
    else:
        property = 3
    SpritesContainer.addPackets(SupplyPack(x, y, property))
    return


def generateEnemyOnTime(timeCount):
    if timeCount <= 20:
        Generate_0_20(timeCount)
    if 20 < timeCount <= 50:
        Generate_20_50(timeCount)
    if 50 < timeCount <= 60:
        Generate_50_60(timeCount)
    if timeCount == 65:
        Generate_BOSS_C1()
    return

class GameSurface(pygame.Surface):
    def __init__(self):
        super().__init__((RegionTime.regionWidth,RegionTime.regionHeight))
        self.game_area_background = pygame.transform.scale(
            pygame.image.load(".\game-pic/background.png"), (RegionTime.regionWidth, RegionTime.regionHeight))
        return
