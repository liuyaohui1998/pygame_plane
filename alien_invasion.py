import sys #system
import pygame 
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

# 音乐的路径
file=r'music\bg_music.mp3'
# 初始化
pygame.mixer.init()
# 加载音乐文件
track = pygame.mixer.music.load(file)
# 开始播放音乐流
pygame.mixer.music.play()

def run_game(): 
    # 初始化游戏并创建一个屏幕对象
    pygame.init() #调用init方法 游戏初始化
    ai_settings = Settings()
    # 创建一个屏幕对象
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建ship对象，将屏幕对象作为参数传入
    ship = Ship(ai_settings,screen)
    # 创建子弹编组对象
    bullets = Group()
    # 创建一个外星人对象
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)
    
    
    
    # 开始游戏的主循环
    while True: 
        # 事件驱动：监视键盘和鼠标事件
        # 循环检查所获取的所有事件（鼠标点击、键盘动作）
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        # 刷新屏幕
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
        
run_game()