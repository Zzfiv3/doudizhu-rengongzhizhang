class Combo:
    def __init__(self, primal, kicker):
        """
        parameters
        ----------
        primal : Primal object, the primal part of a combo
        kicker : Kicker object, the kicker part of a combo
        """
        self.primal = primal
        self.kicker = kicker
        self.combo_dict = {
            '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, 
            '8': 0, '9': 0, 'T': 0, 'J': 0, 'Q': 0, 
            'K': 0, 'A': 0, '2': 0, 'S': 0, 'B': 0}
        for card in self.primal.card:
            self.combo_dict[card] += self.primal.card_num
        for card in self.kicker.card:
            card_num = 1 if self.kicker.kicker_type == 'solo' else 2
            self.combo_dict[card] += card_num
    
    
    def get_combo_str(self):
        """
        Output the combo in the form of a string

        returns
        -------
        str : the ouput string of the combo
        """
        return ''.join([c * n for c, n in self.combo_dict.items()])
    





    
