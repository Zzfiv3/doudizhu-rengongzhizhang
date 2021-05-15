import numpy as np
from functools import reduce
from itertools import combinations
from game_generation.Combo import Combo, Primal, Kicker
from game_generation.cards import Cards


# hc = HandCard([1,2,334,])
# combo = Combo([ssss])
# hc.get_next_combo(combo)


class HandCard(Cards):
    def __init__(self, arg=None, ctype=None, is_landlord=False) -> None:
        Cards.__init__(self, arg, ctype)
        self.is_landlord = is_landlord

    def __sub__(self, other):
        result = HandCard(is_landlord=self.is_landlord)
        for card in self.card_dict.keys():
            result.card_dict[card] = self.card_dict[card]
            result.card_dict[card] -= other.card_dict[card]
        result.card_num = np.array(list(result.card_dict.values()))
        return result

    def get_next_combo(self, pre_combo=None):
        if pre_combo is None:
            return self.get_all_combo()
        next_combo_list = list()
        for combo in self.get_all_combo():
            if combo > pre_combo:
                next_combo_list.append(combo)
        return next_combo_list

    def get_all_combo(self):
        combo_list = list()
        for primal in self.get_all_primal():
            if primal.kicker_type is not None:
                kicker_list = self.get_kicker(primal)
                if kicker_list is None:
                    continue
                for kicker in kicker_list:
                    combo = Combo(primal, kicker)
                    combo_list.append(combo)
            else:
                combo = Combo(primal)
                combo_list.append(combo)
        return combo_list

    def get_all_primal(self):
        solo = self.get_simple(1)
        solo_chain = self.get_chain(1, 5)
        pair = self.get_simple(2)
        pair_chain = self.get_chain(2, 3)
        trio = self.get_simple(3)
        trio_chain = self.get_chain(3, 2)
        bomb = self.get_bomb()
        trio_solo = self.get_simple(3, kicker_type='solo')
        trio_pair = self.get_simple(3, kicker_type='pair')
        four_solo = self.get_simple(4, kicker_type='solo')
        four_pair = self.get_simple(4, kicker_type='pair')
        plane_solo = self.get_chain(3, 2, kicker_type='solo')
        plane_pair = self.get_chain(3, 2, kicker_type='pair')
        primal_all = reduce(
            lambda x, y: x + y,
            [solo, solo_chain, pair, pair_chain, trio, trio_chain, bomb, trio_solo,
             trio_pair, four_solo, four_pair, plane_solo, plane_pair])
        return primal_all

    def get_kicker(self, primal):
        cards_left = self - primal
        kicker_card_num = 1 if primal.kicker_type == 'solo' else 2
        pos = np.where(cards_left.card_num >= kicker_card_num)[0]
        if len(pos) < primal.kicker_len:
            return None
        comb = combinations(pos, primal.kicker_len)
        kicker_list = list()
        for c in comb:
            kicker_array = np.zeros(15, dtype=int)
            kicker_array[np.array(c)] = kicker_card_num
            kicker = Kicker(
                kicker_array, 'num',
                kicker_type=primal.kicker_type,
                kicker_len=primal.kicker_len
            )
            kicker_list.append(kicker)
        return kicker_list

    def get_simple(self, card_num, kicker_type=None):
        primal_list = list()
        for i, num in enumerate(self.card_num):
            primal_array = np.zeros(15, dtype=int)
            if num >= card_num:
                primal_array[i] = card_num
                if kicker_type is None:
                    primal = Primal(primal_array, 'num', 1, card_num)
                else:
                    primal = Primal(primal_array, 'num', 1, card_num, kicker_type, 1)
                primal_list.append(primal)
        return primal_list

    def get_chain(self, card_num, min_len, kicker_type=None):
        pos = np.where(self.card_num[0:12] >= card_num)[0]
        primal_list = list()
        for i in range(0, len(pos)):
            for j in range(i, len(pos)):
                if j - i == pos[j] - pos[i] and j - i >= min_len - 1:
                    primal_array = np.zeros(15, dtype=int)
                    primal_array[pos[i]:pos[j] + 1] = card_num
                    if kicker_type is None:
                        primal = Primal(primal_array, 'num', j - i + 1, card_num)
                    else:
                        primal = Primal(primal_array, 'num', j - i + 1, card_num, kicker_type, j - i + 1)
                    primal_list.append(primal)
        return primal_list

    def get_bomb(self):
        primal_list = list()
        # normal bomb
        for i, num in enumerate(self.card_num):
            primal_array = np.zeros(15, dtype=int)
            if num >= 4:
                primal_array[i] = 1
                primal = Primal(primal_array, 'num', bomb=True)
                primal_list.append(primal)
        # two jokers
        if self.card_num[-1] == 1 and self.card_num[-2] == 1:
            primal_array = np.zeros(15, dtype=int)
            primal_array[-1] = 1
            primal_array[-2] = 1
            primal = Primal(primal_array, 'num', bomb=True)
            primal_list.append(primal)
        return primal_list
