import numpy as np
from itertools import combinations


l = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
for i in range(0, len(l) - 2):
    for j in range(i + 2, len(l)):
        a = ''.join([l[k] * 2 for k in range(i, j + 1)])
        if len(a) <= 20:
            print(a)



# l = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
# for i in range(0, len(l) - 4):
#     for j in range(i + 4, len(l)):
#         for num in range(i, j + 1):
#             print(l[num], sep='', end='')
#         print()