from helper import aoc_timer
from collections import Counter, defaultdict, deque
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
    return sum((p - q) ** 2 for p, q in zip(a, b))


def manhattan(a, b):
    '''Return the Manhattan distance between points a and b.'''
    return sum(abs(p - q) for p, q in zip(a, b))


def tri(coords):
    '''Return an integer representation of the triangle traced by coords.'''
    return sum(it.starmap(euc, it.combinations(coords, 2)))


def draw_beacons(beacons):
    '''Render 3D plot of beacons, colour coded by region.'''
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


def inverses(coords):
    '''Return a generator of orientations of coords in 3D space.'''
    x, y, z = coords
    yield from [
        (+x, +y, +z), (+x, -z, +y), (+x, -y, -z), (+x, +z, -y),
        (+y, +x, -z), (+z, +x, +y), (-y, +x, +z), (-z, +x, -y),
        (+y, +z, +x), (-z, +y, +x), (-y, -z, +x), (+z, -y, +x),
        (-x, +y, -z), (-x, +z, +y), (-x, -y, +z), (-x, -z, -y),
        (+y, -x, +z), (-z, -x, +y), (-y, -x, -z), (+z, -x, -y),
        (+y, -z, -x), (+z, +y, -x), (-y, +z, -x), (-z, -y, -x)
    ]


def nth(iterable, n, default=None):
    '''Returns the nth item of the iterable or a default value.'''
    return next(it.islice(iterable, n, None), default)


def nth_triangle(triangle, n, f=orientations):
    return tuple([nth(f(p), n) for p in triangle])


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


def print_dict(dict: dict) -> None:
    for k, v in dict.items():
        print(f'{k}: {v}')


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
        rule, which states that if all sides are equal, the triangles are
        equal.
    6.  For part 1, we count the unique triangles and add the anchors.
    7.  I assume part 2 will require us to actually orient the map. Joy.
    '''
    A = {0: (0, 0, 0)}      # Positions  s: (x, y, z)
    M = defaultdict(set)    # Map        s: {s1, s2, ...}
    S = defaultdict(set)    # Sensors    s: {t1, t1, ..., t12}
    T = defaultdict(list)   # Triangles  t: [(s1, xyz1), (s2, xyz2), ...]
    P = [{} for _ in data]  # Point map  [{t1: xyz1, t2: xyz2, ...}, ...]
    p1 = 0
    for s, beacons in data.items():
        num_anchors = len(beacons) - 24
        anchors, triangles = beacons[:num_anchors], beacons[num_anchors:]
        for t in it.zip_longest(*[iter(triangles)] * 3):
            triangle = tri(t)
            T[triangle].append((s, list(t)))
            S[s].add(triangle)
            P[s][triangle] = t
        p1 += len(anchors)
    p1 += 3 * len(T)

    # TODO: Part 2
    # General idea is to start with scanner 0 and orient all others
    # relative to this one. Do this by applying rotations to triangles
    # until all 12 distances match for all coordinates - this is then
    # the distance between the scanners.
    # Continue via linked scanners, each time orienting relative to
    # scanner 0.

    # Overlapping bounding cubes - four triangles shared between two sensors
    SHARED = {}
    for r, s in it.combinations(S.keys(), 2):
        if len((common_triangles := S[r] & S[s])) == 4:
            M[r].add(s)
            M[s].add(r)
            SHARED[r] = common_triangles
            SHARED[s] = common_triangles
    # print_dict(M)

    # For each overlapping pair of sensors, take one shared triangle and
    # use this to orient the second sensor relative to the first
    Q = deque([(0, 0)])
    while Q:
        s1, k1 = Q.popleft()
        print(f'{s1}: {k1}')
        for triangle_id in SHARED[s1]:
            if triangle_id not in P[s1]:
                continue
            t1 = P[s1][triangle_id]
            for s2 in M[s1]:
                if s2 in A:
                    continue
                if triangle_id not in P[s2]:
                    continue
                # t2 = nth_triangle(X[s2][tid], k1, f=inverses)
                t2 = P[s2][triangle_id]
                dist, k2 = translation(t1, t2)
                if dist is not None:
                    A[s2] = add(A[s1], nth(inverses(dist), k1))
                    Q.append((s2, k2))
    print_dict(A)

    print("old method below")
    D = {}
    for k, v in T.items():
        # print(f'{k}: {v}')
        if len(v) == 1:
            continue
        for (s1, t1), (s2, t2) in it.combinations(v, 2):
            if s2 not in M[s1]:
                continue
            if (s1, s2) in D:
                continue
            if (t := translation(t1, t2)) is not None:
                D[(s1, s2)] = t
    print_dict(D)

    return p1, None


# %% Output
def main():
    print("AoC 2021\nDay 19")
    data = get_input('input.txt')
    data = get_input('sample.txt')  # 79
    # data = get_input('sample2.txt')  # 465
    p1, p2 = Day19(data)
    print("Part 1:", p1)
    print("Part 2:", p2)
    # for _, beacons in data.items():
    #     test_plot(beacons)
    # draw_beacons(data[0])


if __name__ == '__main__':
    main()
