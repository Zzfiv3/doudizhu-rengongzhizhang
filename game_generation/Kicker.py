class Kicker:
    """
    One of the two basic components of a combo
    """
    def __init__(self, card, kicker_type):
        """
        parameters
        ----------
        card : list(str)
            The unique card pattern of a kicker, if kicker_type equals 'solo', then it 
            represent exactly the cards in a kicker, e.g. for kicker '34', it should be
            ['3', '4']; if kicker_type equals to 'dual', it represent the unique pattern
            of each pair, e.g. for kicker '445566', it should be ['4', '5', '6']

        kicker_type : str, {'solo', 'dual'}
            The type of kicker, if 'solo', each element in 'card' appears only once in the 
            kicker, if 'dual', each element in 'card' appears twice in the kicker.
        """
        self.card = card
        self.kicker_type = kicker_type

    