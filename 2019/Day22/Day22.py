from helper import aoc_timer


@aoc_timer
def get_input(path, time=True):
    """Return generator for shuffling techniques."""
    for line in open(path).read().split('\n'):
        t, n = line.rsplit(' ', 1)
        if n == 'stack':
            n = 0
        yield t.split().pop()[:3], int(n)


def get_lcf(technique):
    """
    Observe that each shuffle technique is a linear mapping:
        f(x) = (ax + b) mod m
    where m is the deck length and x is the card position.
    This is called a linear congruential function (LCF). See:
    https://en.wikipedia.org/wiki/Linear_congruential_generator
    Return LCF parameters (a, b) for a shuffle technique.
    """
    t, n = technique
    LCF = {
        'cut': lambda n: (1, -n),
        'inc': lambda n: (n, 0),
        'new': lambda n: (-1, -1)
    }
    return LCF[t](n)


def compose_lcf(f, g, m):
    """
    Compose functions f and g: (f ∘ g)(x) = f(g(x)), where:
        f(x) = ax + b mod m
        g(x) = cx + d mod m
    Return parameters for (f ∘ g)(x)
    """
    a, b = f
    c, d = g
    return (a * c) % m, ((b * c) + d) % m


def exp_lcf(f, m, n):
    """
    Compute result of composing f with itself n times (mod m).
    i.e. functional power / iterated function. See:
    https://en.wikipedia.org/wiki/Function_composition#Functional_powers
    Compute efficiently using exponentiation by squaring.
    This is possible because LCF composition is associative.
    """
    r = (1, 0)    # Identity LCF
    while n > 0:
        if n % 2 == 1:
            r = compose_lcf(r, f, m)
            n -= 1
        f = compose_lcf(f, f, m)
        n //= 2
    return r


def lcf(f, x, m):
    """Apply LCF, f, to a card position, x."""
    a, b = f
    return ((a * x) + b) % m


def reduce_techniques(data, m):
    """Reduce successive shuffle techniques to one LCF."""
    f = get_lcf(next(data))
    for technique in data:
        g = get_lcf(technique)
        f = compose_lcf(f, g, m)
    return f


@aoc_timer
def Day22(data, x, m, n=False):
    """ Part 1:
    Reduce the list of shuffle techniques into a single LCF
    Then we can apply this LCF to a card position, x, to
    calculate its resultant position after the full shuffle.
    """
    f = reduce_techniques(data, m)
    if not n:
        return lcf(f, x, m)

    """ Part 2:
    First we are required to shuffle the deck of m cards n
    times, where m and n are large. We observe that m and n
    are coprime, so we can compose the reduced LCF with itself
    n times to get the resultant LCF for the full shuffle.
    We implement an exponentiation by squaring algorithm to
    efficiently calculate the nth power of the base LCF mod m.
    Require the card number at a given position after the full
    shuffle, effectively the inverse of the part 1 operation.
    Let g(x) = (ax + b) mod m, then the inverse, g'(x) can be
    computed by substitution:
    g(g'(x)) = x
             = (a*g'(x) + b) mod m
    => g'(x) = (x - b)/a mod m
    Division in modular space requires modular multiplicative
    inverse. Python's pow function supports negative exponents
    with three arguments (base**exp % mod) since Python 3.8.
    """
    a, b = exp_lcf(f, m, n)
    return (x - b) * pow(a, -1, m) % m


# %% Output
def main():
    print("AoC 2019\nDay 22")
    p1 = Day22(
        data=get_input('input.txt'),
        x=2019,
        m=10007
    )
    print("Part 1:", p1)
    p2 = Day22(
        data=get_input('input.txt', time=False),
        x=2020,
        m=119315717514047,
        n=101741582076661
    )
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
