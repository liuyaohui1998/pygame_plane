import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        # 初始化飞船，并设置其起始位置
        super(Ship,self).__init__()
        # 使飞船对象拥有screen属性
        self.screen = screen
        # 将游戏设置参数作为ship对象的属性
        self.ai_settings = ai_settings
    # 加载飞船图像
        self.image = pygame.image.load('images/ship.png')
    # 飞船外接矩形rectangle
        self.rect = self.image.get_rect()
    # 屏幕screen的外接矩形
        self.screen_rect = screen.get_rect()

    # 飞船初始位置：横向居中，纵向底部对齐
    # 飞船矩形中心点横坐标x = 窗口中心横坐标x
        self.rect.centerx = self.screen_rect.centerx
    # 飞船矩形底部纵坐标y = 窗口底部纵坐标y
        self.rect.bottom = self.screen_rect.bottom
    # 在飞船的属性center中存储小数值
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.bottom)
    # 飞船正在向右移动的标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
# 在指定位置绘制飞船    
    def blitme(self):
        self.screen.blit(self.image , self.rect)

# 飞船移动函数
    def update(self): 
        # 当飞船正在向右移动，并且飞船右边界小于窗口右边界
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        # 当飞船正在向左移动，并且飞船左边界小于窗口左边界（0）
        elif self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
            # 飞船上下移动
        elif self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
            
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
    
    def center_ship(self):
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom-25