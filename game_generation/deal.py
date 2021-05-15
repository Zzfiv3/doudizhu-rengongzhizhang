import pickle
import numpy as np
from game_generation.Combo import Cards
from functools import reduce


def get_init_dict():
    card_dict = {
        '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, 
        '8': 0, '9': 0, 'T': 0, 'J': 0, 'Q': 0, 
        'K': 0, 'A': 0, '2': 0, 'S': 0, 'B': 0
    }
    return card_dict


def call_landlord_prob(cards_array):
    with open("call_landlord_model.pkl", 'rb') as file:
        pickle_model = pickle.load(file)
    call_prob = pickle_model.predict_proba(cards_array)
    return call_prob[0, 1]


def deal(landlord_model):
    poker_dict = {
        '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, 
        '8': 4, '9': 4, 'T': 4, 'J': 4, 'Q': 4, 
        'K': 4, 'A': 4, '2': 4, 'S': 1, 'B': 1
    }
    poker = [[k] * v for k, v in poker_dict.items()]
    poker_array = np.array(reduce(lambda x, y: x + y, poker))
    np.random.shuffle(poker_array)
    p1 = Cards(poker_array[0:17], 'card')
    p2 = Cards(poker_array[17:34], 'card')
    p3 = Cards(poker_array[34:51], 'card')
    public = Cards(poker_array[51:54], 'card')
    player_list = [p1, p2, p3]
    prob_list = [p.call_landlord_prob(landlord_model) for p in player_list]
    landlord_index = np.argmax(prob_list)
    landlord = player_list.pop(landlord_index)
    landlord.add(public)
    return landlord, player_list[0], player_list[1]

