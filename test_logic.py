#!/usr/bin/env python3

import unittest
import logic
from game_object import GameObject
from bullet import Bullet


class LogicTests(unittest.TestCase):
    def testCheckCollision(self):
        bullets = [Bullet(0, 0, (0, 0, 0))]
        player_in_obj = GameObject(1, 1, 2, 2,)
        player_out = GameObject(110, 20, 2, 2)
        logic.check_collision(player_in_obj, bullets)
        logic.check_collision(player_out, bullets)
        self.assertTrue(player_in_obj.is_dead)
        self.assertFalse(player_out.is_dead)


if __name__ == '__main__':
    unittest.main()
