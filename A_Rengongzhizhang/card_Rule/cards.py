import numpy as np
from typing import Tuple, List, Union

from A_Rengongzhizhang.card_Rule import *
from A_Rengongzhizhang.card_Rule import CARD_VIEW


def has_rocket(card: Union[np.ndarray, List[int]]) -> bool:
    """
    用来判断是否存在大小王
    :param card
    :return: 输出是True或False
    """
    if len(card >= 2) and card[-2] == CARD_G0:
        return True
    else:
        return False


def card_lt2(card: Union[np.ndarray, List[int]]):
    """
    将比2小的牌提取出来，先默认牌是已经排好序的
    :param card:
    :return:比2小的牌
    """
    card_less_than_2 = np.searchsorted(card, CARD_2)  # 默认card是已经排序好了的
    return card[:card_less_than_2]


def card_lt2_two_g(card: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    将牌分解成小于2，等于2，大于2的牌
    :param card:
    :return:一个元组，分别是<2,=2,>2的牌
    """
    return card[card < CARD_2], card[card == CARD_2], card[card > CARD_2]


def card_split(card: Union[np.ndarray, List[int]]) -> List[np.ndarray]:
    """
    分解不连续的牌，可见dong_test中相关代码理解
    :param card:
    :return:分解出的牌
    """
    split_card = [i + 1 for i in range(len(card) - 1) if card[i] + 1 < card[i + 1]]
    return np.split(card, split_card)


def card_to_di(card: np.ndarray) -> Tuple[Dict[int, list], int, int]:
    """
    获取不同种类卡牌数量
    :param card:
    :return: 不同的牌型，最多的牌型，最多牌型里的最大值
    """
    di = {1: [], 2: [], 3: [], 4: []}
    if card.size == 0:
        return di, 0, 0

    count: int = 0
    former_card = card[0]
    for card in card:
        if card == former_card:
            count += 1
        else:
            di[count].append(former_card)
            count = 1
            former_card = card
    di[count].append(former_card)

    max_count: int = 0
    value: int = 0
    for k, v in di.items():
        if v:
            max_count = k
            value = max(v)
    return di, max_count, value


def card_to_suffix_di(card: np.ndarray) -> Tuple[Dict[int, list], int, int]:
    """
    获取不同的牌型的数量，比如3 3 3 可以在单，双和飞机中
    :param card:
    :return:
    """
    di, max_count, value = card_to_di(card)
    di[1].extend(di[2])
    di[1].extend(di[3])
    di[2].extend(di[3])
    di[1].sort()
    di[2].sort()
    return di, max_count, value


def cards_view(cards: np.ndarray) -> str:
    """
    获取牌的字符串形式，映射方式见 CARD_VIEW
    :param cards:
    :return: 牌的字符串输出形式
    """
    result: str = ''
    for i in cards:
        result += CARD_VIEW[i]

    return result


def _is_consequent(card,min_len:int) -> bool:
    """
    用来验证牌的序列是否合法，例如，3 4 5 6 7是合法的，3 4 5 6是不合法的, 66 77 88合法 77 88 不合法
    :param card:
    :param min_len:用来定义最小的长度，单张顺子是5，对子顺是3
    :return:是否合法
    """
    if card[-1] >= CARD_2 or len(card) < min_len:
        return False
    mininest = card[0]
    for i in range(0,len(card)):
        if card[i] - i != mininest:
            return False
    return True