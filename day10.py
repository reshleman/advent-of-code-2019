import collections
import functools
import itertools
import math

INPUT = """
#..#....#...#.#..#.......##.#.####
#......#..#.#..####.....#..#...##.
.##.......#..#.#....#.#..#.#....#.
###..#.....###.#....##.....#...#..
...#.##..#.###.......#....#....###
.####...##...........##..#..#.##..
..#...#.#.#.###....#.#...##.....#.
......#.....#..#...##.#..##.#..###
...###.#....#..##.#.#.#....#...###
..#.###.####..###.#.##..#.##.###..
...##...#.#..##.#............##.##
....#.##.##.##..#......##.........
.#..#.#..#.##......##...#.#.#...##
.##.....#.#.##...#.#.#...#..###...
#.#.#..##......#...#...#.......#..
#.......#..#####.###.#..#..#.#.#..
.#......##......##...#..#..#..###.
#.#...#..#....##.#....#.##.#....#.
....#..#....##..#...##..#..#.#.##.
#.#.#.#.##.#.#..###.......#....###
...#.#..##....###.####.#..#.#..#..
#....##..#...##.#.#.........##.#..
.#....#.#...#.#.........#..#......
...#..###...#...#.#.#...#.#..##.##
.####.##.#..#.#.#.#...#.##......#.
.##....##..#.#.#.......#.....####.
#.##.##....#...#..#.#..###..#.###.
...###.#..#.....#.#.#.#....#....#.
......#...#.........##....#....##.
.....#.....#..#.##.#.###.#..##....
.#.....#.#.....#####.....##..#....
.####.##...#.......####..#....##..
.#.#.......#......#.##..##.#.#..##
......##.....##...##.##...##......
""".strip().split('\n')

ASTEROID = '#'

Point = collections.namedtuple('Point', ['x', 'y'])


def asteroid_positions():
    return [
        Point(x, y)
        for y, row in enumerate(INPUT)
        for x, val in enumerate(row)
        if val == ASTEROID
    ]


def angle(a, b):
    return math.atan2(b.x-a.x, b.y-a.y)


def distance(a, b):
    return math.sqrt((b.x-a.x)**2 + (b.y-a.y)**2)


def part1():
    asteroids = asteroid_positions()
    max_asteroids = -float('inf')

    for a in asteroids:
        angles = set()

        for b in asteroids:
            if a == b:
                continue

            angles.add(angle(a, b))

        if len(angles) > max_asteroids:
            max_asteroids = len(angles)
            point = a

    return max_asteroids, point


def part2():
    _, origin = part1()

    asteroids_by_angle = collections.defaultdict(list)

    for point in asteroid_positions():
        if origin == point:
            continue

        asteroids_by_angle[angle(origin, point)].append(point)

    for asteroids in asteroids_by_angle.values():
        asteroids.sort(key=functools.partial(distance, origin))

    num_zapped = 0
    last_zapped = None
    for _, asteroids in itertools.cycle(sorted(asteroids_by_angle.items(), reverse=True)):
        try:
            last_zapped = asteroids.pop(0)
        except IndexError:
            continue

        num_zapped += 1
        if num_zapped == 200:
            break

    return last_zapped.x * 100 + last_zapped.y


if __name__ == '__main__':
    print(part1())
    print(part2())
