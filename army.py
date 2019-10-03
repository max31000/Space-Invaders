from game_object import GameObject
from pygame import Rect
import config
from enemy import Enemy
import logic
import random
import pygame


class Army(GameObject):
    """
    Enemy armada class
    """
    def __init__(self, enemy_w, enemy_h,
                 army_lines, army_columns,
                 x, y,
                 speed=(0, 0)):
        """
        Army constructor
        :param enemy_w:
        int
        enemy width
        :param enemy_h:
        int
        enemy height
        :param army_lines:
        int
        number of enemy lines
        :param army_columns:
        int
        number of enemy columns
        :param x:
        int
        horizontal left-top angle position of armada
        :param y:
        int
        vertical left-top angle position of armada
        :param speed:
        two-arg speed vector (x, y)
        """
        self.bounds = Rect(x, y,
                           (enemy_w + enemy_w // 4) * army_columns,
                           (enemy_h + enemy_h // 4) * army_lines)
        self.is_dead = False
        self.to_left = False
        self.to_right = True
        self.border = config.enemy_border
        self.enemies = [[Enemy(self.left + self.border / 2
                               + (enemy_w + self.border) * ((j * army_lines + i) // army_lines),
                               self.top + self.border / 2
                               + (enemy_h + self.border) * ((j * army_lines + i) % army_lines),
                               enemy_w,
                               enemy_h,
                               config.enemy_speed,
                               (j * army_lines + i),
                               30 - ((i + 1) // 2) * 10) for i in range(army_lines)] for j in range(army_columns)]
        self.speed = speed[0]
        self.move_error = (0.0, 0.0)
        self.next_line_step = (enemy_h + config.enemy_border) / 2
        self.is_win = False
        random.seed()

    def draw(self, surface):
        for column in self.enemies:
            for e in column:
                e.draw(surface)

    @property
    def strength(self):
        """
        the amount of the cost of enemies property
        :return:
        int
        """
        return sum([sum([i.cost for i in column]) for column in self.enemies])

    def check_collision(self, game_objects):
        """
        Проверка всех объектов, попал ли в них элемент из game_objects
        :param game_objects:
        list(GameObject)
        :return:
        void
        """
        for column in self.enemies:
            for e in column:
                e.check_collision(game_objects)

    def shoot_to_player(self, game_objects):
        """
        fina player under enemy and fire to him
        :param game_objects:
        GameObject instance
        :return:
        """
        for player in game_objects.game_objects:
            if player.__class__.__name__ == "Player":
                for column in self.enemies:
                    for e in column:
                        if player.left < e.right and player.right > e.left:
                            e.shooting(game_objects)

    def to_next_line(self):
        """
        move enemies to one line down
        :return:
        void
        """
        self.move(0, self.next_line_step)
        self.to_left = not self.to_left
        self.to_right = not self.to_right
        for column in self.enemies:
            for e in column:
                e.move(0, self.next_line_step)

    def delete_dead(self):
        """
        find enemies, who dead, and delete him
        if delete - delete shooting rights to the next enemy in column
        :return:
        void
        """
        for column in self.enemies:
            logic.delete_dead_from_collection(column)
            if len(column) > 0:
                column[-1].can_shoot = True

    def update(self):
        min_x = self.right
        max_x = self.left
        max_y = self.top

        speed = (self.speed / (sum([len(column) for column in self.enemies]) + 0.1))

        if self.to_left:
            dx = -(min(speed, self.left))
        elif self.to_right:
            dx = min(speed, config.width - self.right)
        else:
            return

        if abs(dx) < speed:
            self.to_next_line()

        for column in self.enemies:
            for e in column:
                e.move(dx, 0)
                min_x = min(e.left, min_x)
                max_x = max(e.right, max_x)
                max_y = max(e.bottom, max_y)

        self.bounds = Rect(min_x - self.border,
                           self.bounds.y,
                           max_x - min_x + self.border*2,
                           max_y - self.top + self.border)
