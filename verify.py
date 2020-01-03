import itertools
import copy
import math

# 許容ミス桁
miss_digit = 2


def change_register_pw(password):
    PW = list(password)
    # 桁数を計算する 12桁想定なので12C2
    len_password = len(PW)
    digit = sorted(list(itertools.combinations(list(range(1, len_password + 1)), 2)), reverse=True)

    # 組み合わせを計算する
    comb_password = list(itertools.combinations(PW, len_password - miss_digit))

    # サーバ登録情報（部分文字列、含まれない文字の桁番号）
    register_info = []
    for i in range(len(digit)):
        temp = [comb_password[i], digit[i]]
        register_info.append(temp)

    return register_info


def change_enter_pw(password, len_reg_password):
    # 桁数を計算する 10-14を許容
    PW = list(password)
    len_password = len(PW)
    x = len_password - len_reg_password
    if x == 0:
        # 桁数が同じ
        digit = sorted(list(itertools.combinations(list(range(1, len_password + 1)), 2)),
                       reverse=True)
    elif x < 0:
        if x == -1:
            digit = sorted(list(range(1, len_password + 1)),
                           reverse=True)
            # digit = sorted(list(itertools.combinations(list(range(1, len_password + 1)), 1)),
            #                reverse=True)
            # print(list(range(1, len_password + 1)))
        elif x == -2:
            # digit = sorted(list(itertools.combinations(list(range(1, len_password + 1)), 0)),
            #                reverse=True)
            digit = [0, ]
        else:
            # エラー
            return -1
    else:
        if x == 1:
            digit = sorted(list(itertools.combinations(list(range(1, len_password + 1)), 3)),
                           reverse=True)
        elif x == 2:
            digit = sorted(list(itertools.combinations(list(range(1, len_password + 1)), 4)),
                           reverse=True)
        else:
            # エラー
            return -1

    # 組み合わせを計算する
    comb_password = list(itertools.combinations(PW, len_reg_password - miss_digit))

    # サーバ登録情報（部分文字列、含まれない文字の桁番号）
    enter_info = []
    for i in range(len(comb_password)):
        temp = [comb_password[i], digit[i]]
        enter_info.append(temp)

    return enter_info


def compare(r_pw, e_pw, len_pw, enter_len_pw):
    r_result = []  # 登録パスワード側の一致部分文字列
    e_result = []  # 入力パスワード側の一致部分文字列
    for i in r_pw:
        for j in e_pw:
            if i[0] == j[0]:
                r_result.append(i)
                e_result.append(j)

    print(r_result)
    print(e_result)
    return search(r_result, e_result, len_pw, enter_len_pw)
    # if combinations(len_pw - 1, len_pw - 2) == len(r_result) and


def search(r_pw, e_pw, len_pw, enter_len_pw):
    r_result = []
    r_num_list = []
    e_num_list = []
    I_ans = []
    D_ans = []
    R_ans = []
    Total_ans = []
    flag = 0
    for i in r_pw:
        r_result.append(i[0])

    for i in r_pw:
        r_num_list.append(i[1])

    for i in e_pw:
        e_num_list.append(i[1])

    print("r_result = ", end='')
    print(r_result)
    print("r_num_list = ", end='')
    print(r_num_list)
    print("e_num_list = ", end='')
    print(e_num_list)

    for i in range(len(r_result)):
        if r_result.count(r_result[i]) > 1:
            flag += 1

    # 重複が無い時
    if flag == 0:
        I_ans = cul_number(r_num_list, len_pw)
        D_ans = cul_number(e_num_list, enter_len_pw)
        R_ans = cul_replacement(I_ans, D_ans)
        print("I_ans is ", end='')
        print(I_ans)
        print("D_ans is ", end='')
        print(D_ans)
        print("R_ans is ", end='')
        print(R_ans)

        # R=1
        if I_ans == D_ans == R_ans and len(I_ans) == 1:
            Total_ans.append("R")
            Total_ans.append(R_ans)
            return Total_ans
        # R=2
        elif I_ans == D_ans == R_ans and len(I_ans) == 2:
            Total_ans.append(["R", "R"])
            Total_ans.append(R_ans)
            return Total_ans
        # I=1,D=1

        # I=1
        elif len(I_ans) == 1 and I_ans != []:
            Total_ans.append("I")
            Total_ans.append(I_ans)
            return Total_ans
        # I=1,R=1
        elif len(I_ans) == 2 and len(R_ans) == 1:
            a = []
            a.append("R")
            a.append(R_ans)
            Total_ans.append(a)
            a = []
            I_ans.remove(R_ans[0])
            a.append("I")
            a.append(I_ans)
            Total_ans.append(a)
            return Total_ans
        # I=2
        elif len(I_ans) == 2 and D_ans[0] == 0 and len(R_ans) == 0:
            Total_ans.append("I")
            Total_ans.append(I_ans)
            return Total_ans
        # D=1
        elif len(I_ans) == 0 and len(D_ans) == 1 and len(R_ans) == 0:
            Total_ans.append("D")
            Total_ans.append(D_ans)
            return Total_ans
        elif len(I_ans) == 0 and len(D_ans) == 2 and len(R_ans) == 0:
            Total_ans.append("D")
            Total_ans.append(D_ans)
            return Total_ans
    # 重複がある時
    elif flag != 0:
        print("flag=", end="")
        print(flag)
        print(r_num_list.count(r_num_list[0]))
        return -1

