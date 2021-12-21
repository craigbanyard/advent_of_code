from helper import aoc_timer
from collections import defaultdict, deque
import itertools as it
from matplotlib import pyplot as plt


@aoc_timer
def get_input(path):
    S = {}
    for idx, group in enumerate(open(path).read().split('\n\n')):
        _, *coords = group.splitlines()
        S[idx] = sorted([tuple(map(int, c.split(','))) for c in coords],
                        key=lambda x: corner(x))
    return S


def corner(a):
    '''This is just disgusting.'''
    T = 200
    x, y, z = a
    if x < -T:
        if y < -T:
            if z < -T:
                return 1
            if z > T:
                return 2
        if y > T:
            if z < -T:
                return 3
            if z > T:
                return 4
    if x > -T:
        if y < -T:
            if z < -T:
                return 5
            if z > T:
                return 6
        if y > T:
            if z < -T:
                return 7
            if z > T:
                return 8
    return 0


def add(a, b):
    '''Return the sum of the vectors a and b.'''
    return tuple((p + q) for p, q in zip(a, b))


def sub(a, b):
    '''Return the result of subtracting vector b from vector a.'''
    return tuple((p - q) for p, q in zip(a, b))


def euc(a, b):
    '''Return the sqaure of the Euclidean distance between points a and b.'''
    return sum(map(lambda d: pow(d, 2), sub(a, b)))


def manhattan(a, b):
    '''Return the Manhattan distance between points a and b.'''
    return sum(map(abs, sub(a, b)))


def tri(coords):
    '''Return an integer representation of the triangle traced by coords.'''
    return sum(it.starmap(euc, it.combinations(coords, 2)))


def draw_beacons(beacons):
    '''Render 3D plot of beacons, colour-coded by region.'''
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    colours = ['r', 'g', 'b', 'c', 'm', 'y', 'darkorange', 'lime', 'k']

    anchors = len(beacons) - 3 * 8
    assert 0 <= anchors <= 3, len(beacons)
    xs, ys, zs = zip(*beacons[:anchors])
    ax.scatter(xs, ys, zs, color=colours[-1])

    triangles = beacons[anchors:]
    for idx in range(8):
        xs, ys, zs = zip(*triangles[idx * 3:(idx + 1) * 3])
        ax.scatter(xs, ys, zs, color=colours[idx])

    plt.show()


def orientations(coords):
    '''Return a generator of orientations of coords in 3D space.'''
    x, y, z = coords
    yield from [
        (+x, +y, +z), (+x, +z, -y), (+x, -y, -z), (+x, -z, +y),
        (+y, +x, -z), (+y, +z, +x), (+y, -x, +z), (+y, -z, -x),
        (+z, +x, +y), (+z, +y, -x), (+z, -x, -y), (+z, -y, +x),
        (-x, +y, -z), (-x, +z, +y), (-x, -y, +z), (-x, -z, -y),
        (-y, +x, +z), (-y, +z, -x), (-y, -x, -z), (-y, -z, +x),
        (-z, +x, -y), (-z, +y, +x), (-z, -x, +y), (-z, -y, -x)
    ]


def nth(iterable, n, default=None):
    '''Returns the nth item of the iterable or a default value.'''
    return next(it.islice(iterable, n, None), default)


def nth_triangle(triangle, n):
    return tuple([nth(orientations(p), n) for p in triangle])


def translation(a, b):
    '''
    Return the (x, y, z) translation that maps triangle a
    onto triangle b, along with the index of the required
    rotation operation to achieve this mapping.
    '''
    # Fix first triangle, permute vertices of second triangle
    for triangle in it.permutations(b, 3):
        # Apply the same rotation to each of the 3 new points
        for k in range(24):
            b = nth_triangle(triangle, k)
            # Construct set of (x, y, z) distances between points
            D = {tuple((n - m) for n, m in zip(p1, p2))
                 for p1, p2 in zip(a, b)}
            if len(D) == 1:
                # We are in the correct orientation
                return D.pop(), k
    return None, None


@aoc_timer
def Day19(data):
    '''
    Assumptions from plotting input:
    1.  Each scanner detects eight triangles of beacons, one in each of
        the eight corners of its bounding cube.
    2.  Each scanner also detects a small number of 'anchor' beacons,
        which are more central in its bounding cube.
    3.  Two scanners' bounding boxes overlap such that the same four
        triangles (12 beacons) are visible to both scanners.
    4.  A scanner can never detect another scanner's 'anchor' beacons.
    5.  We can determine the overlapping triangles via the SSS congruence
        rule, which states that if two triangles have matching side
        lengths, the triangles are equal (congruent).
    6.  For part 1, we count the unique triangles and add the anchors.
    7.  Part 2 requires us to actually orient the map. Joy.
    '''
    A = {0: (0, 0, 0)}      # Sensor positions  s: (x, y, z)
    M = defaultdict(set)    # Overlap map       s: {s1, s2, ...}
    S = defaultdict(set)    # Sensor FoV        s: {t1, t1, ..., t12}
    T = set()               # Unique triangles  {t1, t2, ...}
    P = [{} for _ in data]  # Triangle coords   [{t1: xyz1, t2: xyz2, ...}, ...]
    p1 = 0
    for s, beacons in data.items():
        num_anchors = len(beacons) - 24
        anchors, triangles = beacons[:num_anchors], beacons[num_anchors:]
        for t in it.zip_longest(*[iter(triangles)] * 3):
            triangle = tri(t)
            T.add(triangle)
            S[s].add(triangle)
            P[s][triangle] = t
        p1 += len(anchors)
    p1 += 3 * len(T)

    # Overlapping bounding cubes - four triangles shared between two sensors
    B = defaultdict(set)
    for r, s in it.combinations(S.keys(), 2):
        if len((common_triangles := S[r] & S[s])) == 4:
            M[r].add(s)
            M[s].add(r)
            B[r] |= common_triangles
            B[s] |= common_triangles

    # For each overlapping pair of sensors, take one shared triangle
    # and use this to orient the second sensor relative to the first.
    # If this can't be done, move to the next shared triangle.
    Q = deque([(0, 0)])
    while Q:
        s1, k1 = Q.popleft()
        for triangle_id in B[s1]:
            t1 = nth_triangle(P[s1][triangle_id], k1)
            for s2 in M[s1]:
                if s2 in A:
                    continue
                if triangle_id not in P[s2]:
                    continue
                t2 = P[s2][triangle_id]
                dist, k2 = translation(t1, t2)
                if dist is not None:
                    A[s2] = add(A[s1], dist)
                    Q.append((s2, k2))
    p2 = max(it.starmap(manhattan, it.combinations(A.values(), 2)))

    return p1, p2


# %% Output
def main():
    print("AoC 2021\nDay 19")
    data = get_input('input.txt')
    p1, p2 = Day19(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == '__main__':
    main()
