import pygame
from pygame import Rect
import config


def replace_pixels(texture_replace, old_color, new_color):
    for i in range(texture_replace.get_height()):
        for j in range(texture_replace.get_width()):
            if texture_replace.get_at((j, i)) == old_color:
                texture_replace.set_at((j, i), new_color)


pygame.init()
pygame.display.set_mode((config.width, config.height))
texture = pygame.image.load("textures/all_sprites.png").convert()
replace_pixels(texture, (0, 128, 255, 255), config.colors['black'])

magic_ship = texture.subsurface(Rect(2, 4, 16, 7))
replace_pixels(magic_ship, (255, 255, 255, 255), config.colors['pink'])
magic_ship = pygame.transform.scale(magic_ship, (config.bonus_ship_width, config.bonus_ship_height))

enemy_10 = texture.subsurface(Rect(21, 3, 12, 8))
replace_pixels(enemy_10, (255, 255, 255, 255), config.colors['light-blue'])
enemy_10 = pygame.transform.scale(enemy_10, (config.enemy_width, config.enemy_height))

enemy_20 = texture.subsurface(Rect(50, 3, 12, 8))
replace_pixels(enemy_20, (255, 255, 255, 255), config.colors['light-green'])
enemy_20 = pygame.transform.scale(enemy_20, (config.enemy_width, config.enemy_height))

enemy_30 = texture.subsurface(Rect(77, 3, 12, 8))
replace_pixels(enemy_30, (255, 255, 255, 255), config.colors['pink'])
enemy_30 = pygame.transform.scale(enemy_30, (config.enemy_width+1, config.enemy_height))

dead = texture.subsurface(Rect(103, 3, 12, 8))
dead = pygame.transform.scale(dead, (config.enemy_width-3, config.enemy_height-2))

texture_dict = {10: enemy_10,
                20: enemy_20,
                30: enemy_30,
                300: magic_ship,
                "dead": dead}

