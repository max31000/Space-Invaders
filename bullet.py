from game_object import GameObject
import pygame
import config
import logic


class Bullet(GameObject):
    def __init__(self, x, y, color, speed=(0, 0)):
        """
        Bullet constructor
        :param x:
        int
        horizontal left-top angle position of bullet
        :param y:
        int
        vertical left-top angle position of bullet
        :param color:
        3-elements RGB vector (R, G, B)
        :param speed:
        2-elements speed vector (x, y)
        """
        self.bounds = pygame.Rect(x, y,
                                  config.bullet_width,
                                  config.bullet_height)
        self.speed = speed
        self.is_dead = False
        self.color = color
        self.move_error = (0.0, 0.0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def update(self):
        self.is_dead = self.is_dead or logic.is_out_side(self)
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)
