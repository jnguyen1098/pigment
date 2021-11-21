#!/usr/bin/env python3
"""Skincare partition algorithm."""

import copy
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Result:
    """Reference container for mutating results."""

    min_len: int = 9999999999
    best: List[List[Any]] = field(default_factory=list)


def valid(curr_partition: List[List[Any]], conflicts: Dict[Any, Any]) -> bool:
    """Determine if partition has any conflicts."""
    for part in curr_partition:
        for i, elem in enumerate(part):
            for j in range(i + 1, len(part)):
                if elem in conflicts and part[j] in conflicts[elem]:
                    return False
                if part[j] in conflicts and elem in conflicts[part[j]]:
                    return False
    return True


def backtrack(
    idx: int,
    curr: List[List[Any]],
    conflicts: Dict[Any, Any],
    ingredient_names: List[Any],
    result: Result,
) -> None:
    """Recursively iterate through every partition and validate fitness."""
    if idx == len(ingredient_names):
        if valid(curr, conflicts) and len(curr) < result.min_len:
            result.min_len = len(curr)
            result.best = copy.deepcopy(curr)
        return
    for i in range(len(curr) + 1):
        if i == len(curr):
            curr.append([ingredient_names[idx]])
            backtrack(idx + 1, curr, conflicts, ingredient_names, result)
            curr.pop()
        else:
            curr[i].append(ingredient_names[idx])
            backtrack(idx + 1, curr, conflicts, ingredient_names, result)
            curr[i].pop()


def get_best_partition(conflicts: Dict[Any, Any]) -> List[List[Any]]:
    """Get best partition using known conflicts."""
    ingredient_names = []
    for conflictor, list_of_conflicts in conflicts.items():
        ingredient_names.append(conflictor)
        for conflict in list_of_conflicts:
            ingredient_names.append(conflict)

    result = Result()
    ingredient_names = list(OrderedDict((name, None) for name in ingredient_names))
    curr: List[List[Any]] = []
    backtrack(0, curr, conflicts, ingredient_names, result)
    return result.best


def create_gv(conflicts: OrderedDict[Any, Any], partition: List[List[Any]]) -> None:
    """Create GraphViz DOT graph to STDOUT."""
    colours = ["red", "orange", "gold", "lawngreen", "turquoise", "magenta"]
    print("graph G {")
    for line in partition:
        try:
            colour = colours.pop()
        except IndexError:
            print("Not enough colours to pop!", file=sys.stderr)
            sys.exit(1)
        for node in line:
            print(f'    "{node}" [style=filled, fillcolor={colour}]')
    print()

    for node, edges in conflicts.items():
        for edge in edges:
            print(f'    "{node}" -- "{edge}"')
    print("}")


def main() -> None:
    """Execute main flow."""
    buffet = "Buffet + Copper Peptides"
    aha = "Alpha Hydroxy Acids"
    bha = "Beta Hydroxy Acids"
    hippie = "Mad Hippie"
    elaa = "Ethylated Ascorbic Acid"
    retinol = "Retinol"

    conflicts = OrderedDict(
        (
            (buffet, [aha, bha, hippie, elaa, retinol]),
            (aha, [retinol]),
            (bha, [retinol]),
            (hippie, [aha, bha, retinol]),
            (elaa, [aha, bha, retinol]),
        )
    )

    best_partition = get_best_partition(conflicts)

    for part in best_partition:
        print(part)
    print()

    create_gv(conflicts, best_partition)


if __name__ == "__main__":
    main()
