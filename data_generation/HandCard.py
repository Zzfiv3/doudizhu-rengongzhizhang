import numpy as np
from Poker import deal
from itertools import combinations


class HandCard:
    def __init__(self, hand_card):
        """
        Parameters
        ----------
        hand_card : ndarray, required
            The initial hand card of one player, the shape of the array should be (15,)
            Each of the element records the number a kind of card, (3-10, J, Q, K, ACE, 
            TWO, BLACK/RED JOKER)
        """
        self.handCard = np.array(hand_card)

    def get_solo_combo(self, chain=False):
        """
        Get all possible 'solo' combos.

        Parameters
        ----------
        chain : boolean, optional, default=False
            Whether the combo is a chain of solos.
        
        Returns
        -------
        numpy.ndarray
            a 2d array contains all possible solo combos, the shape should be (x, 15), 
            where x equals the number of possible combos and each line represents one
            possible combo. Return None if there such kind of combo cannot be found.
        """
        solo_pos = np.where(self.handCard >= 1)[0]
        if len(solo_pos) < 1:
            return None
        if not chain:
            solo_combo = np.zeros((len(solo_pos), 15))
            solo_combo[range(len(solo_pos)), solo_pos] = 1
            return solo_combo
        else:
            if len(solo_pos) < 5:
                return None
            else:
                chain_pos = list()
                for i in range(len(solo_pos)):
                    for j in range(i, len(solo_pos)):
                        if solo_pos[j] - solo_pos[i] == j - i and j - i >= 4:
                            chain_pos.append(solo_pos[i:(j + 1)])
                if len(chain_pos) < 1:
                    return None
                solo_combo = np.zeros((len(chain_pos), 15), dtype=int)
                for i, pos in enumerate(chain_pos):
                    solo_combo[i, pos] = 1
                return solo_combo

    def get_pair_combo(self, chain=False):
        """
        Get all possible 'pair' combos.

        Parameters
        ----------
        chain : boolean, optional, default=False
            Whether the combo is a chain of pairs.
        
        Returns
        -------
        numpy.ndarray
            a 2d array contains all possible solo combos, the shape should be (x, 15), 
            where x equals the number of possible combos and each line represents one
            possible combo. Return None if there such kind of combo cannot be found.
        """
        pair_pos = np.where(self.handCard >= 2)[0]
        pair_pos = pair_pos[pair_pos < 12]
        if len(pair_pos) < 1:
            return None
        if not chain:
            pair_combo = np.zeros((len(pair_pos), 15))
            pair_combo[range(len(pair_pos)), pair_pos] = 1
            return pair_combo
        else:
            if len(pair_pos) < 3:
                return None
            else:
                chain_pos = list()
                for i in range(len(pair_pos)):
                    for j in range(i, len(pair_pos)):
                        if pair_pos[j] - pair_pos[i] == j - i and j - i >= 2:
                            chain_pos.append(pair_pos[i:(j + 1)])
                if len(chain_pos) < 1:
                    return None
                pair_combo = np.zeros((len(chain_pos), 15), dtype=int)
                for i, pos in enumerate(chain_pos):
                    pair_combo[i, pos] = 2
                return pair_combo

    def get_trio_combo(self, chain=False, kicker_type=None):
        """
        Get all possible 'trio' combos.

        Parameters
        ----------
        chain : boolean, optional, default=False
            Whether the combo is a chain of pairs.
        kicker_type : str, optional, default=None
            'solo', 'pair', or None. The type of kicker(s), None means trio with no 
            kickers.

        Returns
        -------
        numpy.ndarray
            a 2d array contains all possible solo combos, the shape should be (x, 15), 
            where x equals the number of possible combos and each line represents one
            possible combo. Return None if there such kind of combo cannot be found.
        """
        trio_pos = np.where(self.handCard >= 3)[0]
        if len(trio_pos) < 1:
            return None
        if not chain:
            if kicker_type is None:
                trio_combo = np.zeros((len(trio_pos), 15), dtype=int)
                trio_combo[range(len(trio_pos)), trio_pos] = 3
                return trio_combo
            trio_combo_list = list()
            for tPos in trio_pos:
                card_left = self.handCard.copy()
                card_left[tPos] -= 3
                kicker_card_num = 1 if kicker_type == 'solo' else 2
                kicker_pos = np.where(card_left >= kicker_card_num)[0]
                if len(kicker_pos) < 1:
                    continue
                trio_combo = np.zeros((len(kicker_pos), 15), dtype=int)
                trio_combo[range(len(kicker_pos)), kicker_pos] = kicker_card_num
                trio_combo[range(len(kicker_pos)), tPos] = 3
                trio_combo_list.append(trio_combo)
            if len(trio_combo_list) < 1:
                return None
            return np.concatenate(trio_combo_list, axis=0)
        else:
            if len(trio_pos) < 2:
                return None
            trio_chain_list = list()
            for i in range(len(trio_pos)):
                for j in range(i, len(trio_pos)):
                    if trio_pos[j] - trio_pos[i] == j - i and j - i >= 1:
                        trio_chain_list.append(trio_pos[i:(j + 1)])
            trio_combo_list = list()
            for chainPos in trio_chain_list:
                card_left = self.handCard.copy()
                card_left[chainPos] -= 3
                kicker_num = len(chainPos)
                kicker_card_num = 1 if kicker_type == 'solo' else 2
                kicker_pos = np.where(card_left >= kicker_card_num)[0]
                if len(kicker_pos) < kicker_num:
                    continue
                kicker_list = list(combinations(kicker_pos, kicker_num))
                trio_combo = np.zeros((len(kicker_list), 15), dtype=int)
                for i, kicker in enumerate(kicker_list):
                    trio_combo[i, list(kicker)] = kicker_card_num
                    trio_combo[i, chainPos] = 3
                trio_combo_list.append(trio_combo)
            if len(trio_combo_list) < 1:
                return None
            return np.concatenate(trio_combo_list, axis=0)

    def get_four_combo(self, kicker_type=None):
        """
        Get all possible 'Four' combos.

        Parameters
        ----------
        kicker_type : str, optional, default=None
            'solo', 'pair', or None. The type of kicker(s), None means four with no 
            kickers, i.e., a bomb.

        Returns
        -------
        numpy.ndarray
            a 2d array contains all possible solo combos, the shape should be (x, 15), 
            where x equals the number of possible combos and each line represents one
            possible combo. Return None if there such kind of combo cannot be found.
        """
        four_pos = np.where(self.handCard >= 4)[0]
        if len(four_pos) < 1:
            return None
        else:
            if kicker_type is None:
                four_combo = np.zeros((len(four_pos), 15), dtype=int)
                four_combo[range(len(four_combo)), four_pos] = 4
                return four_combo
            four_combo_list = list()
            for pos in four_pos:
                card_left = self.handCard.copy()
                card_left[pos] = 0
                kicker_card_num = 1 if kicker_type == 'solo' else 2
                kicker_pos = np.where(card_left >= kicker_card_num)[0]
                if len(kicker_pos) < 2:
                    continue
                kicker_list = list(combinations(kicker_pos, 2))
                four_combo = np.zeros((len(kicker_list), 15), dtype=int)
                for i, kicker in enumerate(kicker_list):
                    four_combo[i, list(kicker)] = kicker_card_num
                    four_combo[i, pos] = 4
                four_combo_list.append(four_combo)
            if len(four_combo_list) < 1:
                return None
            return np.concatenate(four_combo_list, axis=0)

    def get_rocket(self):
        """
        Get all possible 'Rocket' combos.

        Returns
        -------
        numpy.ndarray
            a 2d array contains all possible solo combos, the shape should be (x, 15), 
            where x equals the number of possible combos and each line represents one
            possible combo. Return None if there such kind of combo cannot be found.
        """
        if self.handCard[-1] > 0 and self.handCard[-2] > 0:
            rocket = np.zeros((1, 15), dtype=int)
            rocket[0, -2:-1] = 1
            return rocket
        else:
            return None

    def get_all_combo(self):
        """
        get all possible combos
        :return:
        """
        solo = self.get_solo_combo()
        soloChain = self.get_solo_combo(chain=True)
        pair = self.get_pair_combo()
        pairChain = self.get_pair_combo(chain=True)
        trio = self.get_pair_combo()
        trioChain = self.get_trio_combo(chain=True)
        trioSolo = self.get_trio_combo(kicker_type='solo')
        trioPair = self.get_trio_combo(kicker_type='pair')
        trioChainSolo = self.get_trio_combo(chain=True, kicker_type='solo')
        trioChainPair = self.get_trio_combo(chain=True, kicker_type='pair')
        fourSolo = self.get_four_combo(kicker_type='solo')
        fourPair = self.get_four_combo(kicker_type='pair')
        bomb = self.get_four_combo()
        rocket = self.get_rocket()
        passNext = np.zeros((1, 15), dtype=int)
        combo_list = [solo, soloChain, pair, pairChain,
                      trio, trioChain, trioSolo, trioPair,
                      trioChainSolo, trioChainPair, fourSolo,
                      fourPair, bomb, rocket, passNext]
        combo_list = [i for i in combo_list if i is not None]
        return np.concatenate(combo_list, axis=0).astype(int)


a, b, c = deal()
hc = HandCard(a)
print(hc.get_all_combo().shape)
