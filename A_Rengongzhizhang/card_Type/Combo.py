from __future__ import annotations

import numpy as np

from typing import Union, List
from A_Rengongzhizhang.card_Rule import *
from A_Rengongzhizhang.card_Rule.cards import cards_view, card_to_di
from A_Rengongzhizhang.card_Type.card_Value import MAX_COUNT_STRATEGIES

ROCKET_BIT = 0
INVALID_BIT = -1
PASS = -2

"""
    卡牌组合类

    bit_info是一个取值范围在[-1, 300000)上的整数。
    卡牌组合非法时bit_info = -1，王炸 bit_info = 0。
    记bit_info = a5 a4 a3 a2 a1 a0
    其它情况规则如下：
    a1a0: bit_info % 100 = 组合用于比较大小的值。组合类型为N带M时，取N中的最大值。其它时候取所有牌最大值。
    a2  : bit_info // 100 % 10 = max(牌i的数量)。例如`AAA44`时取3，`667788`时取2
    a4a3: bit_info // 1000 % 100 = count(max(牌i的数量))。例如`667788`取3，`333444JK`取2
    a5:   bit_info // 100000 = N带M中的M。例如`66`取0，`333J`取1。
    """


class Combo:
    def __calc_bit_info(self) -> int:

        self._cards.sort()

        # 单，对，三带0，炸弹
        seq_len = len(np.unique(self._cards))  # unique是除去其中重复的元素并且按照元素由大到小返回一个新的数组
        if seq_len == 1:
            return 1000 + 100 * len(self._cards) + self._cards[0]

        # 王炸
        if len(self._cards) == 2:
            return ROCKET_BIT if np.sum(self._cards) == CARD_G1 + CARD_G0 else INVALID_BIT

        di, max_count, value = card_to_di(self._cards)

        return MAX_COUNT_STRATEGIES[max_count - 1](di, value)  # 输出[第几个函数](里面的di和value值)

    def __init__(self):
        self._cards_view: str = ''
        self._cards: np.ndarray = np.array([])
        self._bit_info: int = PASS

    def pass_(self) -> None:
        """
        不出牌。空的手牌
        """
        self._cards_view: str = ''
        self._cards: np.ndarray = np.array([])
        self._bit_info: int = PASS

    def is_valid(self) -> bool:
        """
        本次出牌是否合法
        """
        return self._bit_info != INVALID_BIT

    def is_not_empty(self) -> bool:
        """
        本次出牌是否不为空过
        """
        return self._bit_info >= 0

    def is_rocket(self) -> bool:
        """
        是否为王炸
        """
        return self._bit_info == ROCKET_BIT

    def is_solo(self) -> bool:
        """
        是否为单 a4 a3 a2 = 011
        @see _bit_info
        """
        return self._bit_info // 100 % 1000 == 11

    def is_pair(self) -> bool:
        """
        是否为对子 a4 a3 a2 = 012
        @see _bit_info
        """
        return self._bit_info // 100 % 1000 == 12

    @property
    def take_kind(self) -> int:
        """
        带牌的种类 a5
        """
        return self._bit_info // 100000

    def is_trio(self) -> bool:
        """
        是否为三 a4 a3 a2 = 013
        """
        return self._bit_info // 100 % 1000 == 13

    def is_single(self) -> bool:
        """是否为单牌 a4 a3 a2 = 01"""
        return self._bit_info // 1000 % 100 == 1

    @property
    def seq_len(self) -> int:
        """
        连续的长度 a4 a3
        """
        return self._bit_info // 1000 % 100

    @property
    def main_kind(self) -> int:
        """
        单种牌或序列类型 a2
        """
        return self._bit_info // 100 % 10

    @property
    def value(self) -> int:
        """返回Combo的价值，可用于相同类型比大小"""
        return self._bit_info % 100

    @property
    def cards_view(self) -> str:
        """
        卡牌在控制台上的视图，每张牌之间用空格分开
        """
        return self._cards_view

    @cards_view.setter
    def cards_view(self, v: Union[str, List[str]]):
        if len(v) == 0:
            self.pass_()
            return

        if type(v) is str:
            v = v.split()
        try:
            self._cards = np.array([VIEW_TO_VALUE[c.upper()] for c in v])
        except KeyError:
            self._bit_info = INVALID_BIT
            return

        self._cards.sort()
        self._bit_info = self.__calc_bit_info()
        self._cards_view = cards_view(self._cards)

    @property
    def cards(self) -> np.ndarray:
        """
        卡牌实际值数组
        """
        return self._cards

    @cards.setter
    def cards(self, value: Union[List[int], np.ndarray]):
        if len(value) == 0:
            self.pass_()
        else:
            self._cards: np.ndarray = np.array(value)
            self._cards.sort()
            self._cards_view = cards_view(self._cards)
            self._bit_info = self.__calc_bit_info()

    def is_bomb(self) -> bool:
        """
        判断该bit_info是否代表炸弹（不含王炸）
        @see: Combo
        @return: 是: True; 否: False
        """
        return self._bit_info // 100 == 14

    def _bit_value_gt(self, other: Combo) -> bool:
        """self的价值是否大于other"""
        return self._bit_info % 100 > other._bit_info % 100

    def _bit_type_eq(self, other: Combo) -> bool:
        """两种Combo类型是否相等"""
        return self._bit_info // 100 == other._bit_info // 100

    def __gt__(self, other: Combo):
        if self._bit_info == ROCKET_BIT:
            return True
        if other._bit_info == ROCKET_BIT:
            return False
        if self.is_bomb():
            return not other.is_bomb() or self._bit_value_gt(other)

        return self._bit_type_eq(other) and self._bit_value_gt(other)

    def __repr__(self):
        return 'Combo: ' + self._cards_view
