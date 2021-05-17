from cards import Cards
import numpy as np


class Primal(Cards):
    def __init__(self, arg=None, ctype=None, chain_len=None, num=None, 
            kicker_type=None, kicker_len=None, bomb=False) -> None:
        Cards.__init__(self, arg, ctype)
        self.num = num
        self.chain_len = chain_len
        self.bomb = bomb
        self.kicker_type = kicker_type
        self.kicker_len = kicker_len

        

class Kicker(Cards):
    def __init__(self, arg, ctype, kicker_type, kicker_len) -> None:
        Cards.__init__(self, arg, ctype)
        self.kicker_type = kicker_type
        self.kicker_len = kicker_len


class Combo(Cards):
    def __init__(self, primal=None, kicker=None) -> None:
        self.primal = primal
        self.kicker = kicker
        if primal is None:
            self.primal = Primal()
        if kicker is not None:
            Cards.__init__(self, self.primal.card_num + kicker.card_num, 'num')
        else:
            Cards.__init__(self, self.primal.card_num, 'num')
    
    def get_kicker_type(self):
        primal_type = self.get_primal_type()
        if primal_type in [8, 10, 12]:
            return 1  # solo kicker
        elif primal_type in [9, 11, 13]:
            return 2  # pair kicker
        else:
            return 0  # no kicker

    def get_primal_type(self):
        if self.primal.bomb:
            return 7  # bomb
        if self.primal.kicker_type is None:
            if self.primal.num == 1:
                if self.primal.chain_len == 1:
                    return 1  # solo
                elif self.primal.chain_len >= 5:
                    return 2  # solo chain
            elif self.primal.num == 2:
                if self.primal.chain_len == 1:
                    return 3  # pair
                elif self.primal.chain_len >= 3:
                    return 4   # pair chain
            elif self.primal == 3:
                if self.primal.chain_len == 1:
                    return 5  # trio
                elif self.primal.chain_len >= 2:
                    return 6  # trio chain
        else:
            if self.primal.num == 3 and self.primal.chain_len == 1:
                if self.kicker.kicker_type == 'solo':
                    return 8  # trio solo
                elif self.kicker.kicker_type == 'pair':
                    return 9  # trio pair
            elif self.primal.num == 4 and self.primal.chain_len == 1:
                if self.kicker.kicker_type == 'solo':
                    return 10  # four solo
                elif self.kicker.kicker_type == 'pair':
                    return 11  # four pair
            elif self.primal.num == 3 and self.primal.chain_len > 1:
                if self.kicker.kicker_type == 'solo':
                    return 12  # plane solo
                elif self.kicker.kicker_type == 'pair':
                    return 13  # plane pair


    def comparable(self, other):
        if self.primal.bomb or other.primal.bomb:
            return True
        else:
            return self.primal.chain_len == other.primal.chain_len and self.primal.num == other.primal.num

    def __gt__(self, other):
        if not self.comparable(other):
            return False
        if self.primal.bomb and not other.primal.bomb:
            return True
        elif not self.primal.bomb and other.primal.bomb:
            return False
        elif self.primal.bomb and other.primal.bomb:
            if self.primal.card_dict['S'] > 0:
                return True
            elif other.primal.card_dict['S'] > 0:
                return False
        self_pos = np.where(self.primal.card_num > 0)[0]
        other_pos = np.where(other.primal.card_num > 0)[0]
        return self_pos[0] > other_pos[0]





    
