class Primal:
    def __init__(self, card, card_num):
        """
        One of the two basic components of a combo

        parameters
        ----------
        card : list(str)
            The unique card pattern of a primal, e.g. for combo '334455', it should be
            ['3', '4', '5']

        card_num : int
            the number of each unique card pattern in parameter 'card', e.g. for combo
            '99TTJJQQKK', the 'card' parameter should be ['9', 'T', 'J', 'Q', 'K'] while 
            the 'card_num' parameter should be 2
        """
        self.card = card
        self.card_num = card_num
    