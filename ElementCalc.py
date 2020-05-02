import copy
import calculation as calc
import itertools
import numpy as np


# 4/30 重複する組み合わせの中から正しい組み合わせを検索して、最適なI,D,R_ansを返す関数を作成
def element_calc(r_result, e_result, r_pw_len, e_pw_len):
    list_pos = list_position(r_result)  # 配列ペアの位置
    list_pair = []  # 重複する組み合わせのペア
    all_list_pair = []  # 全ての重複する組み合わせのペア
    all_no_pair = []  # 全ての重複していない残りの配列
    all_ans = []  # 全てのペアのミスの種類
    all_ans_size = []  # 全てのペアのミスの最小値
    dup_list_num = max(list_pos)  # 重複している部分の個数

    # 重複しない時
    dp = 0  # 重複するかどうかの判別用
    for k in list_pos:
        dp += k
    if dp == 0:
        str_result = []  # [('a', 'b', 'c'), ('a', 'b', 'd'), ('a', 'c', 'd'), ('b', 'c', 'd')]など一致文字列の配列
        r_num_list = []  # [(4, 5), (3, 5), (2, 5), (1, 5)]など登録一致文字列の含まれない桁数
        e_num_list = []  # [(4, 5), (3, 5), (2, 5), (1, 5)]など入力一致文字列の含まれない桁数
        for i in r_result:
            str_result.append(i[0])

        for i in r_result:
            r_num_list.append(i[1])

        for i in e_result:
            e_num_list.append(i[1])

        ans = calc.calc_i_d_r(r_num_list, r_pw_len, e_num_list, e_pw_len)
        I_ans = ans[0]
        D_ans = ans[1]
        R_ans = ans[2]
        print("str_result = %s" % str_result)
        print("r_num_list = %s" % r_num_list)
        print("e_num_list = %s" % e_num_list)
        return [I_ans, D_ans, R_ans]

    # 重複するペアをまとめる処理
    for h in range(dup_list_num):
        h += 1
        x = [i for i, x in enumerate(list_pos) if x == h]
        for k in range(len(x)):
            list_pair.append(make_pair(r_result[x[k]], e_result[x[k]]))
        q_copy = copy.copy(list_pair)
        all_list_pair.append(q_copy)
        list_pair.clear()

    # 重複していない部分の配列を作成する処理
    count = 0
    for k in list_pos:
        if k == 0:
            all_no_pair.append(make_pair(r_result[count], e_result[count]))
        count += 1

    #  重複しているペアが２か３か判断する配列を作成する
    pair_num_list = []  # 各重複ペアの個数と種類を格納する配列
    tmp = []
    for k in range(len(all_list_pair)):
        for m in range(len(all_list_pair[k])):
            tmp.append(m)
        cp = copy.copy(tmp)
        pair_num_list.append(cp)
        tmp.clear()

    # !!!!!!以下全ての組み合わせを計算して、ansを保存する処理!!!!!!
    # 全ての組み合わせを作成する
    all_pattern_list_pair = []  # 全ての組み合わせを格納する配列
    product = list(itertools.product(*pair_num_list))  # 直積を格納する 可変長変数を*で展開
    for m in range(len(product)):
        all_pattern_list_pair.append(search_pair(product[m], all_list_pair))

    for m in all_pattern_list_pair:
        result = make_miss(m, all_no_pair, r_pw_len, e_pw_len)
        #  ミスの種類をまとめ用配列に格納
        all_ans.append(result[0])
        #  計算結果をまとめ用配列に格納
        all_ans_size.append(result[1])

    # IとDの各々のサイズが混在してた場合は大きいほうを使うようにする処理（[1]と[1,4]とか）
    I_dig = [0, 0]  # [桁数1,桁数2]
    D_dig = [0, 0]
    for m in all_ans:
        tmp_i = calc.calc_i_d_size(m[0])
        I_dig[0] += tmp_i[0]
        I_dig[1] += tmp_i[1]
        tmp_d = calc.calc_i_d_size(m[1])
        D_dig[0] += tmp_d[0]
        D_dig[1] += tmp_d[1]

    # 片方1以上、片方0はそのまま、両方1以上は２の方だけ使う
    if I_dig[0] >= 1 and I_dig[1] >= 1:
        delete_pair_list(all_ans, all_ans_size, 0)
    elif D_dig[0] >= 1 and D_dig[1]:
        delete_pair_list(all_ans, all_ans_size, 1)

    #  最小値を選択して、インデックスを検索　ここを変更する
    box = []
    data = np.nonzero(all_ans_size)
    for k in data[0]:
        box.append(all_ans_size[k])
    index = all_ans_size.index(min(box))

    #  インデックスを使って各ミスを代入する。
    I_ans = all_ans[index][0]
    D_ans = all_ans[index][1]
    R_ans = all_ans[index][2]

    print(min(all_ans_size))
    print(all_ans)
    print(all_ans_size)
    print(index)
    print(I_ans)
    print(D_ans)
    print(R_ans)

    return [I_ans, D_ans, R_ans]


