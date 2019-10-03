import pygame
from collections import defaultdict
import math
import config

keydown_handlers = defaultdict(list)
keyup_handlers = defaultdict(list)


def get_keydown(player):
    """
    connect press key and methods
    :param player:
    Player
    :return:
    defaultdict(list)
    """
    keydown_handlers[pygame.K_LEFT].append(player.handle_go)
    keydown_handlers[pygame.K_RIGHT].append(player.handle_go)
    return keydown_handlers


def get_keyup(player):
    """
    connect keyexit and methods
    :param player:
    Player
    :return:
    defaultdict(list)
    """
    keyup_handlers[pygame.K_LEFT].append(player.handle_stop)
    keyup_handlers[pygame.K_RIGHT].append(player.handle_stop)
    return keyup_handlers


def delete_dead_from_collection(objects):
    """
    :param objects:
    list(GameObject)
    :return:
    void
    """
    for obj in objects:
        if obj.is_dead:
            objects.remove(obj)


def check_collision(target, game_objects):
    """
    check collide bullet and target
    :param target:
    GameObject
    :param game_objects:
    list(GameObject)
    :return:
    void
    """
    res = False
    for obj in game_objects:
        if target.is_collided_with(obj) and obj.__class__.__name__ == 'Bullet':
            obj.kill()
            target.kill()
            res = True
    return res


def is_out_side(obj, width=config.width, height=config.height):
    """
    a predicate that returns true if an object is inside a surface(don't used)
    :param height:
    int (surface height)
    :param width:
    int (surface width)
    :return:
    bool
    """
    out_x = obj.center_x < 0 or obj.center_x > width
    out_y = obj.center_y < 0 or obj.center_y > height
    return out_x or out_y


def distance(obj1, obj2):
    """
    Return distance between center 2 objects
    :param obj1:
    GameObject
    :param obj2:
    GameObject
    :return:
    double
    """
    return math.sqrt((obj1.center_x - obj2.center_x)**2 + (obj1.center_y - obj2.center_y)**2)
