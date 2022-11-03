from math import ceil


def max_yantras(gnosis: int) -> int:
    return 1 + ceil(gnosis / 2)


def highest_arcana_max(gnosis: int) -> int:
    return min(2 + ceil(gnosis / 2), 5)


def other_arcana_max(gnosis: int) -> int:
    return min(2 + gnosis // 2, 5)


def paradox_per_reach(gnosis: int) -> int:
    return (gnosis + 1) // 2
