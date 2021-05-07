class Combo:
    def __init__(self, primal, kicker):
        self.primal = primal
        self.kicker = kicker

    def get_combo_dict(self):
        combo_dict = {
            '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, 
            '8': 0, '9': 0, 'T': 0, 'J': 0, 'Q': 0, 
            'K': 0, 'A': 0, '2': 0, 'S': 0, 'B': 0}
        for card in self.primal.card:
            combo_dict[card] += self.primal.card_num
        for card in self.kicker.card:
            combo_dict[card] += 1 if self.kicker.kicker_type == 'solo' else 2

    def get_combo_str(self):
        combo_str = ''
        for card, card_num in self.get_combo_dict().items():
            combo_str += card * card_num
        return combo_str




    
