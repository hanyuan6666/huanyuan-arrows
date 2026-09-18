import pygame

from game import Game
from ui import UI
# ============================================================
# 初始化
# ============================================================
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption("一箭又一箭")

clock = pygame.time.Clock()

# ============================================================
# UI
# ============================================================

ui = UI(
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

# ============================================================
# 游戏状态
# ============================================================

MENU = "menu"
PLAYING = "playing"
SUCCESS = "success"
FAILED = "failed"

game_state = MENU

game = None

# ============================================================
# 按钮
# ============================================================

start_button = pygame.Rect(
    350,
    350,
    300,
    70
)

next_button = pygame.Rect(
    330,
    400,
    160,
    60
)

restart_button = pygame.Rect(
    510,
    400,
    160,
    60
)
# ============================================================
# 开始游戏
# ============================================================
def start_game():
    """
    创建一个新的游戏。
    """
    global game
    global game_state
    game = Game()
    game_state = PLAYING
# ============================================================
# 菜单点击
# ============================================================
def handle_menu_click(pos):
    """
    处理开始界面的点击。
    """

    if start_button.collidepoint(pos):

        start_game()
# ============================================================
# 游戏点击
# ============================================================
def handle_game_click(pos):
    """
    处理游戏中的点击。
    """

    global game_state

    if game is None:
        return

    game.handle_click(
        pos[0],
        pos[1]
    )
    # 通关
    if game.get_state() == Game.SUCCESS:

        game_state = SUCCESS
    # 失败
    elif game.get_state() == Game.FAILED:

        game_state = FAILED
# ============================================================
# 通关界面点击
# ============================================================

def handle_success_click(pos):
    """
    处理通关界面的按钮。
    """
    global game_state
    if game is None:
        return
    # 下一关 / 重新开始
    if next_button.collidepoint(pos):

        if game.get_level_number() < 3:

            game.next_level()

            game_state = PLAYING
        else:
            # 第三关完成后重新开始
            game.load_level(1)

            game_state = PLAYING
    # 重玩本关
    elif restart_button.collidepoint(pos):

        game.restart_level()

        game_state = PLAYING
# ============================================================
# 失败界面点击
# ============================================================

def handle_failed_click(pos):
    """
    处理失败界面的按钮。
    """

    global game_state

    if game is None:
        return

    if restart_button.collidepoint(pos):

        game.restart_level()

        game_state = PLAYING
# ============================================================
# 绘制菜单
# ============================================================
def draw_menu():
    """
    绘制开始界面。
    """

    ui.draw_menu(
        screen,
        start_button
    )

# ============================================================
# 绘制游戏
# ============================================================

def draw_playing():
    """
    绘制游戏界面。
    """

    screen.fill(
        ui.background
    )
    # 顶部信息
    ui.draw_game_header(
        screen,
        game.get_level_number(),
        game.get_remaining_count(),
        game.get_mistake_count(),
        game.MAX_MISTAKES
    )
    # 棋盘
    game.draw_board(screen)

    # 箭头
    game.draw_arrows(screen)

    # 底部提示
    ui.draw_game_hint(
        screen,
        game.message
    )

# ============================================================
# 绘制通关界面
# ============================================================

def draw_success():
    """
    绘制通关界面。
    """

    ui.draw_success(
        screen,
        game.get_level_number(),
        next_button,
        restart_button,
        game.get_level_number() < 3
    )
# ============================================================
# 绘制失败界面
# ============================================================
def draw_failed():
    """
    绘制失败界面。
    """

    ui.draw_failed(
        screen,
        restart_button
    )
# ============================================================
# 主循环
# ============================================================
running = True
while running:
    # 控制 60 FPS
    dt = clock.tick(60) / 1000.0
    # --------------------------------------------------------
    # 处理事件
    # --------------------------------------------------------
    for event in pygame.event.get():
        # 关闭窗口
        if event.type == pygame.QUIT:
            running = False
        # 鼠标点击
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                # 开始界面
                if game_state == MENU:
                    handle_menu_click(
                        mouse_pos
                    )
                # 游戏界面
                elif game_state == PLAYING:

                    handle_game_click(
                        mouse_pos
                    )
                # 通关界面
                elif game_state == SUCCESS:

                    handle_success_click(
                        mouse_pos
                    )
                # 失败界面
                elif game_state == FAILED:

                    handle_failed_click(
                        mouse_pos
                    )
    # --------------------------------------------------------
    # 更新游戏
    # --------------------------------------------------------
    if game_state == PLAYING and game is not None:

        game.update(dt)

        if game.get_state() == Game.SUCCESS:

            game_state = SUCCESS

        elif game.get_state() == Game.FAILED:

            game_state = FAILED

    # --------------------------------------------------------
    # 绘制
    # --------------------------------------------------------
    if game_state == MENU:

        draw_menu()

    elif game_state == PLAYING:

        draw_playing()

    elif game_state == SUCCESS:

        draw_success()

    elif game_state == FAILED:

        draw_failed()
    # --------------------------------------------------------
    # 刷新屏幕
    # --------------------------------------------------------
    pygame.display.flip()
# ============================================================
# 退出
# ============================================================
pygame.quit()