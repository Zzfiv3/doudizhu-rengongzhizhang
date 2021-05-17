import numpy as np


class Cards:
    def __init__(self, arg=None, ctype=None) -> None:
        self.card_dict = {
            '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, 
            '8': 0, '9': 0, 'T': 0, 'J': 0, 'Q': 0, 
            'K': 0, 'A': 0, '2': 0, 'S': 0, 'B': 0
        }
        if ctype == 'dict':
            self.card_dict = arg
            self.card_num = np.array(list(arg.values()))
        elif ctype == 'card':
            for card in arg:
                self.card_dict[card] += 1
            self.card_num = np.array(list(self.card_dict.values()))
        elif ctype == 'num':
            self.card_num = arg
            for i, key in enumerate(self.card_dict.keys()):
                self.card_dict[key] += self.card_num[i]
        else:
            self.card_num = np.zeros(15, dtype=int)

    def __str__(self):
        return ''.join([k * v for k, v in self.card_dict.items()])

    def __sub__(self, other):
        result = Cards()
        for card in self.card_dict.keys():
            result.card_dict[card] = self.card_dict[card]
            result.card_dict[card] -= other.card_dict[card]
        result.card_num = np.array(list(result.card_dict.values()))
        return result

    def __len__(self):
        return sum(self.card_num)

    def add(self, other):
        for k, v in other.card_dict.items():
            self.card_dict[k] += v

    def sub(self, other):
        for k, v in other.card_dict.items():
            self.card_dict[k] -= v

    def call_landlord_prob(self, model):
        prob = model.predict_proba(self.card_num.reshape((1, -1)))
        return prob[0, 1]