import pandas as pd
import numpy as np
from functools import reduce


def get_kicker_data(df, i):
    kicker_str_list = list()
    primal_str_list = list()
    possible_kicker_list = list()
    primal_type_list = list()

    primal_str = df.loc[i, 'primal_str']
    combo_str = df.loc[i, 'combo_str']
    kicker_str = combo_str.replace(primal_str, '')
    primal_type = df.loc[i, 'primal_type']
    up_str = df.loc[i, 'up_str']
    primal_type = df.loc[i, 'primal_type']

    if df.loc[i, 'kicker_len'] == 1:
        possible_kicker = up_str + kicker_str
        kicker_str_list.append(kicker_str)
        primal_str_list.append(primal_str)
        possible_kicker_list.append(possible_kicker)
        primal_type_list.append(primal_type)
    else:
        kicker_len = df.loc[i, 'kicker_len']
        kicker_type = df.loc[i, 'kicker_type']
        for k in range(kicker_len):
            sub_kicker_str = kicker_str[k * kicker_type:(k + 1) * kicker_type]
            sub_primal_str = primal_str
            if primal_type not in [10, 11]:
                sub_primal_str = primal_str[k * 3:(k + 1) * 3]
            possible_kicker = (up_str + kicker_str).replace(sub_kicker_str, '')
            kicker_str_list.append(sub_kicker_str)
            primal_str_list.append(sub_primal_str)
            possible_kicker_list.append(possible_kicker)
            primal_type_list.append(primal_type)
    data = pd.DataFrame({
        'kicker_str': kicker_str_list,
        'primal_str': primal_str_list,
        'possible_kicker_str': possible_kicker_list,
        'primal_type': primal_type_list
    })
    return data


def get_kicker_data_all(game_data):
    kicker_data = game_data.loc[game_data.kicker_type != 0, :]
    kicker_data = kicker_data.reset_index()
    kicker_data_all = pd.DataFrame()
    for i in range(len(kicker_data)):
        data = get_kicker_data(kicker_data, i)
        kicker_data_all = pd.concat([kicker_data_all, data])
    return kicker_data_all.reset_index().drop('index', axis=1)


def row_to_y(df, i, kicker_out):
    kicker_str = df.loc[i, 'kicker_str']
    y = np.zeros((1, 1), dtype=int)
    if isinstance(kicker_str, str):
        row = kicker_out.loc[kicker_out.kicker == kicker_str, 'kicker_out'].values
        y[0, 0] = row[0]
    return y


def str_to_dict(s):
    card_count = {
        '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, 
        '8': 0, '9': 0, 'T': 0, 'J': 0, 'Q': 0, 
        'K': 0, 'A': 0, '2': 0, 'S': 0, 'B': 0
    }
    for i in s:
        card_count[i] += 1
    return card_count


def row_to_X(df, i):
    kicker_str = df.loc[i, 'kicker_str']
    primal_str = df.loc[i, 'primal_str']
    possible_kicker_str = df.loc[i, 'possible_kicker_str']
    primal_type = df.loc[i, 'primal_type']
    card_pos = {'3': 0, '4': 1, '5': 2, '6': 3, 
                '7': 4, '8': 5, '9': 6, 'T': 7, 
                'J': 8, 'Q': 9, 'K': 10, 'A': 11, 
                '2': 12, 'S': 13, 'B': 14}

    X = np.zeros((1, 8, 15), dtype=int)
    # primal info
    row_pos = {8: 0, 9: 1, 10: 2, 11: 3, 12: 0, 13: 1}[primal_type]
    primal_dict = str_to_dict(primal_str)
    for card, num in primal_dict.items():
        if num > 0:
            col_pos = card_pos[card]
            X[0, row_pos, col_pos] = 1
    # remaining cards info
    possible_kicker_dict = str_to_dict(possible_kicker_str)
    col_pos = list()
    row_pos = list()
    for card, num in possible_kicker_dict.items():
        if num > 0:
            col_pos = card_pos[card]
            row_pos = {1: 4, 2: 5, 3: 6, 4: 7}[num]
            X[0, row_pos, col_pos] = 1
    return X


def get_kicker_sample(df, kicker_out):
    X = reduce(
        lambda x, y: np.concatenate([x, y], axis=0),
        [row_to_X(df, i) for i in range(len(df))])
    y = reduce(
        lambda x, y: np.concatenate([x, y], axis=0),
        [row_to_y(df, i, kicker_out) for i in range(len(df))])
    return X, y



if __name__ == '__main__':
    game_data = pd.read_csv('data/game_data.csv')[0:1000]
    kicker_out = pd.read_csv('data/kicker_out.csv')
    kicker_out.kicker = kicker_out.kicker.astype('str')
    kicker_data_all = get_kicker_data_all(game_data)
    X, y = get_kicker_sample(kicker_data_all, kicker_out)
    print(f'\nShape of X = {X.shape} \nShape of y = {y.shape}')