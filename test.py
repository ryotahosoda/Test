

def solution(A, K):
    for x in range(K):
        A.insert(0, A.pop(-1))
    return A


if __name__ == '__main__':
    A = [1, 2, 3, 4, 5, 6]
    print(solution(A, 7))