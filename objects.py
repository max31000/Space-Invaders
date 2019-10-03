from player import Player
from interface import Interface
from army import Army
from tower import Tower
from enemy import Enemy
import config
import logic
from pygame import Rect
import random


class Objects:
    """
    Class-container all game objects
    """
    def __init__(self):
        self.game_objects = []
        self.towers = []
        self.player = None
        self.army = None
        self.score_text = None
        self.points = 0
        self.health = None
        self.level_text = None
        self.top_text = None
        self.start_army_strength = 0
        self.max_army_top = (config.height - config.player_height
                             - config.down_field - (config.enemy_height + config.enemy_border) * 2)
        self.pause = Interface(config.width // 2 - 60, config.down_border_field // 2,
                               290, 50,
                               "text", config.colors['orange'], 30)
        self.pause.set_text("PAUSE")
        random.seed()
        self.bonus_ship = None
        self.is_pause = False
        self.bonus_ship_cooldown = config.bonus_ship_cooldown

    def add(self, game_object):
        """
        add element to game
        :param game_object:
        GameObject
        :return:
        void
        """
        if not self.is_pause or game_object.__class__.__name__ != "Bullet":
            self.game_objects.append(game_object)

    def create_player(self, health=4):
        for obj in self.game_objects:
            if obj.__class__.__name__ == 'Player':
                self.game_objects.remove(obj)

        self.remove_all_bullets()

        self.player = Player((config.width - config.player_width) / 2,
                             config.height - config.player_height - config.down_field,
                             config.player_width,
                             config.player_height,
                             health)
        if self.health is not None:
            self.health.set_text("HEALTH: %d" % health)
        self.add(self.player)

    def create_bonus_ship(self):
        if self.bonus_ship is None:
            self.bonus_ship_cooldown = config.bonus_ship_cooldown
            self.bonus_ship = Enemy(0, config.up_border_field + 4,
                                    config.enemy_width * 1.5, config.enemy_height,
                                    (2.2, 0), 100, 300,
                                    config.colors['pink'])
            self.add(self.bonus_ship)

    def create_army(self, level=1):
        """
        create army, update lvl text in surface, add points from prev round, remove bullets, create towers
        :param level:
        int
        :return:
        """
        if self.level_text is not None:
            self.level_text.set_text("LVL: %d" % level)

        if self.army is None:
            old_army_strength = 0
            old_army_is_win = False
        else:
            old_army_strength = self.army.strength
            old_army_is_win = self.army.is_win

        self.army = Army(config.enemy_width,
                         config.enemy_height,
                         config.army_lines,
                         config.army_columns,
                         10,
                         config.up_border_field + min((config.enemy_height + config.enemy_border)
                                                      * level, self.max_army_top),
                         (config.enemy_speed[0] + level / 2, 0))
        if not old_army_is_win:
            self.start_army_strength += self.army.strength - old_army_strength
        self.remove_all_bullets()
        self.create_towers()

    def pause_game(self):
        self.is_pause = not self.is_pause
        if self.pause in self.game_objects:
            self.game_objects.remove(self.pause)
            return
        self.add(self.pause)

    def create_towers(self):
        with_towers_range = config.width // (config.towers_count + 0.7)
        for i in range(0, config.towers_count):
            tower = Tower(i * with_towers_range + config.towers_width // 2 + 12,
                          config.tower_top,
                          config.towers_width,
                          config.tower_height)
            self.towers.append(tower)
            self.add(tower)

    def create_interface(self):
        """
        Create Interface instances
        :return:
        void
        """
        self.score_text = Interface(0, 0, 400, 50, "text", config.colors['blue'])
        self.score_text.set_text("SCORE:0")
        self.health = Interface(0, config.down_border_field, 290, 50, "text", config.colors['blue'])
        self.health.set_text("HEALTH: %d" % 4)
        self.level_text = Interface(290, config.down_border_field, 290, 50, "text", config.colors['blue'])
        self.level_text.set_text("LVL: %d" % 1)
        self.top_text = Interface(220, 0, 220, 50, "text", config.colors['blue'])
        self.add(self.level_text)
        self.add(self.score_text)
        self.add(self.health)
        self.add(self.top_text)

        self.add(Interface(0, config.up_border_field, config.width, 2, "line"))
        self.add(Interface(0, config.down_border_field, config.width, 2, "line"))
        self.add(Interface(0, config.up_border_field,
                           2, config.down_border_field - config.up_border_field, "line"))
        self.add(Interface(config.width - 2, config.up_border_field,
                           2, config.down_border_field - config.up_border_field, "line"))
        self.add(Interface(0, config.down_border_field + 80, config.width, 2, "line"))

    def update_towers(self):
        for tower in self.towers:
            logic.check_collision(tower, self.game_objects)

            if tower.is_collided_with(self.army):
                if tower.bottom < self.army.bottom:
                    self.game_objects.remove(tower)
                    self.towers.remove(tower)
                    continue
                new_tower_top = max(tower.top, self.army.bottom)
                tower.bounds = Rect(tower.left,
                                    new_tower_top,
                                    tower.width,
                                    tower.bottom - new_tower_top)

    def update_bonus_ship(self):
        self.bonus_ship_cooldown -= 1
        if self.bonus_ship is not None:
            if logic.check_collision(self.bonus_ship, self.game_objects):
                self.add_points(self.bonus_ship.cost)
                self.bonus_ship = None
            elif logic.is_out_side(self.bonus_ship):
                self.bonus_ship = None
        if self.bonus_ship_cooldown < 0 and self.army.top > 100 and random.randint(0, 400) == 322:
            self.create_bonus_ship()

    def update(self):
        self.army.check_collision(self.game_objects)
        logic.check_collision(self.player, self.game_objects)
        self.update_towers()
        self.update_bonus_ship()
        self.army.update()
        self.army.shoot_to_player(self)
        if self.army.bottom > self.player.top + 3:
            self.player.kill()
            self.army.is_win = True
        for o in self.game_objects:
            o.update()

    def remove_all_bullets(self):
        for obj in self.game_objects:
            if obj.__class__.__name__ == 'Bullet':
                self.game_objects.remove(obj)

    def add_points(self, points):
        self.points += points
        self.score_text.set_text("SCORE:%d" % self.points)

    def draw(self, surface):
        self.army.draw(surface)
        for o in self.game_objects:
            o.draw(surface)

    def delete_dead(self):
        """
        delete dead objects and update scores
        :return:
        void
        """
        before_strength = self.army.strength
        logic.delete_dead_from_collection(self.game_objects)
        self.army.delete_dead()
        current_strength = self.army.strength
        if before_strength - current_strength > 0 and self.score_text is not None:
            self.add_points(before_strength - current_strength)
