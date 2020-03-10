from itertools import combinations
from collections import Counter
from functools import reduce
from operator import add


def cmb(n, r):
    r = min(n - r, r)
    if r == 0:
        return 1
    mul_combi = zip(range(n, n - r, -1), range(1, r + 1))
    return reduce(lambda accum, combi : (accum * combi[0]) // combi[1],  mul_combi, 1)


def count_uniq_combination_simple(in_arr, num):
    arr = sorted(in_arr)
    combi = set()
    for c in combinations(arr, num):
        combi.add(c)

    return len(combi)


def count_uniq_combination_lattice(arr, num):
    if len(arr) < num:
        return 0

    # どの数字が何回現れているか
    # Counter([1, 2, 3, 4, 5, 3, 5, 5]) => {1: 1, 2: 1, 3: 2, 4: 1, 5: 3}
    number_counter = Counter(arr)
    # numよりも大きいものは、numにする
    number_counter = {n: min(c, num) for n, c in number_counter.items()}
    arr_len = reduce(add, number_counter.values())
    # 出現回数はそれぞれ何回現れているか
    # Counter({1: 1, 2: 1, 3: 2, 4: 1, 5: 3}.values())
    # => Counter([1, 1, 2, 1, 3]) => {1: 3, 2: 1, 3: 1}
    count_counter = Counter(number_counter.values())
    # print(count_counter)

    # 格子の作成
    # 格子のx方向の長さ
    lattice_x_len = arr_len - num + 1
    # 組み合わせ数を格納する配列(lattice_x_len, (num + 1) の格子)
    lattice = [[0] * (num + 1) for i in range(lattice_x_len)]
    # 原点
    lattice[0][0] = 1

    # 原点からの距離
    step = count_counter[1]
    # print(f'step:{step}')

    # duplication = 1
    for x in range(max(step - num, 0), min(step + 1, lattice_x_len)):
        y = count_counter[1] - x
        lattice[x][y] = cmb(x + y, x)

    del count_counter[1]
    # print(lattice)

    for duplication, count in count_counter.items():
        for i in range(count):
            step += duplication
            # print(f'step:{step}')
            for x in range(max(step - num, 0), min(step + 1, lattice_x_len)):
                y = step - x
                # print(f'x:{x}, y:{y}')

                for sub_x in range(min(x + 1, duplication + 1)):
                    sub_y = duplication - sub_x
                    lattice[x][y] += lattice[x - sub_x][y - sub_y]

    # print(lattice)
    return lattice[lattice_x_len - 1][num]
