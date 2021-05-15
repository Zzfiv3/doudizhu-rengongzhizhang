import numpy as np
from numpy import inf
from game_generation.Combo import Combo


class Node:
    def __init__(self, current, down, up, pre1_combo=None, pre2_combo=None) -> None:
        self.current = current
        self.down = down
        self.up = up
        self.pre1_combo = pre1_combo
        self.pre2_combo = pre2_combo
        self.CARD_VALUE = np.array(list(range(1, 14)) + [20, 30])


    def get_childern(self):
        children = list()
        pre_combo = self.pre1_combo if self.pre1_combo is not None else self.pre2_combo
        next_combo_list = self.current.get_next_combo(pre_combo)
        if len(next_combo_list) < 1:    
            child = Node(current=self.down, down=self.up, up=self.current, 
                         pre1_combo=None, pre2_combo=self.pre1_combo)
            children.append(child)
            return children
        for combo in next_combo_list:
            child = Node(current=self.down, down=self.up, up=self.current - combo, 
                         pre1_combo=combo, pre2_combo=self.pre1_combo)
            children.append(child)
        return children

    def get_state_value(self):
        peasant_score = 0
        for player in [self.current, self.down, self.up]:
            if player.is_landlord:
                landlord_score = self.get_socore(player)
            else:
                peasant_score += self.get_socore(player)
        return peasant_score/2 - landlord_score

    def get_socore(self, player):
        card_value = np.sum(player.card_num * self.CARD_VALUE)
        if np.sum(player.card_num) == 0:
            return +inf
        return card_value/np.sum(player.card_num)
    

    def is_over(self):
        return len(self.current) == 0 or len(self.down) == 0 or len(self.up) == 0

    def __str__(self) -> str:
        s = 'Up: \t{} \nCurr: \t{} \nDown: \t{} \nPre1: \t{}'.format(
            self.up, self.current, self.down, self.pre1_combo)
        return s


def minimax(node, depth, alpha, beta):
    if depth == 0 or node.is_over():
        return node.get_state_value(), node
    if not node.current.is_landlord:
        max_value = -inf
        max_child = None
        for child in node.get_childern():
            value, _ = minimax(child, depth - 1, alpha, beta)
            if value > max_value:
                max_value = value
                max_child = child
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return max_value, max_child
    else:
        min_value = +inf
        min_child = None
        for child in node.get_childern():
            value, _ = minimax(child, depth - 1, alpha, beta)
            if value < min_value:
                min_value = value
                min_child = child
            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_value, min_child


    

    


    

    
