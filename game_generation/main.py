from numpy import inf
import numpy as np
import pandas as pd
from hand_card import HandCard
import pickle
from deal import deal
from tree import Node, minimax



with open("call_landlord_model.pkl", 'rb') as file:
    model = pickle.load(file)


def generate_game(game_no):
    # deal cards
    l, p1, p2 = deal(model)
    landlord = HandCard(l.card_dict, 'dict', is_landlord=True)
    peasant1 = HandCard(p1.card_dict, 'dict',)
    peasant2 = HandCard(p2.card_dict, 'dict')
    # construct game tree
    node = Node(current=landlord, down=peasant1, up=peasant2)
    game_data = pd.DataFrame()
    for i in range(100):
        # calculate next step
        _, node = minimax(node, 3, -inf, +inf)
        if node is None or node.is_over():
            break
        if node.pre1_combo is None:
            combo_str = ''
            primal_type = 0
            kicker_len = 0
            kicker_type = 0
        else:
            combo_str = node.pre1_combo.__str__()
            primal_type = node.pre1_combo.get_primal_type()
            kicker_len = 0 if node.pre1_combo.kicker is None else node.pre1_combo.kicker.kicker_len
            kicker_type = node.pre1_combo.get_kicker_type()
        player_no = i % 3 + 1
        round_no = (i // 3) + 1
        current_str = node.current.__str__()
        up_str = node.up.__str__()
        down_str = node.down.__str__()
        data = pd.DataFrame({
            'game_no': [game_no], 
            'player_no': [player_no], 
            'round_no': [round_no], 
            'primal_type': [primal_type], 
            'kicker_type': [kicker_type], 
            'kicker_len': [kicker_len],
            'combo_str': [combo_str],
            'current_str': [current_str],
            'up_str': [up_str],
            'down_str': [down_str]
        })
        game_data = pd.concat([game_data, data])
    return game_data


game_data_all = pd.DataFrame()
for game_no in range(20):
    print(game_no)
    game_data = generate_game(game_no + 1)
    game_data_all = pd.concat([game_data_all, game_data])

game_data_all.to_csv('sample_game_data.csv', index=False)