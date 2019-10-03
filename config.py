width = 462
height = 528
player_height = 16
player_width = 26
bullet_height = 20
bullet_width = 3
bullet_speed = 6
enemy_width = 28
enemy_height = 19
enemy_border = 11
enemy_recreation = 20
fps = 60
reload_time = 22
enemy_shoot_chance = 4
army_lines = 5
towers_count = 4
towers_width = 65
tower_height = enemy_height * 2
down_field = 46
tower_top = height - tower_height - player_height - (enemy_height + enemy_border) - down_field
army_columns = 11
enemy_reload_time = 45
colors = {'white': (255, 255, 255),
          'black': (0, 0, 0),
          'green': (0, 255, 0),
          'light-green': (80, 255, 40),
          'orange': (255, 120, 0),
          'blue': (0, 0, 255),
          'pink': (255, 0, 255),
          'red': (255, 0, 0),
          'yellow': (255, 255, 0),
          'grey': (150, 150, 150),
          'light-blue': (0, 255, 255)}
player_speed = 2.5
enemy_speed = (5, 0)
up_border_field = 32
down_border_field = height - down_field + 16
death_timer = 8
bonus_ship_cooldown = 1000
bonus_ship_height = enemy_height
bonus_ship_width = enemy_width * 2
