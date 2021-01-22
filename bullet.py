import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__ (self,ai_settings,screen,ship):
        super(Bullet,self).__init__()
        self.screen = screen
        # 创建子弹图片
        self.image = pygame.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 子弹横向位置在飞船中心
        self.rect.centerx = ship.rect.centerx
        # 子弹的顶端与飞船顶端对齐
        self.rect.top = ship.rect.top
        # 子弹的纵坐标（浮点数）中间变量，修改后再赋值回去
        self.y = float(self.rect.y)

        # self.color = ai_settings.bullet_color#子弹颜色  
        self.speed_factor = ai_settings.bullet_speed_factor#子弹速度

    def update(self):#子弹运动
        # 浮点数类型的中间变量
        self.y -= self.speed_factor
        self.rect.y = self.y
    
    def blitme(self):#将子弹绘制在screen上
        
        self.screen.blit(self.image,self.rect)