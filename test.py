import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 定义生命条的颜色、尺寸和位置
BAR_LENGTH = 200
BAR_HEIGHT = 30
BAR_POSITION = (0, 0)  # 生命条在其 Surface 对象上的位置

# 定义颜色常量
GREEN = (0,   255, 0  )
RED   = (255,   0, 0  )
BLACK = (0,     0, 0  )
YELLOW= (0,   255, 255)
WHITE = (255, 255, 255)
def draw_health_bar(health_surface, health_pct):
    if health_pct > 0.8:
        bar_color = GREEN
    elif health_pct > 0.3:
        bar_color = YELLOW
    else:
        bar_color = RED

    # 绘制生命条背景
    background_rect = pygame.Rect(BAR_POSITION[0], BAR_POSITION[1], BAR_LENGTH, BAR_HEIGHT)
    health_surface.fill(BLACK)  # 填充生命条 Surface 的背景色

    # 绘制生命条前景
    health_length = int(BAR_LENGTH * health_pct)
    health_rect = pygame.Rect(BAR_POSITION[0], BAR_POSITION[1], health_length, BAR_HEIGHT)
    pygame.draw.rect(health_surface, bar_color, health_rect)

    # 绘制生命值文本
    font = pygame.font.Font(None, 24)
    text = font.render(f'{int(health_pct * 100)}%', True, WHITE)
    health_surface.blit(text, (BAR_LENGTH + 10, 0))

# 创建生命条的 Surface 对象
health_surface = pygame.Surface((BAR_LENGTH + 50, BAR_HEIGHT))
health_surface_rect = health_surface.get_rect(topleft=(50, 50))  # 生命条在屏幕上的位置

# 设置初始生命值百分比
health_pct = 1.0
FPS = 10
running = True
while running:
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充屏幕背景
    screen.fill(WHITE)

    # 绘制生命条到它的 Surface 上
    draw_health_bar(health_surface, health_pct)

    # 将生命条的 Surface 绘制到主屏幕上
    screen.blit(health_surface, health_surface_rect.topleft)

    # 更新屏幕显示
    pygame.display.flip()

    # 这里是模拟生命值变化的代码，实际游戏中应该根据游戏逻辑来更新生命值
    health_pct -= 0.01
    if health_pct < 0:
        health_pct = 0

pygame.quit()
sys.exit()