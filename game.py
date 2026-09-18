import pygame
from arrow import Arrow
from level import create_level, get_level_count

class Game:
    """
    游戏核心逻辑类
    """
    PLAYING = "playing"
    SUCCESS = "success"
    FAILED = "failed"
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700

    BOARD_SIZE = 6
    CELL_SIZE = 80

    MAX_MISTAKES = 3

    def __init__(self):
        self.current_level = 1
        self.state = self.PLAYING
        self.mistakes = 0
        self.arrows = []
        # 棋盘位置
        self.board_x = (
            self.SCREEN_WIDTH
            - self.BOARD_SIZE * self.CELL_SIZE
        ) // 2
        self.board_y = 130
        # 提示文字
        self.message = ""
        # 提示显示时间
        self.message_timer = 0
        # 当前被点击、但被挡住的箭头
        self.selected_arrow = None
        self.load_level(1)
    # ========================================================
    # 关卡
    # ========================================================
    def load_level(self, level_number):
        """
        加载关卡
        """
        if level_number < 1:
            level_number = 1

        if level_number > get_level_count():
            level_number = get_level_count()

        self.current_level = level_number

        self.arrows = create_level(
            level_number
        )

        self.state = self.PLAYING

        self.mistakes = 0

        self.message = ""
        self.message_timer = 0

        self.selected_arrow = None

        # 设置箭头初始位置
        for arrow in self.arrows:

            arrow.set_position(
                self.board_x,
                self.board_y,
                self.CELL_SIZE
            )

    def restart_level(self):
        """
        重新开始当前关卡
        """

        self.load_level(
            self.current_level
        )

    def next_level(self):
        """
        进入下一关
        """
        if self.current_level < get_level_count():

            self.load_level(
                self.current_level + 1
            )
        else:

            self.load_level(1)
    # ========================================================
    # 鼠标点击
    # ========================================================
    def get_clicked_cell(
        self,
        mouse_x,
        mouse_y
    ):
        """
        根据鼠标位置获取棋盘格。
        """

        board_width = (
            self.BOARD_SIZE
            * self.CELL_SIZE
        )

        if not (
            self.board_x <= mouse_x
            < self.board_x + board_width
        ):
            return None

        if not (
            self.board_y <= mouse_y
            < self.board_y + board_width
        ):
            return None

        col = (
            mouse_x - self.board_x
        ) // self.CELL_SIZE

        row = (
            mouse_y - self.board_y
        ) // self.CELL_SIZE

        return int(row), int(col)

    def find_arrow(
        self,
        row,
        col
    ):
        """
        根据行列寻找箭头。
        """
        for arrow in self.arrows:

            if arrow.moving:
                continue

            if (
                arrow.row == row
                and
                arrow.col == col
            ):
                return arrow

        return None

    def handle_click(
        self,
        mouse_x,
        mouse_y
    ):
        """
        处理玩家点击。
        """
        if self.state != self.PLAYING:
            return

        cell = self.get_clicked_cell(
            mouse_x,
            mouse_y
        )

        if cell is None:
            return

        row, col = cell

        arrow = self.find_arrow(
            row,
            col
        )

        # 点击空白位置
        if arrow is None:

            self.selected_arrow = None

            self.show_message(
                "这里没有箭头"
            )

            return
        # ====================================================
        # 可以飞
        # ====================================================
        if self.can_arrow_move(arrow):

            self.selected_arrow = None

            arrow.start_moving()

            self.show_message(
                "箭头飞出！"
            )
        # ====================================================
        # 被挡住
        # ====================================================
        else:

            self.selected_arrow = arrow

            arrow.play_hit_effect()

            self.mistakes += 1

            self.show_message(
                f"前方有箭头挡住！"
                f"  错误 {self.mistakes}/{self.MAX_MISTAKES}"
            )

            if self.mistakes >= self.MAX_MISTAKES:

                self.state = self.FAILED
    # ========================================================
    # 判断箭头能否飞出
    # ========================================================

    def can_arrow_move(
        self,
        arrow
    ):
        """
        判断箭头前方是否有其他箭头。

        如果一路走到棋盘外都没有遇到箭头，
        则可以飞出。

        如果遇到其他箭头，
        则不能飞。
        """
        row = arrow.row
        col = arrow.col

        dr, dc = self.get_grid_direction(
            arrow.direction
        )
        # 从箭头前面的第一个格子开始检查
        row += dr
        col += dc

        while self.is_inside_board(
            row,
            col
        ):
            for other_arrow in self.arrows:

                # 不检查自己
                if other_arrow is arrow:
                    continue

                # 正在飞走的箭头不再阻挡
                if other_arrow.moving:
                    continue

                if (
                    other_arrow.row == row
                    and
                    other_arrow.col == col
                ):

                    return False

            row += dr
            col += dc

        return True

    def get_grid_direction(
        self,
        direction
    ):
        """
        把方向转换成行列变化。
        """

        if direction == Arrow.UP:
            return -1, 0

        if direction == Arrow.DOWN:
            return 1, 0

        if direction == Arrow.LEFT:
            return 0, -1

        if direction == Arrow.RIGHT:
            return 0, 1

        return 0, 0

    def is_inside_board(
        self,
        row,
        col
    ):
        """
        判断格子是否在棋盘内。
        """

        return (
            0 <= row < self.BOARD_SIZE
            and
            0 <= col < self.BOARD_SIZE
        )
    # ========================================================
    # 更新
    # ========================================================
    def update(self, dt):
        """
        每一帧更新游戏。
        """
        # 更新提示计时器
        if self.message_timer > 0:

            self.message_timer -= dt

            if self.message_timer <= 0:

                self.message_timer = 0
                self.message = ""

        # 更新所有箭头
        for arrow in self.arrows:

            if arrow.moving:

                arrow.update(dt)

            arrow.update_hit_effect(dt)

        # 删除已经飞出屏幕的箭头
        remaining_arrows = []

        for arrow in self.arrows:

            if arrow.moving:

                if arrow.is_outside(
                    self.SCREEN_WIDTH,
                    self.SCREEN_HEIGHT
                ):
                    continue

            remaining_arrows.append(
                arrow
            )

        self.arrows = remaining_arrows

        # 全部箭头清除
        if (
            self.state == self.PLAYING
            and
            len(self.arrows) == 0
        ):

            self.state = self.SUCCESS

    # ========================================================
    # 提示
    # ========================================================

    def show_message(
        self,
        message
    ):
        """
        显示提示文字。
        """
        self.message = message

        self.message_timer = 1.5

    # ========================================================
    # 游戏信息
    # ========================================================

    def get_remaining_count(self):
        return len(self.arrows)

    def get_mistake_count(self):
        return self.mistakes

    def get_level_number(self):
        return self.current_level

    def get_state(self):
        return self.state

    # ========================================================
    # 绘制棋盘
    # ========================================================

    def draw_board(
        self,
        screen
    ):
        """
        绘制 6×6 棋盘。
        """

        for row in range(
            self.BOARD_SIZE
        ):

            for col in range(
                self.BOARD_SIZE
            ):

                x = (
                    self.board_x
                    + col * self.CELL_SIZE
                )

                y = (
                    self.board_y
                    + row * self.CELL_SIZE
                )

                rect = pygame.Rect(
                    x,
                    y,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )

                pygame.draw.rect(
                    screen,
                    (235, 235, 235),
                    rect
                )

                pygame.draw.rect(
                    screen,
                    (180, 180, 180),
                    rect,
                    2
                )

    # ========================================================
    # 绘制箭头
    # ========================================================

    def draw_arrows(
        self,
        screen
    ):
        """
        绘制所有箭头。
        """

        for arrow in self.arrows:

            # 被挡住的箭头使用特殊颜色
            if arrow is self.selected_arrow:

                arrow_color = (
                    245,
                    130,
                    40
                )

                outline_color = (
                    180,
                    70,
                    10
                )

            else:

                arrow_color = (
                    220,
                    60,
                    60
                )

                outline_color = (
                    120,
                    20,
                    20
                )

            arrow.draw(
                screen,
                self.board_x,
                self.board_y,
                self.CELL_SIZE,
                arrow_color,
                outline_color
            )

    # ========================================================
    # 绘制游戏
    # ========================================================

    def draw(
        self,
        screen
    ):
        """
        绘制整个游戏。
        """

        screen.fill(
            (248, 248, 248)
        )

        font = pygame.font.Font(
            "C:/Windows/Fonts/msyh.ttc",
            40
        )

        title = font.render(
            f"一箭又一箭    第 {self.current_level} 关",
            True,
            (40, 40, 40)
        )

        title_rect = title.get_rect(
            center=(
                self.SCREEN_WIDTH // 2,
                50
            )
        )

        screen.blit(
            title,
            title_rect
        )

        # 棋盘
        self.draw_board(
            screen
        )

        # 箭头
        self.draw_arrows(
            screen
        )

        # 底部信息
        info_font = pygame.font.Font(
            "C:/Windows/Fonts/msyh.ttc",
            24
        )

        info_text = (
            f"剩余箭头：{self.get_remaining_count()}"
            f"    "
            f"错误次数："
            f"{self.mistakes}/{self.MAX_MISTAKES}"
        )

        info = info_font.render(
            info_text,
            True,
            (60, 60, 60)
        )

        info_rect = info.get_rect(
            center=(
                self.SCREEN_WIDTH // 2,
                610
            )
        )

        screen.blit(
            info,
            info_rect
        )

        # 提示信息
        if self.message:

            message_font = pygame.font.Font(
                "C:/Windows/Fonts/msyh.ttc",
                26
            )

            message = message_font.render(
                self.message,
                True,
                (200, 70, 40)
            )

            message_rect = message.get_rect(
                center=(
                    self.SCREEN_WIDTH // 2,
                    660
                )
            )

            screen.blit(
                message,
                message_rect
            )


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":

    pygame.init()

    print("=" * 50)
    print("Game 类测试")
    print("=" * 50)

    game = Game()

    print(
        f"当前关卡："
        f"{game.get_level_number()}"
    )

    print(
        f"箭头数量："
        f"{game.get_remaining_count()}"
    )

    print(
        f"错误次数："
        f"{game.get_mistake_count()}"
    )

    print(
        f"游戏状态："
        f"{game.get_state()}"
    )

    print("=" * 50)
    print("Game 类创建成功！")
    print("=" * 50)

    pygame.quit()