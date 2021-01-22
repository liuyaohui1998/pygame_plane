# 创建类Settings
# 类名首字母大写
class Settings():
    # init 左右各有两个下划线
    # __init__,构造函数
    # 当Settings类初始化为对象
    # self 指对象本身
    def __init__(self):
        self.screen_width = 480
        self.screen_height = 800
        self.bg_color = (230,230,230)   
        self.ship_limit = 3
        

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 10#最多存在十发子弹

        self.fleet_drop_speed = 10
        
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        # 重置动态设置
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 1
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        self.alien_points = 50
    
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