#  5/1 ペアを作る関数
def make_pair(r_result, e_result):
    tmp = [r_result, e_result]

    return tmp


#  5/2 特定の組み合わせを引っ張ってくる関数
def search_pair(num_list, all_list_pair):
    tmp = []
    for m in range(len(all_list_pair)):
        tmp.append(all_list_pair[m][num_list[m]])

    return tmp


#  5/2　ミスの種類を判別させる
def make_miss(all_list_pair, all_no_pair, r_pw_len, e_pw_len):
    # 重複ありとなしを連結する
    all_list = all_list_pair
    all_list.extend(all_no_pair)

    exm_str = []  # ある1つの組み合わせを入れる配列(文字列)
    exm_reg_num = []  # ある1つの組み合わせを入れる配列(登録パスワード)
    exm_ent_num = []  # ある1つの組み合わせを入れる配列(入力パスワード)
    for m in all_list:
        exm_str.append(m[0][0])
        exm_reg_num.append(m[0][1])
        exm_ent_num.append(m[1][1])
    #  ミスの種類を計算
    ans = calc.calc_i_d_r(exm_reg_num, r_pw_len, exm_ent_num, e_pw_len)
    #  ある1つの組み合わせの桁の値を計算
    ans_size = calc.calc_min(ans)  # 桁の最小値を格納する配列
    return [ans, ans_size]


# 4/30 一致文字列の内重複する部分の位置と個数を記録する配列list_posを返す関数を作成
def list_position(r_result):
    tmp = [0] * len(r_result)  # 位置記録用配列
    count = 0  # ペアの数
    box = []  # 比較用
    for k in range(len(r_result)):
        for l in range(len(r_result)):
            if k != l:
                if r_result[k] == r_result[l]:
                    if r_result[k] in box:
                        tmp[l] = count
                    else:
                        count += 1
                        tmp[l] = count
                        box.clear()
                        box.append(r_result[k])
    return tmp


# 5/2 サイズが1のペアを削除する
def delete_pair_list(all_ans, all_ans_size, ans_type):
    # ans_type==0はI,1はD
    for m in range(len(all_ans)):
        if len(all_ans[m][ans_type]) == 1:
            all_ans_size[m] = 0


if __name__ == '__main__':
    r_pw = [[('a', 'b', 'c', 'd'), (5, 6)], [('a', 'b', 'c', 'd'), (5, 6)], [('a', 'b', 'c', 'f'), (4, 5)],
            [('a', 'b', 'c', 'f'), (4, 5)], [('a', 'b', 'd', 'f'), (3, 5)], [('a', 'b', 'd', 'f'), (3, 5)],
            [('a', 'c', 'd', 'f'), (2, 5)], [('a', 'c', 'd', 'f'), (2, 5)], [('b', 'c', 'd', 'f'), (1, 5)]]

    e_pw = [[('a', 'b', 'c', 'd'), (2, 6, 7)], [('a', 'b', 'c', 'd'), (1, 6, 7)], [('a', 'b', 'c', 'f'), (2, 5, 6)],
            [('a', 'b', 'c', 'f'), (1, 5, 6)], [('a', 'b', 'd', 'f'), (2, 4, 6)], [('a', 'b', 'd', 'f'), (1, 4, 6)],
            [('a', 'c', 'd', 'f'), (2, 3, 6)], [('a', 'c', 'd', 'f'), (1, 3, 6)], [('b', 'c', 'd', 'f'), (1, 2, 6)]]

    r_pw_len = 6
    e_pw_len = 7
    element_calc(r_pw, e_pw, r_pw_len, e_pw_len)

    all_list_pair = [[[('a', 'b', 'c', 'd'), (5, 6)], [('a', 'b', 'c', 'd'), (2, 6, 7)]],
                     [[('a', 'b', 'c', 'f'), (4, 5)], [('a', 'b', 'c', 'f'), (2, 5, 6)]],
                     [[('a', 'b', 'd', 'f'), (3, 5)], [('a', 'b', 'd', 'f'), (2, 4, 6)]],
                     [[('a', 'c', 'd', 'f'), (2, 5)], [('a', 'c', 'd', 'f'), (2, 3, 6)]]]
    all_no_pair = [[[('b', 'c', 'd', 'f'), (1, 5)], [('b', 'c', 'd', 'f'), (1, 2, 6)]]]
    make_miss(all_list_pair, all_no_pair, r_pw_len, e_pw_len)
    print(list_position([[('a', 'b', 'c', 'd'), (5, 6)], [('a', 'b', 'c', 'f'), (4, 5)], [('a', 'b', 'd', 'f'), (3, 5)],
                         [('a', 'c', 'd', 'f'), (2, 5)], [('b', 'c', 'd', 'f'), (1, 5)]]))
