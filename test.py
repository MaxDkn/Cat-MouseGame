import unittest

import pygame
from game import Game
import time
KEYS_P1 = [pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s]
KEYS_P2 = [pygame.K_k, pygame.K_m, pygame.K_o, pygame.K_l]


def create_key_mock(initial_keys, pressed_keys):
   def helper():
        tmp = {}
        for key in initial_keys:
            tmp[key] = 0
        for pressed_key in pressed_keys:
            tmp[pressed_key] = 1
        return tmp
   return helper

no_key = create_key_mock(KEYS_P1 + KEYS_P2, [])
initial_rect1 = (72, 361, 56, 38)
initial_rect2 = (1255, 369, 50, 22)


def function_of_Ben(swap_time, current_time):
    res = swap_time - current_time
    while res < 0:
        res += swap_time
    return res


def remainingTime(swap_time, current_time):
    res2 = swap_time - (current_time % swap_time)
    return res2


class Time(unittest.TestCase):
    def testToto(self):
        self.assertEqual(remainingTime(30, 1), 29)
        self.assertEqual(remainingTime(30, 0), 30)
        self.assertEqual(remainingTime(30, 35), 25)


class GameTest(unittest.TestCase):


    def setUp(self) -> None:
        self.game = Game()

    def test_game(self):
        self.assertIsNotNone(self.game)
        self.assertIsNotNone(self.game.screen)
        self.assertIsNotNone(self.game.player1)
        self.assertIsNotNone(self.game.player2)
        self.assertEqual(self.game.player1.animal_type, 'Cat')
        self.assertEqual(self.game.player2.animal_type, 'Mouse')
        initial_image1 = self.game.player1.image
        self.assertIsNotNone(initial_image1)
        self.assertEqual(self.game.player1.rect, initial_rect1)
        self.assertEqual(self.game.player2.rect, initial_rect2)

    def test_movedown_player2(self):
        initial_image1 = self.game.player1.image
        initial_image2 = self.game.player2.image
        initial_x = self.game.player2.rect.x
        initial_y = self.game.player2.rect.y
        move_down_mock = create_key_mock(KEYS_P1 + KEYS_P2, [pygame.K_l])
        self.game.loop_one(move_down_mock)
        self.assertNotEqual(self.game.player1.image, initial_image1)
        self.assertNotEqual(self.game.player2.image, initial_image2)
        self.assertEqual(self.game.player1.rect, initial_rect1)
        self.assertEqual(self.game.player2.rect.x, initial_x)
        self.assertEqual(self.game.player2.rect.y, initial_y + 2)

        for i in range(120):
            self.game.loop_one(move_down_mock)
        self.assertEqual(self.game.player2.rect.y, 707)

    def test_move_up_player2(self):
        move_up_mock = create_key_mock(KEYS_P1 + KEYS_P2, [pygame.K_o])
        for i in range(100):
            self.game.loop_one(move_up_mock)
        self.assertEqual(self.game.player2.rect.y, 70)
        for i in range(10):
            self.game.loop_one(move_up_mock)
        self.assertEqual(self.game.player2.rect.y, 40)

    def test_collide_and_the_cat_wins(self):
        self.assertEqual(self.game.player1.score, 0)
        move_up_and_left_mock = create_key_mock(KEYS_P1 + KEYS_P2, [pygame.K_k, pygame.K_d])
        for i in range(250):
            self.game.loop_one(move_up_and_left_mock)
        # Collision happens and the cat wins
        self.assertGreater(self.game.player2.rect.x, 500)
        self.assertLess(self.game.player1.rect.x, 500)
        self.assertEqual(self.game.player1.score, 1)


class FastGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(timing_swap=1)

    def test_animal_type_swaps(self):

        self.assertEqual(self.game.player1.animal_type, 'Cat')
        self.assertEqual(self.game.player2.animal_type, 'Mouse')
        self.assertEqual(self.game.player1.delta_speed, 2)
        self.assertEqual(self.game.player2.delta_speed, 3)
        self.game.loop_one(no_key)
        time.sleep(1.5)
        self.game.loop_one(no_key)
        self.assertEqual(self.game.player1.animal_type, 'Mouse')
        self.assertEqual(self.game.player2.animal_type, 'Cat')
        self.assertEqual(self.game.player1.delta_speed, 3)
        self.assertEqual(self.game.player2.delta_speed, 2)


class FastGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(timing_swap=1)

    def test_display_score(self):
        self.game.loop_one(no_key)
        self.game.display_win(self.game.player1)
        for i in range(200):
            self.game.loop_one(no_key)


if __name__ == '__main__':
    unittest.main()
