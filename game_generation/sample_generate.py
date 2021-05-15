import pandas as pd
import numpy as np
import torch
from functools import reduce


def str_to_dict(s):
    card_count = {
        '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, 
        '8': 0, '9': 0, 'T': 0, 'J': 0, 'Q': 0, 
        'K': 0, 'A': 0, '2': 0, 'S': 0, 'B': 0
    }
    for i in s:
        card_count[i] += 1
    return card_count


def row_to_X(data, row_index):
    card_pos = {'3': 0, '4': 1, '5': 2, '6': 3, 
                '7': 4, '8': 5, '9': 6, 'T': 7, 
                'J': 8, 'Q': 9, 'K': 10, 'A': 11, 
                '2': 12, 'S': 13, 'B': 14}
    primal_str = data.loc[row_index, 'primal_str']
    primal_type = data.loc[row_index, 'primal_type']
    combo_str = data.loc[row_index, 'combo_str']
    up_str = data.loc[row_index, 'up_str']
    current_str = data.loc[row_index, 'current_str']
    down_str = data.loc[row_index, 'down_str']

    # get all cards in hand
    all_cards_in_hand = np.zeros((20, 15, 1), dtype=int)
    if isinstance(combo_str, str) and isinstance(up_str, str):
        card_dict = str_to_dict(combo_str + up_str)
        for card, num in card_dict.items():
            if num == 0:
                continue
            col = card_pos[card]
            row = {1: 16, 2: 17, 3: 18, 4: 19}[num]
            all_cards_in_hand[row, col, 0] = 1
    # print(all_cards_in_hand)

    # all the cards have not been seen
    all_cards_not_seen = np.zeros((20, 15, 1), dtype=int)
    if isinstance(current_str, str) and isinstance(down_str, str):
        card_dict = str_to_dict(current_str + down_str)
        for card, num in card_dict.items():
            if num == 0:
                continue
            col = card_pos[card]
            row = {1: 16, 2: 17, 3: 18, 4: 19}[num]
            all_cards_not_seen[row, col, 0] = 1
    # print(all_cards_not_seen)

    # last six round
    last_six_round = np.zeros((20, 15, 18), dtype=int)
    current_row = row_index
    channel_index = 17
    while current_row >= 0 and channel_index >= 0:
        primal_str = data.loc[current_row, 'primal_str']
        primal_type = data.loc[current_row, 'primal_type']
        if isinstance(primal_str, str):
            for i in primal_str:
                last_six_round[primal_type, card_pos[i], channel_index] = 1
        current_row -= 1
        channel_index -= 1

    # all cards before previous six round
    all_cards_before = np.zeros((20, 15, 1), dtype=int)
    if current_row > 0:
        cards_played = ''
        for i in range(current_row):
            primal_str = data.loc[i, 'primal_str']
            if isinstance(primal_str, str):
                cards_played += primal_str
        card_dict = str_to_dict(cards_played)
        for card, num in card_dict.items():
            if num == 0:
                continue
            col = card_pos[card]
            row = {1: 16, 2: 17, 3: 18, 4: 19}[num]
            all_cards_before[row, col, 0] = 1

    # construct X
    X = np.concatenate([
        all_cards_before, last_six_round, 
        all_cards_not_seen, all_cards_in_hand
    ], axis=2).reshape((20, 15, 21, 1))

    return X


def row_to_y(data, row_index, primal_out):
    primal_str = data.loc[row_index, 'primal_str']
    y = np.zeros((len(primal_out), 1))
    hot_pos = 0 if not isinstance(primal_str, str) \
        else primal_out.loc[primal_out.primal == primal_str, 'out_code']
    y[hot_pos] = 1
    return y.reshape((309, 1, 1))


def get_game_sample(game_data, primal_out):
    X = reduce(lambda x, y: np.concatenate([x, y], axis=3),
               [row_to_X(game_data, i) for i in range(len(game_data))])
    y = reduce(lambda x, y: np.concatenate([x, y], axis=2),
               [row_to_y(game_data, i, primal_out) for i in range(len(game_data))])
    return X, y


def get_sample_all(data, primal_out):
    game_data = data.loc[data.game_no == 1, :]
    X_all, y_all = get_game_sample(game_data, primal_out)
    for game_no in np.unique(data.game_no)[1:]:
        game_data = data.loc[data.game_no == game_no, :].reset_index()
        X, y = get_game_sample(game_data, primal_out)
        X_all = np.concatenate([X_all, X], axis=3)
        y_all = np.concatenate([y_all, y], axis=2)
        print(f'Finished converting {game_no} games!')
    return X_all, y_all


if __name__ == '__main__':
    data = pd.read_csv('sample_game_data.csv')
    primal_out = pd.read_csv('primal_out.csv')
    X, y = get_sample_all(data, primal_out)
    print(f'\nShape of X = {X.shape} \nShape of y = {y.shape}')