import math
from typing import Any


def powerset(s: set[Any]) -> set[set[Any]]:
    """The Power set P(S) of a set S is the set of all subsets of S."""
    power_sets = set()
    set_size = len(s)
    sets = list(s)
    pow_set_size = int(math.pow(2, set_size))
    for counter in range(0, pow_set_size):
        current_set = set()
        for j in range(0, set_size):
            if (counter & (1 << j)) > 0:
                current_set.add(sets[j])
        power_sets.add(frozenset(current_set))
    return power_sets
