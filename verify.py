import calculation as calc
import Levenshtein as Lev
import file
import password as pw
import ElementCalc as el

#  許容ミス桁
miss_digit = 2


# r_pw　登録パスワード　e_pw登録パスワード
def compare(r_pw, e_pw, len_pw, enter_len_pw):
    r_result = []  # 登録パスワード側の一致部分文字列
    e_result = []  # 入力パスワード側の一致部分文字列

    if enter_len_pw > len_pw + miss_digit or enter_len_pw < len_pw - miss_digit:
        return "入力パスワードの桁数が+-3以上です"

    for i in r_pw:
        for j in e_pw:
            if i[0] == j[0]:
                r_result.append(i)
                e_result.append(j)

    file.writefile(r_result, 5)
    file.writefile(e_result, 6)

    if r_pw == e_pw:
        return "一致しています"

    else:
        return search(r_result, e_result, len_pw, enter_len_pw)


def search(r_result, e_result, len_pw, enter_len_pw):
    str_result = []  # [('a', 'b', 'c'), ('a', 'b', 'd'), ('a', 'c', 'd'), ('b', 'c', 'd')]など一致文字列の配列
    r_num_list = []  # [(4, 5), (3, 5), (2, 5), (1, 5)]など登録一致文字列の含まれない桁数
    e_num_list = []  # [(4, 5), (3, 5), (2, 5), (1, 5)]など入力一致文字列の含まれない桁数
    Total_ans = []  # ['I', [5]]など最終の答えを返す
    flag = 0

    # 重複あり、なしに関わらず各ansを計算する
    tmp = el.element_calc(r_result, e_result, len_pw, enter_len_pw)

    print("r_result (r_pw) = %s" % r_result)
    print("e_result (e_pw) = %s" % e_result)
    print("len_pw = %d" % len_pw)
    print("enter_len_pw = %d" % enter_len_pw)

    file.make_match2(r_result, e_result)

    #  重複を数える
    for i in range(len(str_result)):
        if str_result.count(str_result[i]) > 1:
            flag += 1
    # 重複が無い時(入力ミスをした文字が登録パスワードに含まれていない場合？)
    if flag == 0:

        I_ans = tmp[0]
        D_ans = tmp[1]
        R_ans = tmp[2]

        # if D_ans == []:
        #     D_ans.append(0)
        # if R_ans == []:
        #     R_ans.append(0)
        print("I_ans is ", end='')
        print(I_ans)
        file.writefile(I_ans, 7)
        print("D_ans is ", end='')
        print(D_ans)
        file.writefile(D_ans, 8)
        print("R_ans is ", end='')
        print(R_ans)
        file.writefile(R_ans, 9)
        # 条件式が甘い
        #  I=1
        if len(I_ans) == 1 and D_ans == []:
            Total_ans.append("I")
            Total_ans.append(I_ans)
            file.writefile(Total_ans, 10)
            return Total_ans
        #  I=2
        elif len(I_ans) == 2 and D_ans == []:
            Total_ans.append("I")
            Total_ans.append(I_ans)
            file.writefile(Total_ans, 10)
            return Total_ans
        #  D=1
        elif len(D_ans) == 1 and I_ans == []:
            Total_ans.append("D")
            Total_ans.append(D_ans)
            file.writefile(Total_ans, 10)
            return Total_ans
        #  D=2
        elif len(D_ans) == 2 and I_ans == []:
            Total_ans.append("D")
            Total_ans.append(D_ans)
            file.writefile(Total_ans, 10)
            return Total_ans
        #  R=1かI=1,D=1
        elif len(I_ans) == 1 and len(D_ans) == 1:
            #  R=1
            if I_ans == D_ans:
                Total_ans.append("R")
                Total_ans.append(R_ans)
                file.writefile(Total_ans, 10)
                return Total_ans
            #  I=1,D=1
            else:
                a = ["I", I_ans[0]]
                Total_ans.append(a)
                b = ["D", D_ans[0]]
                Total_ans.append(b)
                file.writefile(Total_ans, 10)
                return Total_ans
        #  R=2(特殊パターンI=1,D=1、順番が違うやつ)
        elif I_ans == [] and D_ans == [] and len(R_ans) == 2:
            Total_ans.append(["R", R_ans[0]])
            Total_ans.append(["R", R_ans[1]])
            file.writefile(Total_ans, 10)
            return Total_ans
        #  I=2,D=1（許容しないけど）かR=1,I=1
        elif len(I_ans) == 2 and len(D_ans) == 1:
            #  R=1,I=1
            if D_ans[0] in I_ans:
                R_ans.append(D_ans[0])
                I_ans.remove(D_ans[0])
                Total_ans.append(["R", R_ans[0]])
                Total_ans.append(["I", I_ans[0]])
                file.writefile(Total_ans, 10)
                return Total_ans
            #  R=1,I=1([[('b', 'd', 'e', 'f'), (1, 3)]]と[[('b', 'd', 'e', 'f'), 2]]の時)
            elif I_ans[0] < D_ans[0] < I_ans[1] and I_ans[1] - 1 == D_ans[0]:
                R_ans.append(D_ans[0])  # 入力パスワードのミスの位置を基準に考える（Rを優先する）
                #  もし登録パスワードに対する入力ミスの位置を基準にするならR_ans.append(I_ans[1])
                I_ans.remove(I_ans[1])
                Total_ans.append(["R", R_ans[0]])
                Total_ans.append(["I", I_ans[0]])
                file.writefile(Total_ans, 10)
                return Total_ans
            else:
                Total_ans.append("I=2,D=1は許容しない")
                file.writefile(Total_ans, 11)
                return "I=2,D=1は許容しない"
        #  I=1,D=2(許容しないけど)かR=1,D=1
        elif len(I_ans) == 1 and len(D_ans) == 2:
            #  R=1,D=1
            if I_ans[0] in D_ans:
                R_ans.append(I_ans[0])
                D_ans.remove(I_ans[0])
                Total_ans.append(["R", R_ans[0]])
                Total_ans.append(["D", D_ans[0]])
                file.writefile(Total_ans, 10)
                return Total_ans
            #  R=1,D=1(隣接する時)
            elif D_ans[0] < I_ans[0] < D_ans[1] and D_ans[1] - 1 == I_ans[0]:
                R_ans.append(D_ans[1])
                D_ans.remove(D_ans[1])
                Total_ans.append(["R", R_ans[0]])
                Total_ans.append(["D", D_ans[0]])
                file.writefile(Total_ans, 10)
                return Total_ans
            else:
                Total_ans.append("I=1,D=2は許容しない")
                file.writefile(Total_ans, 11)
                return "I=1,D=2は許容しない"
        #  I=2,D=2(許容しないけど)かR=2
        elif len(I_ans) == 2 and len(D_ans) == 2:
            #  R=2
            if I_ans[0] in D_ans and I_ans[1] in D_ans:
                R_ans.append(I_ans[0])
                R_ans.append(I_ans[1])
                Total_ans.append(["R", R_ans[0]])
                Total_ans.append(["R", R_ans[1]])
                file.writefile(Total_ans, 10)
                return Total_ans
            else:
                Total_ans.append("I=2,D=2は許容しない")
                file.writefile(Total_ans, 11)
                return "I=2,D=2は許容しない"

        # どれも一致しない時
        else:
            Total_ans.append("どれにも一致しない")
            file.writefile(Total_ans, 11)
            return -1
    # 重複がある時(I=1,2は存在しない)
    elif flag != 0:
        #  重複している部分を両方削除して、残ったものをリストにする
        new_str_result = []
        new_r_num_list = []
        new_e_num_list = []
        temp = [0] * len(str_result)
        is_same = False
        for k in range(len(str_result)):
            for l in range(len(str_result)):
                if k != l:
                    if str_result[k] == str_result[l]:
                        if is_same:
                            is_same = False
                        else:
                            temp[l] = 1
                            is_same = True
        print("temp = ", end="")
        print(temp)
        for m in range(len(str_result)):
            if temp[m] == 0:
                new_str_result.append(str_result[m])
                new_r_num_list.append(r_num_list[m])
                new_e_num_list.append(e_num_list[m])

        print("Change str_result = ", end='')
        print(new_str_result)
        print("Change r_num_list = ", end='')
        print(new_r_num_list)
        print("Change e_num_list = ", end='')
        print(new_e_num_list)

        #  何桁目にミスがあるか ここの動きの調査！
        ans = calc.calc_i_d_r(r_num_list, len_pw, e_num_list, enter_len_pw)
        I_ans = ans[0]
        D_ans = ans[1]
        R_ans = ans[2]

        file.writefile(I_ans, 7)
        file.writefile(D_ans, 8)
        file.writefile(R_ans, 9)
        print(I_ans)
        print(D_ans)
        print(R_ans)
        #  D=1
        if len(D_ans) == 1 and I_ans == []:
            Total_ans.append("D")
            Total_ans.append(D_ans)
            file.writefile(Total_ans, 10)
            return Total_ans
        #  D=1（隣接しているとき）かR=1,D=1
        elif len(D_ans) == 2 and len(I_ans) == 1:
            #  D=1（隣接しているとき）
            if I_ans[0] in D_ans:
                D_ans.remove(I_ans[0])
                Total_ans.append("D")
                Total_ans.append(D_ans)
                file.writefile(Total_ans, 10)
                return Total_ans
            #  R=1,D=1
            elif D_ans[0] < I_ans[0] < D_ans[1] and D_ans[1] - 1 == I_ans[0]:
                R_ans.append(D_ans[1])
                D_ans.remove(D_ans[1])
                Total_ans.append(["R", R_ans[0]])
                Total_ans.append(["D", D_ans[0]])
                file.writefile(Total_ans, 10)
                return Total_ans
            else:
                Total_ans.append("D=1（隣接しているとき）かR=1,D=1のどちらでもない")
                file.writefile(Total_ans, 11)
                return "D=1（隣接しているとき）かR=1,D=1のどちらでもない"
        #  D=2
        elif len(D_ans) == 2 and I_ans == []:
            Total_ans.append("D")
            Total_ans.append(D_ans)
            file.writefile(Total_ans, 10)
            return Total_ans
        #  D=1（隣接しているとき）
        elif len(D_ans) == 3 and len(I_ans) == 1:
            D_ans.remove(I_ans[0])
            Total_ans.append("D")
            Total_ans.append(D_ans)
            file.writefile(Total_ans, 10)
            return Total_ans
        #  R=1
        elif len(I_ans) == 1 and len(D_ans) == 1:
            if I_ans == D_ans:
                Total_ans.append("R")
                Total_ans.append(R_ans)
                file.writefile(Total_ans, 10)
                return Total_ans
        #  R=1(特殊パターン：隣接しているとき)
        elif len(I_ans) == len(D_ans) == 2 and len(new_str_result) == 1:
            R_ans.remove(R_ans[0])
            Total_ans.append("R")
            Total_ans.append(R_ans)
            file.writefile(Total_ans, 10)
            return Total_ans

        else:
            Total_ans.append("例外")
            file.writefile(Total_ans, 11)
            return -1


if __name__ == '__main__':
    f2 = open('pw.txt', 'r')
    line = f2.readline().rstrip('\r\n')

    while line:
        rg_pw = "abcdef"  # 登録パスワード
        file.make_match(rg_pw, line)
        file.writefile(rg_pw, 1)
        file.writefile(line, 2)
        table = Lev.initialize_table(line, rg_pw)
        calculated_table = Lev.calculate_cost(table, line, rg_pw)
        results = Lev.judge_result(calculated_table, line, rg_pw)
        Lev.print_results(results)
        i = compare(pw.change_register_pw(rg_pw), pw.change_enter_pw(line, len(rg_pw)), len(rg_pw), len(line))
        print(i)
        line = f2.readline().rstrip('\r\n')
        file.writefile("a", 12)

    f2.close()
