from sys import argv, exit
from typing import Tuple, List
import csv
import copy

dict = {'m': 'match', 'i': 'insertion', 'd': 'deletion', 'r': 'replacement'}
I_cost = 1
D_cost = 1
R_cost = 1


# def validation_argv() -> None:
#     if len(argv) < 3:
#         exit('Less arguments...\n' + 'should $' + argv[0] + ' "text1" "text2"')
#     for index in range(1, 2):
#         if type(argv[index]) is not str:
#             exit('Argument must be string')


def initialize_table(word1: str, word2: str) -> List[List[Tuple[int, int, int]]]:
    # (スコア, 遷移前の座標x(row), 遷移前の座標y(column))
    table = [[(0, 0, 0)] * (len(word1) + 1) for i in range(len(word2) + 1)]

    for column in range(1, len(table[0])):
        table[0][column] = table[0][column - 1][0] + 1, 0, column - 1
    for row in range(1, len(table)):
        table[row][0] = table[row - 1][0][0] + 1, row - 1, 0
    return table


def calculate_cost(table: List[List[Tuple[int, int, int]]], word1: str, word2: str) -> List[List[Tuple[int, int, int]]]:
    for row in range(1, len(table)):
        for column in range(1, len(table[0])):
            if word1[column - 1] == word2[row - 1]:
                table[row][column] = table[row - 1][column - 1][0], row - 1, column - 1
            else:
                up_left = (table[row - 1][column - 1][0] + R_cost, row - 1, column - 1)
                left = (table[row][column - 1][0] + D_cost, row, column - 1)
                up = (table[row - 1][column][0] + I_cost, row - 1, column)
                table[row][column] = sorted([up_left, left, up], key=lambda x: x[0])[0]
    return table


def print_table(table: List[List[Tuple[int, int, int]]]) -> None:
    for row in table:
        print(row)


def judge_result(table: List[List[Tuple[int, int, int]]], word1: str, word2: str) -> List[Tuple[str, str]]:
    results = []
    follow = (len(word2), len(word1))
    while follow != (0, 0):
        point = table[follow[0]][follow[1]]
        route = (point[1], point[2])

        if follow[0] == route[0]:
            results.append(([word1[route[1]]], 'd'))
        elif follow[1] == route[1]:
            results.append(([word2[route[0]]], 'i'))
        elif table[route[0]][route[1]][0] == point[0]:
            results.append(([word1[route[1]]], 'm'))
        else:
            results.append(([word1[route[1]], word2[route[0]]], 'r'))
        follow = route
    results.reverse()
    return results


def print_results(results: List[Tuple[str, str]]) -> None:
    i = 1
    I_ans = ["I", []]
    D_ans = ["D", []]
    R_ans = ["R", []]
    ans = []
    tmp = []
    for result in results:
        if dict[result[1]] != "match":
            if dict[result[1]] == "replacement":
                R_ans[1].append(i)
            elif dict[result[1]] == "insertion":
                I_ans[1].append(i)
            elif dict[result[1]] == "deletion":
                D_ans[1].append(i)
        i += 1

    i = 0
    tmp.append(R_ans)
    tmp.append(D_ans)
    tmp.append(I_ans)
    for m in tmp:
        if m[1]:
            ans.append(m)
    print(results)
    print(ans[0])
    make_csv(ans)


def make_csv(ans):
    f = open('correct_ans.csv', 'a', newline="")
    writer = csv.writer(f)
    writer.writerow(ans)

    f.close()


if __name__ == '__main__':
    word1 = "abcdef"
    word2 = "aBCdef"
    table = initialize_table(word1, word2)
    calculated_table = calculate_cost(table, word1, word2)
    results = judge_result(calculated_table, word1, word2)
    print_results(results)
