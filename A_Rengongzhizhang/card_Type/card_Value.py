import numpy as np
from A_Rengongzhizhang.card_Rule.cards import _is_consequent
from A_Rengongzhizhang.card_Rule.cards import *
from A_Rengongzhizhang.card_Rule.cards import cards_view, card_to_di

"""
用来计算
"""

ROCKET_BIT = 0
INVALID_BIT = -1
PASS = -2


def _one(di, value) -> int:
    """
    从di中选取一张的卡牌，
    e.g.输出5105  5表示顺子五张牌，1表示一张牌，5表示最大值是到5
    """
    if _is_consequent(di[1], 5):
        return len(di[1]) * 1000 + 100 + value
    return INVALID_BIT


def _two(di, value) -> int:
    """
    用于计算连对，具体可看test_combo_two里面.
    """
    if _is_consequent(di[2], 3) and not di[1]:
        return len(di[2]) * 1000 + 200 + value
    return INVALID_BIT


def _three(di, value) -> int:
    # 飞机 或3带1 或3带2
    if _is_consequent(di[3], 1) or len(di[3]) == 1 and di[3][0] == CARD_2:
        if not di[1]:  # di[1]中是空的
            # 无翼
            if not di[2]:  # di[2]中是空的
                return len(di[3]) * 1000 + 300 + value

            # 大翼 或3带2
            if len(di[2]) == len(di[3]):
                return 200000 + len(di[3]) * 1000 + 300 + value

        # 小翼 或3带1
        if len(di[1]) + len(di[2]) * 2 == len(di[3]):  # 为什么要di[2]*2来比较呢？
            return 100000 + len(di[3]) * 1000 + 300 + value
    return INVALID_BIT


def _four(di, value) -> int:
    if di[3]:
        return INVALID_BIT

    if len(di[4]) == 1:

        # 4带2单
        if len(di[1]) + len(di[2]) * 2 == 2:  # 为什么要用di[2]?
            return 101400 + value
        # 4带2双
        elif len(di[2]) == 2 and not di[1]:
            return 201400 + value

    return INVALID_BIT


MAX_COUNT_STRATEGIES: tuple = (_one, _two, _three, _four)  # 元组，定义后不可修改

