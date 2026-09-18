import pygame
import unittest

from game import Game
from arrow import Arrow


class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    # T01：游戏能够正常创建
    def test_game_create(self):
        game = Game()

        self.assertIsNotNone(game)
        self.assertEqual(game.current_level, 1)
        self.assertEqual(game.state, Game.PLAYING)

    # T02：箭头前方没有障碍物，可以移动
    def test_arrow_can_move(self):
        game = Game()

        arrow = Arrow(0, 0, Arrow.RIGHT)
        game.arrows = [arrow]

        result = game.can_arrow_move(arrow)

        self.assertTrue(result)

    # T03：箭头前方存在其他箭头，不能移动
    def test_arrow_blocked(self):
        game = Game()

        arrow1 = Arrow(0, 0, Arrow.RIGHT)
        arrow2 = Arrow(0, 2, Arrow.UP)

        game.arrows = [arrow1, arrow2]

        result = game.can_arrow_move(arrow1)

        self.assertFalse(result)

    # T04：点击被挡住的箭头，错误次数增加
    def test_mistake_increase(self):
        game = Game()

        arrow1 = Arrow(0, 0, Arrow.RIGHT)
        arrow2 = Arrow(0, 2, Arrow.UP)

        game.arrows = [arrow1, arrow2]

        mouse_x = game.board_x + 40
        mouse_y = game.board_y + 40

        game.handle_click(mouse_x, mouse_y)

        self.assertEqual(game.mistakes, 1)
        self.assertEqual(game.state, Game.PLAYING)

    # T05：连续错误三次后游戏失败
    def test_game_failed_after_three_mistakes(self):
        game = Game()

        arrow1 = Arrow(0, 0, Arrow.RIGHT)
        arrow2 = Arrow(0, 2, Arrow.UP)

        game.arrows = [arrow1, arrow2]

        mouse_x = game.board_x + 40
        mouse_y = game.board_y + 40

        game.handle_click(mouse_x, mouse_y)
        game.handle_click(mouse_x, mouse_y)
        game.handle_click(mouse_x, mouse_y)

        self.assertEqual(game.mistakes, 3)
        self.assertEqual(game.state, Game.FAILED)

    # T06：所有箭头移除后进入成功状态
    def test_game_success(self):
        game = Game()

        arrow = Arrow(0, 0, Arrow.RIGHT)

        game.arrows = [arrow]

        # 让箭头开始飞出
        arrow.start_moving()

        # 模拟足够长的时间，让箭头飞出屏幕
        for _ in range(20):
            game.update(0.1)

        self.assertEqual(len(game.arrows), 0)
        self.assertEqual(game.state, Game.SUCCESS)


if __name__ == "__main__":
    unittest.main(verbosity=2)