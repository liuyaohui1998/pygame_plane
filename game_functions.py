import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from gamebackgroud import GameBackground


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:#保持向右移动
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True   
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen ,ship ,bullets)
    elif event.key == pygame.K_q: 
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT: 
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):#检查事件
    for event in pygame.event.get(): 
        # 如果事件的类型（type）是“退出”
        if event.type == pygame.QUIT: 
            # 中断进程，退出程序
            sys.exit()
        # pygame.KEYDOWN 键盘上有键被按下去了 
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets) 
        # 当右键抬起来的时候，使飞船停止向右移动
        elif event.type == pygame.KEYUP: 
            check_keyup_events(event, ship)
        # 响应鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
        # 使screen填充bg_color
        # screen.fill(ai_settings.bg_color)
        bgimg = pygame.image.load("images/bg.jpg")
        screen.blit(bgimg,(0,0))
        
        # 绘制飞船
        ship.blitme()
        #在飞船和外星人后面重绘子弹
        for bullet in bullets.sprites():
            bullet.blitme()
        # 绘制外星人群
        aliens.draw(screen)
        sb.show_score()
        # 如果游戏处于非活动状态，就绘制play按钮
        if not stats.game_active:
            play_button.draw_button()
        # 刷新屏幕
        pygame.display.flip() 
        
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
        # 删除已经消失的子弹
    for bullet in bullets.copy(): 
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet) 
        # print(len(bullets))
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
    

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values(): 
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen ,ship ,bullets):
    
    # 添加发射音效
    pygame.mixer.init()
    sound = pygame.mixer.Sound('music/bm.wav')
    sound.play()

    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings,screen,ship)
            # 把子弹加入到编组当中
            bullets.add(new_bullet)
    

# 计算外星人的个数
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width #水平有效空间
    number_aliens_x = int(available_space_x / (2 * alien_width))#水平可容纳外星人数
    return number_aliens_x

# 计算生成外星人的行数
def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y / (4 * alien_height))
    return number_rows

# 生成单个外星人
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 生成一个alien对象
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    # 计算alien的水平位置
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    # 将alien加入编组
    aliens.add(alien)

def create_fleet(ai_settings, screen,ship, aliens):
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
        # 改变外星人舰队水平左右方向
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 检测外星人和飞船之间碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)

    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break

def check_high_score(stats, sb):
    # 检查是否诞生了新得最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()





        

