import pygame


class UI:
    """
    游戏界面管理类
    """

    FONT_PATH = "C:/Windows/Fonts/msyh.ttc"

    def __init__(self, screen_width=1000, screen_height=700):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 字体
        self.title_font = pygame.font.Font(
            self.FONT_PATH,
            56
        )

        self.large_font = pygame.font.Font(
            self.FONT_PATH,
            40
        )

        self.button_font = pygame.font.Font(
            self.FONT_PATH,
            30
        )

        self.info_font = pygame.font.Font(
            self.FONT_PATH,
            24
        )

        self.small_font = pygame.font.Font(
            self.FONT_PATH,
            20
        )

        # 颜色
        self.background = (245, 245, 245)
        self.dark = (40, 40, 40)
        self.gray = (100, 100, 100)

        self.button_color = (70, 130, 200)
        self.button_hover = (90, 150, 220)

        self.success_color = (50, 160, 80)
        self.failed_color = (200, 60, 60)

    # ========================================================
    # 文字
    # ========================================================

    def draw_text(
        self,
        screen,
        text,
        font,
        color,
        center
    ):
        surface = font.render(
            text,
            True,
            color
        )

        rect = surface.get_rect(
            center=center
        )

        screen.blit(
            surface,
            rect
        )

    # ========================================================
    # 按钮
    # ========================================================

    def draw_button(
        self,
        screen,
        rect,
        text
    ):
        """
        绘制带鼠标悬停效果的按钮
        """

        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):
            color = self.button_hover
        else:
            color = self.button_color

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (40, 80, 130),
            rect,
            2,
            border_radius=12
        )

        self.draw_text(
            screen,
            text,
            self.button_font,
            (255, 255, 255),
            rect.center
        )

    # ========================================================
    # 开始界面
    # ========================================================

    def draw_menu(
        self,
        screen,
        start_button
    ):
        screen.fill(
            self.background
        )

        self.draw_text(
            screen,
            "一箭又一箭",
            self.title_font,
            self.dark,
            (
                self.screen_width // 2,
                180
            )
        )

        self.draw_text(
            screen,
            "观察箭头方向，让箭头依次飞出棋盘",
            self.info_font,
            self.gray,
            (
                self.screen_width // 2,
                260
            )
        )

        self.draw_button(
            screen,
            start_button,
            "开始游戏"
        )

        self.draw_text(
            screen,
            "游戏共有 3 个关卡",
            self.small_font,
            self.gray,
            (
                self.screen_width // 2,
                470
            )
        )

    # ========================================================
    # 游戏顶部信息
    # ========================================================

    def draw_game_header(
        self,
        screen,
        level,
        remaining,
        mistakes,
        max_mistakes
    ):
        """
        绘制游戏顶部信息
        """

        self.draw_text(
            screen,
            f"一箭又一箭    第 {level} 关",
            self.large_font,
            self.dark,
            (
                self.screen_width // 2,
                50
            )
        )

        # 左侧信息
        remaining_text = (
            f"剩余箭头：{remaining}"
        )

        self.draw_text(
            screen,
            remaining_text,
            self.info_font,
            self.dark,
            (180, 100)
        )

        # 右侧信息
        mistake_text = (
            f"错误次数：{mistakes}/{max_mistakes}"
        )

        if mistakes >= max_mistakes - 1:
            mistake_color = self.failed_color
        else:
            mistake_color = self.dark

        self.draw_text(
            screen,
            mistake_text,
            self.info_font,
            mistake_color,
            (820, 100)
        )

    # ========================================================
    # 游戏底部提示
    # ========================================================

    def draw_game_hint(
        self,
        screen,
        message=""
    ):
        """
        绘制游戏提示
        """

        if message:
            color = self.failed_color

            self.draw_text(
                screen,
                message,
                self.info_font,
                color,
                (
                    self.screen_width // 2,
                    650
                )
            )

        else:
            self.draw_text(
                screen,
                "点击箭头，让它沿箭头方向飞出",
                self.small_font,
                self.gray,
                (
                    self.screen_width // 2,
                    650
                )
            )

    # ========================================================
    # 通关界面
    # ========================================================

    def draw_success(
        self,
        screen,
        level,
        next_button,
        restart_button,
        has_next_level
    ):
        screen.fill(
            self.background
        )

        self.draw_text(
            screen,
            "恭喜通关！",
            self.title_font,
            self.success_color,
            (
                self.screen_width // 2,
                180
            )
        )

        self.draw_text(
            screen,
            f"第 {level} 关完成",
            self.info_font,
            self.gray,
            (
                self.screen_width // 2,
                260
            )
        )

        if has_next_level:
            self.draw_button(
                screen,
                next_button,
                "下一关"
            )
        else:
            self.draw_button(
                screen,
                next_button,
                "重新开始"
            )

        self.draw_button(
            screen,
            restart_button,
            "重玩本关"
        )

    # ========================================================
    # 失败界面
    # ========================================================

    def draw_failed(
        self,
        screen,
        restart_button
    ):
        screen.fill(
            self.background
        )

        self.draw_text(
            screen,
            "游戏失败",
            self.title_font,
            self.failed_color,
            (
                self.screen_width // 2,
                180
            )
        )

        self.draw_text(
            screen,
            "错误次数已经达到上限",
            self.info_font,
            self.gray,
            (
                self.screen_width // 2,
                260
            )
        )

        self.draw_button(
            screen,
            restart_button,
            "重新开始"
        )