from typing import Dict

'''
将牌与数字对应起来，其中CARD_G0和CARD_G1分别代表小王与大王
'''
CARD_3, CARD_4, CARD_5, CARD_6, CARD_7 = 1, 2, 3, 4, 5
CARD_8, CARD_9, CARD_10, CARD_J, CARD_Q = 6, 7, 8, 9, 10
CARD_K, CARD_A, CARD_2, CARD_G0, CARD_G1 = 11, 12, 13, 14, 15

CARD_VIEW: dict = {
    1: '3 ', 2: '4 ', 3: '5 ', 4: '6 ', 5: '7 ',
    6: '8 ', 7: '9 ', 8: '10 ', 9: 'J ', 10: 'Q ',
    11: 'K ', 12: 'A ', 13: '2 ', 14: 'B ', 15: 'G '
}

VIEW_TO_VALUE: Dict[str, int] = {
    '3': CARD_3, '4': CARD_4, '5': CARD_5, '6': CARD_6, '7': CARD_7,
    '8': CARD_8, '9': CARD_9, '10': CARD_10, 'J': CARD_J,
    'Q': CARD_Q, 'K': CARD_K, 'A': CARD_A, '2': CARD_2, 'B': CARD_G0,
    'G': CARD_G1
}