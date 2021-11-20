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
    HIPPIE: [AHA, BHA, RETINOL, BUFFET],
    ELAA: [AHA, BHA, RETINOL],
    RETINOL: []
}

things = [BUFFET, AHA, BHA, HIPPIE, ELAA, RETINOL]

curr: List[Union[List[str], str]] = []
min_len = math.inf
result = None


def validate() -> bool:
    for conflictor, list_of_conflicts in conflicts.items():
        if conflictor not in things:
            print(f"{conflictor} not in {things}")
            exit(1)
        for conflict in list_of_conflicts:
            if conflict not in things:
                print(f"{conflict} not in {things}")
                exit(1)

def valid(curr):
    for group in curr:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if group[j] in conflicts[group[i]]:
                    return False
                if group[i] in conflicts[group[j]]:
                    return False

    return True

def backtrack(idx):
    if idx == len(things):
        global min_len
        if valid(curr) and len(curr) < min_len:
            min_len = len(curr)
            global result
            result = copy.deepcopy(curr)
        return
    for i in range(len(curr) + 1):
        if i == len(curr):
            curr.append([things[idx]])
            backtrack(idx + 1)
            curr.pop()
        else:
            curr[i].append(things[idx])
            backtrack(idx + 1)
            curr[i].pop()

validate()
backtrack(0)

for line in result:
    print(line)
print(len(result))
