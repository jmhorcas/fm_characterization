from typing import Collection


def int_to_scientific_notation(n: int, precision: int = 2) -> str:
    """Convert a large int into scientific notation.
    
    It is required for large numbers that Python cannot convert to float,
    solving the error `OverflowError: int too large to convert to float`.
    """
    str_n = str(n)
    decimal = str_n[1:precision+1]
    exponent = str(len(str_n) - 1)
    return str_n[0] + '.' + decimal + 'e' + exponent


def get_nof_configuration_as_str(nof_configurations: int, aproximation: bool, nof_cross_tree_constraints: int) -> str:
    return f"{'≤ ' if aproximation and nof_cross_tree_constraints > 0 else ''}{int_to_scientific_notation(nof_configurations) if nof_configurations > 1e6 else nof_configurations}"


def get_ratio(collection1: Collection, collection2: Collection, precision: int = 4) -> float:
    if not collection2:
        return 0.0
    return round(len(collection1) / len(collection2), precision)