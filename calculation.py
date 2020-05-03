import math


def calc_I_D(r_num_list, e_num_list):
    temp = []
    for i in range(len(r_num_list)):
        for j in range(len(e_num_list)):
            if i == j:
                if r_num_list[i] == e_num_list[j]:
                    temp = r_num_list[i]
    if temp:
        if sorted(r_num_list) == sorted(e_num_list):
            return temp
        else:
            return []
    else:
        return []


def calc_replacement(I_ans, D_ans):
    result = []
    if len(I_ans) == len(D_ans):
        for i in range(len(I_ans)):
            for j in range(len(D_ans)):
                if I_ans[i] == D_ans[j]:
                    result.append(I_ans[i])

    elif len(I_ans) > len(D_ans):
        for i in range(len(I_ans)):
            for j in range(len(D_ans)):
                if I_ans[i] == D_ans[j]:
                    result.append(I_ans[i])
    else:
        for i in range(len(D_ans)):
            for j in range(len(I_ans)):
                if D_ans[i] == I_ans[j]:
                    result.append(D_ans[i])
    return result


def calc_number(list, length):
    count = 0
    ans = []
    for i in range(1, length + 1):
        count = 0
        # 特定の数字が全てのリストの中に存在するかどうか　例：[(4, 5), (3, 5), (2, 5), (1, 5)]の5を探す
        for j in list:
            if type(j) is int:
                j = j,
            if i in j:
                count += 1
            if count == len(list):
                ans.append(i)
                count = 0
    return ans


#  5/1　i,d,rを特定する関数
def calc_i_d_r(r_num_list, r_pw_len, e_num_list, e_pw_len):
    i_ans = calc_number(r_num_list, r_pw_len)
    d_ans = calc_number(e_num_list, e_pw_len)
    r_ans = calc_replacement(i_ans, d_ans)
    # # I=1 D=1の時(特殊パターン:順番が違う)
    # if i_ans == [] and d_ans == []:
    #     tmp = calc_I_D(r_num_list, e_num_list)
    #     if tmp:
    #         r_ans.append(tmp[0])
    #         r_ans.append(tmp[1])
    ans = [i_ans, d_ans, r_ans]
    return ans


#  IまたはDの桁が１と2が混在している時を探す関数
def calc_i_d_r_size(ans):
    digit = [0, 0]
    if len(ans) == 1:
        digit[0] += 1
    elif len(ans) == 2:
        digit[1] += 1

    return digit


# サイズを見て桁を格納する関数
def calc_check(ans):
    result = []
    for m in ans:
        length = len(m)
        if length == 1:
            result.append(1)
        elif length == 2:
            result.append(2)
        else:
            result.append(0)
    return result


#  ある1つの組み合わせの桁の最小値を計算
def calc_min(ans):
    res = 0
    for miss in ans:
        if not miss:
            res += 0
        else:
            for num in miss:
                res += num

    return res


def combinations(n, r):
    return math.factorial(n) // (math.factorial(n - r) * math.factorial(r))


if __name__ == '__main__':
    ans = [[1], [3], []]
    print(calc_check(ans))
