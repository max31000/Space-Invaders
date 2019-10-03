from game_object import GameObject
import pygame
from pygame import Rect
import config


class Interface(GameObject):
    def __init__(self, x, y, w, h, mode, color=config.colors['green'], font_size=24, speed=(0, 0)):
        """
        Init Interface object
        :param x:
        left-top angle x pos
        :param y:
        left-top angle y pos
        :param w:
        width
        :param h:
        height
        :param mode:
        String:
        "line", "text"
        :param speed:
        not used
        """
        self.bounds = Rect(x, y, w, h)
        self.speed = speed
        self.is_text = mode is "text"
        self.is_line = mode is "line"
        self.color = color
        if self.is_text:
            self.font = pygame.font.Font('fonts/joystix monospace.ttf', font_size)
            self.text = self.font.render("", 1, config.colors["blue"])
        self.is_dead = False
        self.move_error = (0.0, 0.0)

    def draw(self, surface):
        if self.is_text:
            surface.blit(self.text, (self.left, self.top))
        elif self.is_line:
            pygame.draw.rect(surface, self.color, self.bounds)

    def set_text(self, text):
        self.text = self.font.render(text, 1, self.color)
