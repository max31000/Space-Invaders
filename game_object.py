#!/usr/bin/env python3

from pygame.rect import Rect
import config


class GameObject:
    """
    Основной класс, от которого наследуются все игровые объекты
    """
    def __init__(self, x, y, w, h, speed=(0, 0)):
        self.bounds = Rect(x, y, w, h)
        self.speed = speed
        self.is_dead = False
        self.move_error = (0.0, 0.0)

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def center_x(self):
        return self.bounds.centerx

    @property
    def center_y(self):
        return self.bounds.centery

    def draw(self, surface):
        """
        draw this in surface
        :param surface:
        pygame.display
        :return:
        void
        """
        pass

    def kill(self):
        self.is_dead = True

    def move(self, dx, dy):
        """
        move this to (dx, dy)
        :param dx:
        double
        :param dy:
        double
        :return:
        void
        """
        dxy = (round(dx + self.move_error[0]), round(dy + self.move_error[1]))
        self.move_error = (dx + self.move_error[0] - dxy[0], dy + self.move_error[1] - dxy[1])
        self.bounds = self.bounds.move(*dxy)

    def update(self):
        """
        calc next position and move
        :return:
        void
        """
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)

    def is_collided_with(self, sprite):
        """
        True if this collide with sprite
        :param sprite:
        GameObject
        :return:
        bool
        """
        return self.bounds.colliderect(sprite.bounds)
