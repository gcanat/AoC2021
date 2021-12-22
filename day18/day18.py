import sys
import math
from functools import reduce


def parse_numbers(lines):
    for line in lines:
        it = iter(line)
        if next(it) != '[':
            raise ValueError
        yield parse_number_rec(it)


def parse_number_rec(it):
    c = next(it)
    if c == '[':
        left = parse_number_rec(it)
        c = next(it)
    else:
        left, c = parse_number_regular(c, it)
    if c != ',':
        raise ValueError
    c = next(it)
    if c == '[':
        right = parse_number_rec(it)
        c = next(it)
    else:
        right, c = parse_number_regular(c, it)
    if c != ']':
        raise ValueError
    return (left, right)


def parse_number_regular(c, it):
    n = 0
    while c in '0123456789':
        n *= 10
        n += int(c, 10)
        c = next(it)
    return n, c


def add_numbers(a, b):
    return reduce_number((a, b))


def reduce_number(n):
    reduced = True
    while reduced:
        n, reduced, *_ = explode_rec(n, 0)
        if not reduced:
            n, reduced = split_rec(n)
    return n


def explode_rec(n, level):
    if not isinstance(n, int):
        l, r = n
        if level >= 4:
            return 0, True, l, r
        else:
            l, reduced, expl, expr = explode_rec(l, level + 1)
            if reduced:
                if expr != 0:
                    r = add_left(r, expr)
                    expr = 0
            else:
                r, reduced, expl, expr = explode_rec(r, level + 1)
                if reduced:
                    if expl != 0:
                        l = add_right(l, expl)
                        expl = 0
            if reduced:
                return (l, r), True, expl, expr
    return n, False, 0, 0


def add_left(n, m):
    if isinstance(n, int):
        return n + m
    else:
        a, b = n
        return add_left(a, m), b


def add_right(n, m):
    if isinstance(n, int):
        return n + m
    else:
        a, b = n
        return a, add_right(b, m)


def split_rec(n):
    if isinstance(n, int):
        if n >= 10:
            a = n // 2
            return (a, n - a), True
    else:
        l, r = n
        l, reduced = split_rec(l)
        if not reduced:
            r, reduced = split_rec(r)
        if reduced:
            return (l, r), True
    return n, False


def number_magnitude(n):
    if isinstance(n, int):
        return n
    l, r = n
    return 3 * number_magnitude(l) + 2 * number_magnitude(r)


def part1(in_file):
    with open(in_file, 'r') as f:
        numbers = parse_numbers(map(str.strip, f))
        numbers = map(reduce_number, numbers)
        res = reduce(add_numbers, numbers)
    print(res)
    m = number_magnitude(res)
    print(m)


def part2(in_file):
    with open(in_file, 'r') as f:
        numbers = parse_numbers(map(str.strip, f))
        numbers = list(map(reduce_number, numbers))
    m_max = -math.inf
    for i, n1 in enumerate(numbers):
        for j, n2 in enumerate(numbers):
            if i == j:
                continue
            m = number_magnitude(add_numbers(n1, n2))
            if m > m_max:
                m_max = m
    print(m_max)


if __name__ == '__main__':
    part1(*sys.argv[1:])
    part2(*sys.argv[1:])
