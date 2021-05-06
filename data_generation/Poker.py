import numpy as np
from functools import reduce


def deal():
    normal = np.ones(13, dtype=int) * 4
    joker = np.ones(2, dtype=int)
    poker = np.concatenate([normal, joker])

    p1_left = 20
    p2_left = 17
    p3_left = 17

    p1_card = np.zeros(len(poker), dtype=int)
    p2_card = np.zeros(len(poker), dtype=int)
    p3_card = np.zeros(len(poker), dtype=int)

    i = 0
    while i < len(poker):
        p1 = np.random.randint(0, min(p1_left, poker[i]) + 1)
        p2 = np.random.randint(0, min(p2_left, poker[i] - p1) + 1)
        p3 = poker[i] - p2 - p1
        if p3_left < p3:
            continue
        p1_left -= p1
        p2_left -= p2
        p3_left -= p3
        p1_card[i] = p1
        p2_card[i] = p2
        p3_card[i] = p3
        i += 1

    return p1_card, p2_card, p3_card

a, b, c = deal()
print(a, b, c, sep='\n')