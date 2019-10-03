import unittest
from game_object import GameObject
from bullet import Bullet
from player import Player
from enemy import Enemy
import config
from objects import Objects
from army import Army
import pygame
import textures
import logic


class ObjectsTests(unittest.TestCase):
    def testGameObject(self):
        go = GameObject(10, 10, 10, 10, (10, 0))
        start = go.center
        moving = (20, 20)
        go.move(*moving)
        end = go.center
        self.assertEqual((start[0] + moving[0], start[1] + moving[1]), end)
        go.update()
        end = go.center
        self.assertEqual((start[0] + moving[0] + 10, start[1] + moving[1]), end)

    def testObjects(self):
        pygame.init()
        o = Objects()
        self.assertEqual(len(o.game_objects), 0)
        o.create_player()
        self.assertEqual(len(o.game_objects), 1)

    def testPlayer(self):
        pl = Player(10, 10, 10, 10)
        start = pl.center
        moving = (20, 0)
        pl.move(*moving)
        end = pl.center
        self.assertEqual((start[0] + moving[0], start[1] + moving[1]), end)
        pl.to_right = True
        pl.update()
        pl.update()
        end = pl.center
        self.assertEqual((start[0] + moving[0] + 2 * config.player_speed, start[1] + moving[1]), end)

    def testEnemy(self):
        en = Enemy(10, 10, 10, 10, (10, 0), 1, 10)
        start = en.center
        moving = (20, 0)
        en.move(*moving)
        end = en.center
        self.assertEqual((start[0] + moving[0], start[1] + moving[1]), end)
        en.to_right = True
        en.update()
        en.update()
        end = en.center
        self.assertEqual((start[0] + moving[0] + 20, start[1] + moving[1]), end)


class ArmyTests(unittest.TestCase):
    def testArmyExist(self):
        self.ar = Army(10, 10, 5, 8, 0, 0)
        for col in self.ar.enemies:
            for a in col:
                b = Bullet(a.bounds.x,
                           a.bounds.y, (0, 0, 0))
            self.assertTrue(a.is_collided_with(b))

    def testArmyDead(self):
        self.ar = Army(10, 10, 5, 8, 0, 0)
        b = [Bullet(3, 3, (0, 0, 0))]
        self.ar.check_collision(b)
        self.assertTrue(b[0].is_dead)
        killed = []
        for i in range(0, config.death_timer):
            self.ar.update()
        for col in self.ar.enemies:
            for e in col:
                if e.is_dead:
                    killed.append(e)

        self.assertTrue(len(killed) > 0)

    def testToNextLine(self):
        enemy_h = 10
        self.ar = Army(enemy_h, enemy_h, 5, 8, 0, 0)
        top_ar = self.ar.top
        self.ar.to_next_line()
        top_next_ar = self.ar.top
        self.assertEqual(top_ar + round((enemy_h + config.enemy_border) / 2), top_next_ar)


if __name__ == '__main__':
    unittest.main()
