from game_object import GameObject
import pygame
import config
from pygame.rect import Rect
from bullet import Bullet


class Player(GameObject):
    def __init__(self, x, y, w, h, health=3, speed=(0, 0)):
        """
        :param x:
        int
        :param y:
        int
        :param w:
        int
        width collider
        :param h:
        width collider
        :param health:
        int
        player health
        :param speed:
        2-el vec (x, y)
        """
        self.bounds = Rect(x, y, w, h)
        self.speed = config.player_speed
        self.to_left = False
        self.to_right = False
        self.is_dead = False
        self.health = health
        self.move_error = (0.0, 0.0)
        self.reload_timer = 0
        self.texture = pygame.image.load("textures/player.png").convert()
        self.texture = pygame.transform.scale(self.texture, (self.bounds.width, self.bounds.height))

    def draw(self, surface):
        #pygame.draw.rect(surface, config.colors['green'], self.bounds)
        surface.blit(self.texture, (self.bounds.x, self.bounds.y))

    def handle_go(self, key):
        """
        Start move player
        :param key:
        pygame.K_LEFT or pygame.K_RIGHT
        :return:
        void
        """
        if key == pygame.K_LEFT:
            self.to_left = True
        else:
            self.to_right = True

    def handle_stop(self, key):
        """
        Stop moving player
        :param key:
        pygame.K_LEFT or pygame.K_RIGHT
        :return:
        void
        """
        if key == pygame.K_LEFT:
            self.to_left = False
        else:
            self.to_right = False

    def shooting(self, game_objects):
        """
        shoot to up from player
        :param game_objects:
        Objects
        :return:
        void
        """
        if self.reload_timer > 0:
            self.reload_timer -= 1
            return
        self.reload_timer = config.reload_time
        bullet = Bullet(self.center_x - config.bullet_width / 2,
                        self.top - config.bullet_height,
                        config.colors['yellow'],
                        (0, -config.bullet_speed))
        game_objects.add(bullet)

    def update(self):
        if self.reload_timer > 0:
            self.reload_timer -= 1

        if self.to_left:
            dx = -(min(self.speed, self.left))
        elif self.to_right:
            dx = min(self.speed, config.width - self.right)
        else:
            return
        self.move(dx, 0)
