import pygame
from Constant import *
from GameMemberInstance import *

class ClockDisplay(pygame.Surface):
    def __init__(self,  region, startTime):
        super().__init__(region)
        self.start_time = startTime
        self.font = pygame.font.Font("C:\Windows\Fonts/times.ttf", 54)
        self.image = pygame.Surface(region)
        return

    def update(self):
        self.fill(Color.GRAY)
        nowTime = pygame.time.get_ticks()
        time = max(0,  (nowTime-self.start_time)// 1000)
        text = self.font.render("Time:          " + str(time) + "s", True, Color.RED)
        # 绘制文本
        self.blit(text, (0, self.get_rect().height/2-text.get_rect().height/2))
        return
class HealthBar(pygame.Surface):
    def __init__(self, region):
        super().__init__(region)
        self.health_pct = 1
        self.width  = self.get_width()
        self.height = self.get_height()
        self.health_length = int(self.width * self.health_pct)
        self.barColor = Color.GREEN
        self.font = pygame.font.Font("C:\Windows\Fonts/times.ttf", 72)
        self.plot()
    def update(self):
        self.health_pct = SpritesContainer.player.health/100
        #重新计算血条颜色
        if self.health_pct > 0.8:
            self.barColor = Color.GREEN
        elif self.health_pct > 0.3:
            self.barColor = Color.YELLOW
        else:
            self.barColor = Color.RED
        self.health_length = self.width * self.health_pct     # 重新计算血条长度
        self.plot()
    def plot(self):
        #绘制背景
        self.background_surface = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.background_surface.fill(Color.BLACK)
        #绘制前景
        self.front_surface = pygame.Surface((int(self.width* self.health_pct), self.height))
        self.front_surface.fill(self.barColor)
        #绘制字体
        self.health_text_surface = self.font.render(f'{int(self.health_pct * 100)}%', \
                                            True, Color.WHITE)
        self.blit(self.background_surface, (0,0))
        self.blit(self.front_surface,(0,0))

        pos =  (self.width/2.0 - self.health_text_surface.get_width()/2,
                self.height/2-self.health_text_surface.get_height()/2)

        self.blit(self.health_text_surface,  pos)


# class WeaponBar(pygame.Surface):


class StatusSurface(pygame.Surface):
    def __init__(self, width, height, startTime):
        super().__init__((width, height))
        self.width  = width
        self.height = height
        self.player = SpritesContainer.player
        self.clockDisplayPos = self.unit_to_pixel(0, 0.05)
        self.healthBarPos    = self.unit_to_pixel(0,0.17)

        self.clockDisplay    = ClockDisplay(self.unit_to_pixel(0.95, 0.1),startTime)
        self.healthBar       = HealthBar(self.unit_to_pixel(0.95, 0.1))


    def unit_to_pixel(self, x_unit, y_unit):
        return x_unit * self.width,  y_unit *self.height
    def update(self):
        # 更新状态显示
        self.fill(Color.BLACK)
        self.healthBar.update()
        self.clockDisplay.update()

        self.blit(self.healthBar, self.healthBarPos)
        self.blit(self.clockDisplay, self.clockDisplayPos)


#class statusContainer