import pygame.font

class Button():
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width,self.height = 200, 50#按钮宽高
        self.button_color = (0, 255, 0)#绿色按钮
        self.text_color = (255, 255, 255)#白色文字
        # 默认字体 48号字号
        self.font = pygame.font.SysFont(None,48)
        # 创建按钮rect对象，使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)
    def prep_msg(self, msg):
        # 将字符串文本渲染为图片，并将位置居中
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)