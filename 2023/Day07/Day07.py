# %% Day 07
from helper import aoc_timer
from collections import Counter


T = [
    lambda h: len(set(h)) == 5,
    lambda h: len(set(h)) == 4,
    lambda h: all(v == 2 for _, v in Counter(h).most_common(2)),
    lambda h: set(Counter(h).values()) == {3, 1},
    lambda h: set(Counter(h).values()) == {3, 2},
    lambda h: 4 in Counter(h).values(),
    lambda h: len(set(h)) == 1
]


@aoc_timer
def get_input(path: str) -> list[tuple[str, int]]:
    return [(hand, int(bid)) for hand, bid in
            [line.split() for line in open(path).read().splitlines()]]


def hand_type(hand: str, wildcard: str | None = None) -> int:
    '''
    Determine the hand type allowing for wildcard replacements. The optimal
    wildcard selection will always correspond to the most common non-wildcard
    card in the hand, assuming one exists. The resulting hand type is
    unaffected by ties for the most common non-wildcard card.
    Returns the integer rank of the resulting hand type, where 0 is weakest
    (high card) and 6 is strongest (five of a kind). Returns 0 where a hand
    type cannot be determined.
    '''
    if wildcard is not None and hand != wildcard * 5:
        repl, _ = Counter(hand.replace(wildcard, '')).most_common(1).pop()
        hand = hand.replace(wildcard, repl)
    for t, f in enumerate(T):
        if f(hand):
            return t
    return 0


def hand_strength(hand: str, card_strengths: dict[str, int]) -> tuple[int]:
    '''
    Return a tuple of integers representing the hand strength as dictated by
    the `card_strenghts` mapping. This strength metric is used for the
    secondary ordering rule applied where two hands have the same hand type.
    '''
    return tuple(card_strengths[c] for c in hand)


@aoc_timer
def solve(data: list[tuple[str, int]],
          order: str = '234567889TJQKA',
          wildcard: str | None = None) -> int:
    C = {c: idx for idx, c in enumerate(order)}
    H = [(hand_type(hand, wildcard), hand_strength(hand, C), bid)
         for hand, bid in data]
    return sum(rank * bid for rank, (*_, bid) in enumerate(sorted(H), start=1))


def main() -> None:
    print("AoC 2023\nDay 07")
    data = get_input('input.txt')
    print("Part 1:", solve(data))
    print("Part 2:", solve(data, order='J23456789TQKA', wildcard='J'))


if __name__ == '__main__':
    main()
