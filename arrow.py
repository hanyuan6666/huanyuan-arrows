import pygame
class Arrow:
    """
    游戏中的箭头对象
    """
    # 四个方向
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    def __init__(self, row, col, direction):
        """
        创建箭头
        """
        self.row = row
        self.col = col
        self.direction = direction
        # 是否正在飞行
        self.moving = False
        # 屏幕上的像素位置
        self.x = 0
        self.y = 0
        # 飞行速度
        self.speed = 650
        # 箭头大小
        self.size = 22
        # 飞行过程中逐渐缩小
        self.scale = 1.0
        # 点击反馈动画
        self.hit_effect = 0
    # ========================================================
    # 设置位置
    # ========================================================
    def set_position(
        self,
        board_x,
        board_y,
        cell_size
    ):
        """
        根据棋盘位置设置箭头的屏幕坐标。
        """
        self.x = (
            board_x
            + self.col * cell_size
            + cell_size // 2
        )
        self.y = (
            board_y
            + self.row * cell_size
            + cell_size // 2
        )

    # ========================================================
    # 获取方向
    # ========================================================

    def get_direction_vector(self):
        """
        获取像素移动方向。
        """

        if self.direction == self.UP:
            return 0, -1

        if self.direction == self.DOWN:
            return 0, 1

        if self.direction == self.LEFT:
            return -1, 0

        if self.direction == self.RIGHT:
            return 1, 0

        return 0, 0

    def get_grid_direction(self):
        """
        获取棋盘格移动方向。
        """

        if self.direction == self.UP:
            return -1, 0

        if self.direction == self.DOWN:
            return 1, 0

        if self.direction == self.LEFT:
            return 0, -1

        if self.direction == self.RIGHT:
            return 0, 1

        return 0, 0

    # ========================================================
    # 获取下一个格子
    # ========================================================

    def get_next_cell(self):
        """
        获取箭头前面的格子。
        """

        dr, dc = self.get_grid_direction()

        return (
            self.row + dr,
            self.col + dc
        )

    # ========================================================
    # 开始飞行
    # ========================================================

    def start_moving(self):
        """
        开始飞出棋盘。
        """

        self.moving = True

        # 重置动画参数
        self.scale = 1.0

    # ========================================================
    # 更新动画
    # ========================================================

    def update(self, dt):
        """
        更新箭头动画。
        """

        if not self.moving:
            return

        dx, dy = self.get_direction_vector()

        # 移动
        self.x += (
            dx * self.speed * dt
        )

        self.y += (
            dy * self.speed * dt
        )

        # 飞出去时逐渐缩小
        self.scale -= dt * 0.35

        if self.scale < 0.65:
            self.scale = 0.65

    # ========================================================
    # 是否飞出屏幕
    # ========================================================

    def is_outside(
        self,
        screen_width,
        screen_height
    ):
        """
        判断箭头是否已经飞出屏幕。
        """

        margin = 80

        return (
            self.x < -margin
            or
            self.x > screen_width + margin
            or
            self.y < -margin
            or
            self.y > screen_height + margin
        )

    # ========================================================
    # 点击反馈
    # ========================================================

    def play_hit_effect(self):
        """
        播放点击反馈。
        """

        self.hit_effect = 0.15

    def update_hit_effect(self, dt):
        """
        更新点击反馈动画。
        """

        if self.hit_effect > 0:

            self.hit_effect -= dt

            if self.hit_effect < 0:
                self.hit_effect = 0

    # ========================================================
    # 绘制箭头
    # ========================================================

    def draw(
        self,
        screen,
        board_x,
        board_y,
        cell_size,
        color=(220, 60, 60),
        outline_color=(120, 20, 20)
    ):
        """
        绘制箭头。
        """

        # 没有飞行时，根据棋盘位置计算坐标
        if not self.moving:

            self.set_position(
                board_x,
                board_y,
                cell_size
            )

        # 计算当前大小
        current_size = int(
            self.size * self.scale
        )

        # 点击反馈时稍微放大
        if self.hit_effect > 0:

            current_size += 6

        center_x = int(self.x)
        center_y = int(self.y)

        size = current_size

        # ====================================================
        # 根据方向生成箭头形状
        # ====================================================

        if self.direction == self.UP:

            points = [
                (
                    center_x,
                    center_y - size
                ),
                (
                    center_x - size,
                    center_y
                ),
                (
                    center_x - size // 2,
                    center_y
                ),
                (
                    center_x - size // 2,
                    center_y + size
                ),
                (
                    center_x + size // 2,
                    center_y + size
                ),
                (
                    center_x + size // 2,
                    center_y
                ),
                (
                    center_x + size,
                    center_y
                )
            ]

        elif self.direction == self.DOWN:

            points = [
                (
                    center_x,
                    center_y + size
                ),
                (
                    center_x - size,
                    center_y
                ),
                (
                    center_x - size // 2,
                    center_y
                ),
                (
                    center_x - size // 2,
                    center_y - size
                ),
                (
                    center_x + size // 2,
                    center_y - size
                ),
                (
                    center_x + size // 2,
                    center_y
                ),
                (
                    center_x + size,
                    center_y
                )
            ]

        elif self.direction == self.LEFT:

            points = [
                (
                    center_x - size,
                    center_y
                ),
                (
                    center_x,
                    center_y - size
                ),
                (
                    center_x,
                    center_y - size // 2
                ),
                (
                    center_x + size,
                    center_y - size // 2
                ),
                (
                    center_x + size,
                    center_y + size // 2
                ),
                (
                    center_x,
                    center_y + size // 2
                ),
                (
                    center_x,
                    center_y + size
                )
            ]

        else:  # RIGHT

            points = [
                (
                    center_x + size,
                    center_y
                ),
                (
                    center_x,
                    center_y - size
                ),
                (
                    center_x,
                    center_y - size // 2
                ),
                (
                    center_x - size,
                    center_y - size // 2
                ),
                (
                    center_x - size,
                    center_y + size // 2
                ),
                (
                    center_x,
                    center_y + size // 2
                ),
                (
                    center_x,
                    center_y + size
                )
            ]

        # ====================================================
        # 绘制箭头
        # ====================================================

        pygame.draw.polygon(
            screen,
            color,
            points
        )

        pygame.draw.lines(
            screen,
            outline_color,
            True,
            points,
            3
        )

    # ========================================================
    # 判断鼠标是否点击箭头所在格子
    # ========================================================

    def contains_point(
        self,
        mouse_x,
        mouse_y,
        board_x,
        board_y,
        cell_size
    ):
        """
        判断鼠标是否点击当前箭头所在格子。
        """

        cell_left = (
            board_x
            + self.col * cell_size
        )

        cell_top = (
            board_y
            + self.row * cell_size
        )

        return (
            cell_left <= mouse_x
            < cell_left + cell_size
            and
            cell_top <= mouse_y
            < cell_top + cell_size
        )

    # ========================================================
    # 调试信息
    # ========================================================

    def __repr__(self):
        return (
            f"Arrow("
            f"row={self.row}, "
            f"col={self.col}, "
            f"direction='{self.direction}'"
            f")"
        )