def cul_replacement(r_ans, e_ans):
    result = []
    if len(r_ans) == len(e_ans):
        for i in range(len(r_ans)):
            for j in range(len(e_ans)):
                if r_ans[i] == e_ans[j]:
                    result.append(r_ans[i])
    elif len(r_ans) > len(e_ans):
        for i in range(len(r_ans)):
            for j in range(len(e_ans)):
                if r_ans[i] == e_ans[j]:
                    result.append(r_ans[i])
    else:
        for i in range(len(e_ans)):
            for j in range(len(r_ans)):
                if e_ans[i] == r_ans[j]:
                    result.append(e_ans[i])
    return result


def cul_number(list, length):
    count = 0
    ans = []
    for i in range(1, length+1):
        count = 0
        for j in list:
            if type(j) is int:
                j = j,
            if i in j:
                count += 1
            if count == len(list):
                ans.append(i)
                count = 0
    return ans


def x(p):
    path = 'result.txt'
    f = open(path, mode='w')
    path2 = 'result2.txt'
    f2 = open(path2, mode='w')
    # 正解PW
    value = ['a', 'b', 'c', 'd', 'e']
    v_len = len(value)
    v_list = list(itertools.combinations(value, v_len - 2))
    number = [1, 2, 3, 4, 5]
    n_list = sorted(list(itertools.combinations(number, v_len - 3)), reverse=True)
    current = [value, number]
    print(current)
    print(current[1][1])

    # 入力PW
    p_len = len(p)
    p_list = list(itertools.combinations(p, p_len - 3))
    p_number = list(range(1, p_len + 1))
    pn_list = sorted(list(itertools.combinations(p_number, p_len - 3)), reverse=True)
    print(p_list)

    # 入力に対して正解を比較していく,p_list=入力,v_list=正解
    match_server_pw = []
    match_enter_pw = []
    match_server_num = []
    match_enter_num = []

    for i in range(len(p_list)):
        for j in range(len(v_list)):
            if p_list[i] == v_list[j]:
                match_enter_pw.append(copy.copy(p_list[i]))
                match_enter_num.append(copy.copy(pn_list[i]))
                f.write(str(v_list[j]))
                f.write(str(n_list[j]))
                f.write('=')
                f.write(str(p_list[i]))
                f.write(str(pn_list[i]))
                f.write('\n')
                if v_list[j] not in match_server_pw:
                    match_server_pw.append(copy.copy(v_list[j]))
                    match_server_num.append(copy.copy(n_list[j]))
                else:
                    f2.write(str(v_list[j]))
                    f2.write(str(n_list[j]))
                    f2.write('=')
                    f2.write(str(p_list[i]))
                    f2.write(str(pn_list[i]))
                    f2.write('\n')

    print("正解PWの個数=%d, 入力PWの個数=%d" % (len(match_server_pw), len(match_enter_pw)))
    print("正解PW=", end="")
    print(match_server_pw)
    print("正解PWの桁=", end="")
    print(match_server_num)
    print("入力PW=", end="")
    print(match_enter_pw)
    print("入力PWの桁=", end="")
    print(match_enter_num)
    f.close()
    f2.close()


def combinations(n, r):
    return math.factorial(n) // (math.factorial(n - r) * math.factorial(r))


if __name__ == '__main__':
    i = compare(change_register_pw("abcde"), change_enter_pw("abcdee", 5), 5, 5)
    print(i)
    # x(['a', 'b', 'c', 'd', 'e', 'a'])
    # change_register_pw(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'])
    # change_enter_pw(['a', 'B', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l'], 12)
    # a =[]
    # k = []
    # for i in range(4):
    #     k = i,
    #     a.append(k)
    #     print(type(k))
    # print(a)
