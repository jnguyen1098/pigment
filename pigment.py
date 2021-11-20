#!/usr/bin/env python3

import copy
import math
from collections import OrderedDict
from typing import List, Union

curr = None
min_len = None
result = None

def valid(curr, conflicts):
    for group in curr:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if group[i] in conflicts and group[j] in conflicts[group[i]]:
                    return False
                if group[j] in conflicts and group[i] in conflicts[group[j]]:
                    return False

    return True

def backtrack(idx, conflicts, ingredient_names):
    if idx == len(ingredient_names):
        global min_len
        if valid(curr, conflicts) and len(curr) < min_len:
            min_len = len(curr)
            global result
            result = copy.deepcopy(curr)
        return
    for i in range(len(curr) + 1):
        if i == len(curr):
            curr.append([ingredient_names[idx]])
            backtrack(idx + 1, conflicts, ingredient_names)
            curr.pop()
        else:
            curr[i].append(ingredient_names[idx])
            backtrack(idx + 1, conflicts, ingredient_names)
            curr[i].pop()


def initialize(conflicts):
    global CONFLICTS
    global curr
    global min_len
    global result

    CONFLICTS = conflicts
    curr = []
    min_len = math.inf
    result = None


def get_partitions(conflicts):
    initialize(conflicts)
    ingredient_names = []
    for conflictor, list_of_conflicts in CONFLICTS.items():
        ingredient_names.append(conflictor)
        for conflict in list_of_conflicts:
            ingredient_names.append(conflict)

    ingredient_names = list(OrderedDict((name, None) for name in ingredient_names))
    backtrack(0, conflicts, ingredient_names)
    return result


def main():
    BUFFET = "Buffet + Copper Peptides"
    AHA = "Alpha Hydroxy Acids"
    BHA = "Beta Hydroxy Acids"
    HIPPIE = "Mad Hippie"
    ELAA = "Ethylated Ascorbic Acid"
    RETINOL = "Retinol"

    conflicts = OrderedDict((
        (BUFFET, [AHA, BHA, HIPPIE, ELAA, RETINOL]),
        (AHA, [RETINOL]),
        (BHA, [RETINOL]),
        (HIPPIE, [AHA, BHA, RETINOL]),
        (ELAA, [AHA, BHA, RETINOL]),
    ))
    partitions = get_partitions(conflicts)
    for line in partitions:
        print(line)
    print(len(partitions))


if __name__ == "__main__":
    main()
