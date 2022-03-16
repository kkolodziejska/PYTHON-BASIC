"""
Write function which receives list of integers. Calculate power of each integer and
subtract difference between original previous value and it's power. For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3])
    [1, 4, 7]
"""
from typing import List


def calculate_power_with_difference(ints: List[int]) -> List[int]:
    return [ints[i] ** 2 - (ints[i-1] ** 2 - ints[i-1])
            if i > 0 else ints[i] ** 2 for i, _ in enumerate(ints)]
