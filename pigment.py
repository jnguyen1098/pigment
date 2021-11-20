#!/usr/bin/env python3

import copy
import math
from typing import List, Union

BUFFET = "Buffet + Copper Peptides"
AHA = "Alpha Hydroxy Acids"
BHA = "Beta Hydroxy Acids"
HIPPIE = "Mad Hippie"
ELAA = "Ethylated Ascorbic Acid"
RETINOL = "Retinol"

conflicts = {
    BUFFET: [AHA, BHA, HIPPIE, ELAA, RETINOL],
    AHA: [RETINOL],
    BHA: [RETINOL],
    HIPPIE: [AHA, BHA, RETINOL],
    ELAA: [AHA, BHA, RETINOL],
}

ingredient_names = []

for conflictor, list_of_conflicts in conflicts.items():
    ingredient_names.append(conflictor)
    for conflict in list_of_conflicts:
        ingredient_names.append(conflict)

ingredient_names = list(set(ingredient_names))

curr: List[Union[List[str], str]] = []
min_len = math.inf
result = None

def valid(curr):
    for group in curr:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if group[i] in conflicts and group[j] in conflicts[group[i]]:
                    return False
                if group[j] in conflicts and group[i] in conflicts[group[j]]:
                    return False

    return True

def backtrack(idx):
    if idx == len(ingredient_names):
        global min_len
        if valid(curr) and len(curr) < min_len:
            min_len = len(curr)
            global result
            result = copy.deepcopy(curr)
        return
    for i in range(len(curr) + 1):
        if i == len(curr):
            curr.append([ingredient_names[idx]])
            backtrack(idx + 1)
            curr.pop()
        else:
            curr[i].append(ingredient_names[idx])
            backtrack(idx + 1)
            curr[i].pop()

backtrack(0)

for line in result:
    print(line)
print(len(result))
