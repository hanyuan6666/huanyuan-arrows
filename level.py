from arrow import Arrow


# ============================================================
# 关卡数据
# ============================================================
#
# 每个箭头的数据格式：
#
# (行, 列, 方向)
#
# 行和列都是从 0 开始。
#
# 例如：
# (0, 0, Arrow.RIGHT)
#
# 表示：
# 第 0 行、第 0 列，有一个向右的箭头。
#
# ============================================================


LEVELS = {

    # ========================================================
    # 第 1 关
    # ========================================================
    #
    # 这一关比较简单，主要用来让玩家熟悉操作。
    #
    # 大部分箭头都朝向棋盘外侧。
    #
    1: [
        (0, 1, Arrow.UP),
        (0, 4, Arrow.UP),

        (1, 0, Arrow.LEFT),
        (2, 5, Arrow.RIGHT),

        (3, 0, Arrow.LEFT),
        (3, 5, Arrow.RIGHT),

        (5, 1, Arrow.DOWN),
        (5, 4, Arrow.DOWN),
    ],


    # ========================================================
    # 第 2 关
    # ========================================================
    #
    # 这一关开始出现箭头之间的遮挡关系。
    #
    2: [
        (0, 2, Arrow.UP),
        (0, 4, Arrow.UP),

        (1, 1, Arrow.LEFT),
        (1, 4, Arrow.RIGHT),

        (2, 3, Arrow.UP),

        (3, 0, Arrow.LEFT),
        (3, 5, Arrow.RIGHT),

        (4, 2, Arrow.DOWN),

        (5, 1, Arrow.DOWN),
        (5, 4, Arrow.DOWN),
    ],


    # ========================================================
    # 第 3 关
    # ========================================================
    #
    # 难度进一步提高。
    #
    # 玩家需要观察箭头方向，
    # 判断哪些箭头会挡住其他箭头。
    #
    3: [
        (0, 1, Arrow.UP),
        (0, 3, Arrow.UP),

        (1, 0, Arrow.LEFT),
        (1, 2, Arrow.DOWN),
        (1, 5, Arrow.RIGHT),

        (2, 4, Arrow.UP),

        (3, 1, Arrow.LEFT),
        (3, 3, Arrow.RIGHT),

        (4, 2, Arrow.DOWN),
        (4, 5, Arrow.RIGHT),

        (5, 0, Arrow.LEFT),
        (5, 4, Arrow.DOWN),
    ],
}


def get_level_data(level_number):
    """
    获取指定关卡的数据。

    参数：
        level_number：关卡编号

    返回：
        一个新的列表，避免直接修改原始关卡数据。
    """

    if level_number not in LEVELS:
        return []

    return LEVELS[level_number].copy()


def create_level(level_number):
    """
    根据关卡编号创建 Arrow 对象。

    例如：

        create_level(1)

    会创建第一关的所有箭头。
    """

    level_data = get_level_data(level_number)

    arrows = []

    for row, col, direction in level_data:
        arrow = Arrow(
            row,
            col,
            direction
        )

        arrows.append(arrow)

    return arrows


def get_level_count():
    """
    获取总关卡数量。
    """

    return len(LEVELS)


def is_valid_level(level_number):
    """
    判断某个关卡是否存在。
    """

    return level_number in LEVELS


def print_level(level_number):
    """
    在控制台打印关卡信息。
    """

    if not is_valid_level(level_number):
        print(f"关卡 {level_number} 不存在")
        return

    print("=" * 40)
    print(f"第 {level_number} 关")
    print("=" * 40)

    for arrow in create_level(level_number):
        print(
            f"位置：({arrow.row}, {arrow.col}) "
            f"方向：{arrow.direction}"
        )

    print("=" * 40)


# ============================================================
# 测试代码
# ============================================================
#
# 直接运行：
#
#     python level.py
#
# 可以看到关卡数据。
#
# 但是正常运行游戏时不会执行这里。
#
# ============================================================

if __name__ == "__main__":

    print("正在测试关卡数据...")

    print(f"共有 {get_level_count()} 个关卡")

    for level_number in range(1, get_level_count() + 1):

        print_level(level_number)

    print("关卡数据测试完成！")