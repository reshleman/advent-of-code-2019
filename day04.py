import itertools

INPUT = range(367479, 893698+1)


def has_repeated_digit(num):
    return any(
        len(list(g)) > 1
        for _, g
        in itertools.groupby(str(num))
    )


def has_paired_digit(num):
    return any(
        len(list(g)) == 2
        for _, g
        in itertools.groupby(str(num))
    )


def has_monotonic_digits(num):
    return all(
        int(i) <= int(j)
        for i, j
        in zip(str(num), str(num)[1:])
    )


def part1():
    return len([
        i for i in INPUT
        if has_monotonic_digits(i) and has_repeated_digit(i)
    ])


def part2():
    return len([
        i for i in INPUT
        if has_monotonic_digits(i) and has_paired_digit(i)
    ])


if __name__ == '__main__':
    print(part1())
    print(part2())
