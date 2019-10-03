from game_object import GameObject
import pygame
import config


class Tower(GameObject):
    def draw(self, surface):
        pygame.draw.polygon(surface, config.colors['red'], ((self.left, self.top),
                                                            (self.left, self.bottom),
                                                            (self.left + 14, self.bottom),
                                                            (self.left + 14,
                                                             max(self.bottom - 1.2 * config.enemy_height, self.top)),
                                                            (self.right - 14,
                                                             max(self.bottom - 1.2 * config.enemy_height, self.top)),
                                                            (self.right - 14, self.bottom),
                                                            (self.right, self.bottom),
                                                            (self.right, self.top)))

    def kill(self):
        pass
