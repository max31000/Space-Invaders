from game_object import GameObject
import pygame
import config
from pygame import Rect
from bullet import Bullet
import logic
import random
import textures


class Enemy(GameObject):
    """
    Описание одного врага
    """
    def __init__(self, x, y, w, h, speed=(0, 0), enemy_id=0, cost=0, color=config.colors['white']):
        """
        Enemy class constructor
        :param x:
        int
        horizontal left-top angle position of enemy
        :param y:
        int
        vertical left-top angle position of enemy
        :param w:
        enemy width
        :param h:
        enemy height
        :param speed:
        2-elements speed vector (x, y)
        :param enemy_id:
        int
        id num (now don't used)
        :param cost:
        int
        cost for kill
        """
        self.bounds = Rect(x, y, w, h)
        self.is_dead = False
        self.can_shoot = False
        self.id = enemy_id
        self.cost = cost
        self.speed = speed
        self.move_error = (0.0, 0.0)
        self.reload_timer = config.enemy_reload_time // 4
        random.seed()
        self.recreation = config.enemy_recreation
        self.death_timer = -1
        self.color = color
        self.texture = textures.texture_dict[cost]

    def shooting(self, game_objects):
        """
        shoot to down
        :param game_objects:
        Objects
        :return:
        void
        """
        if not self.can_shoot:
            return

        if self.reload_timer > 0:
            self.reload_timer -= 1
            return

        if random.randint(1, config.enemy_shoot_chance) != 1:
            self.reload_timer = config.enemy_reload_time
            return

        self.reload_timer = config.enemy_reload_time
        bullet = Bullet(self.center_x - config.bullet_width / 2,
                        self.bottom + config.bullet_height,
                        config.colors['green'],
                        (0, config.bullet_speed))
        game_objects.add(bullet)

    def kill(self):
        self.texture = textures.texture_dict['dead']
        self.can_shoot = False
        self.death_timer = config.death_timer

    def draw(self, surface):
        surface.blit(self.texture, (self.bounds.x, self.bounds.y))

    def move(self, dx, dy):
        if self.death_timer > 0:
            self.death_timer -= 1

        if self.death_timer == 0:
            self.is_dead = True

        dxy = (round(dx + self.move_error[0]), round(dy + self.move_error[1]))
        self.move_error = (dx + self.move_error[0] - dxy[0], dy + self.move_error[1] - dxy[1])
        self.bounds = self.bounds.move(*dxy)

    def check_collision(self, game_objects):
        """
        suicide if in collision
        :param game_objects:
        list(GameObject)
        :return:
        void
        """
        logic.check_collision(self, game_objects)
