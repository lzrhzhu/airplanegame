import time
import pygame
from StatusSurface import *
from GameMemberClass import *
from GameMemberInstance import *

pygame.init()   # 初始化pygame
# 设置全屏模式
screen_info = pygame.display.Info()  # 获取当前屏幕的宽高
screen      = pygame.display.set_mode((screen_info.current_w, screen_info.current_h),\
                                      pygame.FULLSCREEN)
status_game_ratio = 0.4  # 假设状态区域占40%，游戏区占60%
FPS               = 60   # 帧率为60

# 计算状态显示区域和游戏区域的宽度
status_Width = int(screen_info.current_w * status_game_ratio)
game_Width   = screen_info.current_w - status_Width
Height       = screen_info.current_h

#设置GameSurface 长度和时间转换的标准
RegionTime.regionWidth = game_Width
RegionTime.regionHeight= Height
RegionTime.FPS         = FPS

# 游戏开始时间
startTime = pygame.time.get_ticks()
# 创建状态区
statusSurface = StatusSurface(status_Width, Height, startTime)
# 创建游戏区 surface
gameSurface = GameSurface()
#设置背景音乐
#background_music = pygame.mixer.Sound('background_music.wav')
#collision_sound = pygame.mixer.Sound('collision_sound.wav')

# 游戏时间限制（秒）
game_duration = 60
pygame.time.set_timer(GameEvent.TIME_EVENT, 1000)  # 设置定时器事件每秒触发一次，

def GameOver():
    text = pygame.font.Font(None, 102).render('Game Over', True, (255, 0, 0))
    text_rect = text.get_rect(center=(400, 300))
    # 将文字显示在屏幕上
    screen.blit(text, text_rect)
    pygame.display.flip()
    # 等待5秒后退出程序
    time.sleep(5)
    pygame.quit()
def Win():
    text = pygame.font.Font("C:\Windows\Fonts/FRSCRIPT.TTF", 102).\
        render('Game Win', True, (255, 0, 0))
    text_rect = text.get_rect(center=(400, 300))
    # 将文字显示在屏幕上
    screen.blit(text, text_rect)
    pygame.display.flip()
    # 等待5秒后退出程序
    time.sleep(5)
    pygame.quit()

SpritesContainer.init(Player())

# 游戏循环标志
running = True
timeCount = 0
# 游戏循环
while running:
    # 保持游戏以恒定速度运行
    pygame.time.Clock().tick(FPS)
    screen.fill(Color.BLACK)
    # 事件处理
    for event in pygame.event.get():
        if event.type==GameEvent.TIME_EVENT:
            generateEnemyOnTime(timeCount)
            timeCount += 1
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == GameEvent.PACKET_EVENT:
            Generate_Packet(int(event.attr1), int(event.attr2) )
        if event.type == GameEvent.CLEAR_BOSS_C1:
            Win()
    # 更新所有精灵
    SpritesContainer.gameSprites.update()

    # 检查子弹是否击中敌人
    collisions = pygame.sprite.groupcollide(SpritesContainer.enemies, SpritesContainer.playerBullets, False, True)
    for enemy in collisions.keys():
        # 获得与键碰撞的所有值
        bullets = collisions[enemy]
        enemy.hitsby(bullets)
    # 检查玩家是否撞到敌人
    hitByEnemies = pygame.sprite.spritecollide(SpritesContainer.player, SpritesContainer.enemies, True)
    if(len(hitByEnemies)>0):
        SpritesContainer.player.hitsbyEnemies(hitByEnemies)
    hitByBullets = pygame.sprite.spritecollide(SpritesContainer.player, SpritesContainer.enemiesBullets, True)
    if(len(hitByBullets)>0):
        SpritesContainer.player.hitsbyBullets(hitByBullets)
    if(SpritesContainer.player.health<=0):
        GameOver()
    # 检查玩家是否获得补给包
    collisions = pygame.sprite.spritecollide(SpritesContainer.player, SpritesContainer.packets, True)
    for packet in collisions:
        if packet.type ==1:
            SpritesContainer.player.bullet_level+=1
        elif packet.type ==2:
            SpritesContainer.player.bullet_power+=1
        elif packet.type ==3:
            SpritesContainer.player.health += 20
    if SpritesContainer.player.bullet_level > 4:
        SpritesContainer.player.bullet_level=4


    gameSurface.blit(gameSurface.game_area_background,(0,0))
    statusSurface.blit(statusSurface.healthBar,statusSurface.healthBarPos)
    # 绘制所有精灵
#    SpritesContainer.gameSprites.clear(gameSurface,gameSurface.game_area_background)

    statusSurface.update()
    SpritesContainer.gameSprites.draw(gameSurface)
    screen.blit(gameSurface,(status_Width,0))
    screen.blit(statusSurface,(0, 0))

    pygame.display.flip()