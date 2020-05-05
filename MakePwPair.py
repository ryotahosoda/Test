import numpy as np
import itertools


def makePwPair():
    m1 = ['a', 'b', 'c', 'd', 'e', 'f']
    m2 = ['a', 'b', 'c', 'd', 'e', 'f']
    m3 = ['a', 'b', 'c', 'd', 'e', 'f']
    m4 = ['a', 'b', 'c', 'd', 'e', 'f']

    lst = list(itertools.product(m1, m2, m3, m4))

    print(lst)

    f = open('pw.txt', 'w')
    for a in lst:
        tmp = ''.join(a)
        f.write(str(tmp))
        f.write("\n")
    f.close()


if __name__ == '__main__':
    makePwPair()
