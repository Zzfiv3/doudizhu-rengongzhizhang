import numpy as np
from Primal import Primal



class HandCard:
    def __init__(self, card_dict):
        """
        parameters
        ----------
        card_dict : dict(str : int)
            A dictionary that stores the number of different kinds of cards
        """
        self.card_dict = card_dict
        self.card_array = np.array(list(card_dict.values()))
        self.card_names = np.array(list(card_dict.keys()))

    
    def get_possible_primal(self, card_num, chain=False):
        """
        Get all possible primal

        parameters
        ----------
        card_num : int
            the number of each unique card in the primal, e.g. for primal '333', card_num
            equals to 3, while for primal '34567', card_num equals to 1
        chain : boolean, optional, default=False
            whether the primal is in the form of a chain, e.g. for primal '333444', '667788', 
            and '45678', is_chain equals to True, while for primal '4444', '3', and 'KK', 
            is_chain equals to False.

        returns
        -------
        list(Primal)
            A list of Primal object, each represents a possible primal.
        """
        primals = list()
        if not chain:
            for c, n in self.card_dict.items():
                if n >= card_num:
                    primals.append(Primal([c], card_num))
        else:
            card_array = self.card_array[:12]
            pos = np.where(card_array >= card_num)[0]
            min_len = {1: 5, 2: 3, 3: 2, 4: 2}[card_num]
            for i, p1 in enumerate(pos):
                for j, p2 in enumerate(pos):
                    if j - i == p2 - p1 and j - i >= min_len - 1:
                        primal = Primal(self.card_names[p1:(p2 + 1)], card_num)
                        primals.append(primal)
        return primals
        

    def get_possible_kicker(self, primal):
        """
        Get all possible kickers given a primal

        parameters
        ----------
        primal : Primal object
            The given primal

        returns
        -------
        list(Kicker)
            A list of Kicker object, each represents a possible kicker.
        """
        # TODO
        pass


card_dict = {
    '3': 2, '4': 3, '5': 3, '6': 3, '7': 1, 
    '8': 1, '9': 2, 'T': 2, 'J': 2, 'Q': 0, 
    'K': 0, 'A': 0, '2': 0, 'S': 0, 'B': 0}
hc = HandCard(card_dict)
primal_list = hc.get_possible_primal(3, chain=True)
for p in primal_list:
    print(p.card, p.card_num)

