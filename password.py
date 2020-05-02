import itertools
import file

#  許容ミス桁
miss_digit = 2


# 登録パスワードから部分文字列を生成する
def change_register_pw(password):
    PW = list(password)  # ['a', 'b', 'c', 'd', 'e']のようにリストに入れる
    len_password = len(PW)
    digit = sorted(list(itertools.combinations(list(range(1, len_password + 1)), 2)), reverse=True)  # 部分文字列の含まれない文字の桁数
    comb_password = list(itertools.combinations(PW, len_password - miss_digit))  # 部分文字列を作成

    # サーバ登録情報（部分文字列、含まれない文字の桁番号）
    register_info = []  # [('a', 'b', 'c'), (4, 5)]のようなリストを作成
    for i in range(len(digit)):
        temp = [comb_password[i], digit[i]]
        register_info.append(temp)

    file.writefile(register_info, 3)
    return register_info


def change_enter_pw(password, len_reg_password):
    PW = list(password)  # ['a', 'b', 'c', 'd', 'e']のようにリストに入れる
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
        elif x == -2:
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

    file.writefile(enter_info, 4)
    return enter_info
