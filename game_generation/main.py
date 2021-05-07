from Kicker import Kicker
from Primal import Primal
from Combo import Combo


k = Kicker(card=['3', '4'], kicker_type='solo')
p = Primal(card=['5'], card_num=3)
c = Combo(primal=p, kicker=k)
print(c.get_combo_str())

