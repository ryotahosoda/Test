import Levenshtein as Lev
import file
import password as pw
import ElementCalc as el
import ApAns as ap

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
    # 重複あり、なしに関わらず各ansを計算する
    tmp = el.element_calc(r_result, e_result, len_pw, enter_len_pw)

    # print("r_result (r_pw) = %s" % r_result)
    # print("e_result (e_pw) = %s" % e_result)
    # print("len_pw = %d" % len_pw)
    # print("enter_len_pw = %d" % enter_len_pw)

    file.make_match2(r_result, e_result)

    I_ans = tmp[0]
    D_ans = tmp[1]
    R_ans = tmp[2]

    # print("I_ans is %s" % I_ans)
    # file.writefile(I_ans, 7)
    # print("D_ans is %s" % D_ans)
    # file.writefile(D_ans, 8)
    # print("R_ans is %s" % R_ans)
    # file.writefile(R_ans, 9)

    # 重複が無い時(入力ミスをした文字が登録パスワードに含まれていない場合？)
    #  I=1 or I=2
    if len(I_ans) == 1 and D_ans == [] or len(I_ans) == 2 and D_ans == []:
        return ap.append_ans_single("I", I_ans)
    #  D=1
    elif len(D_ans) == 1 and I_ans == [] or len(D_ans) == 2 and I_ans == []:
        return ap.append_ans_single("D", D_ans)
    #  R=1かI=1,D=1
    elif len(I_ans) == 1 and len(D_ans) == 1:
        #  R=1
        if I_ans == D_ans:
            return ap.append_ans_single("R", R_ans)
        #  I=1,D=1
        else:
            return ap.append_ans_double("I", I_ans[0], "D", D_ans[0])
    #  R=2(特殊パターンI=1,D=1、順番が違うやつ)
    elif I_ans == [] and D_ans == [] and len(R_ans) == 2:
        return ap.append_ans_single("R", R_ans)
    #  I=2,D=1（許容しないけど）かR=1,I=1
    elif len(I_ans) == 2 and len(D_ans) == 1:
        #  R=1,I=1
        if D_ans[0] in I_ans:
            # Rを最優先　桁が小さいほうを優先　先に入力pw基準で考える
            I_ans.remove(D_ans[0])
            return ap.append_ans_double("R", R_ans, "I", I_ans)
        #  R=1,I=1([[('b', 'd', 'e', 'f'), (1, 3)]]と[[('b', 'd', 'e', 'f'), 2]]の時)
        elif I_ans[0] < D_ans[0] < I_ans[1] and I_ans[1] - 1 == D_ans[0]:
            # 入力パスワードのミスの位置を基準に考える（Rを優先する）
            R_ans.append(D_ans[0])
            #  もし登録パスワードに対する入力ミスの位置を基準にするならR_ans.append(I_ans[1])
            I_ans.remove(I_ans[1])
            return ap.append_ans_double("R", R_ans, "I", I_ans)
        else:
            return ap.append_ans_error("I=2,D=1は許容しない")
    #  I=1,D=2(許容しないけど)かR=1,D=1
    elif len(I_ans) == 1 and len(D_ans) == 2:
        #  R=1,D=1
        if I_ans[0] in D_ans:
            D_ans.remove(I_ans[0])
            return ap.append_ans_double("R", R_ans, "D", D_ans)
        #  R=1,D=1(隣接する時) !!ここ不安!!
        elif D_ans[0] < I_ans[0] < D_ans[1] and D_ans[1] - 1 == I_ans[0]:
            R_ans.append(D_ans[1])
            D_ans.remove(D_ans[1])
            return ap.append_ans_double("R", R_ans, "D", D_ans)
        else:
            return ap.append_ans_error("I=1,D=2は許容しない")
    #  I=2,D=2(許容しないけど)かR=2
    elif len(I_ans) == 2 and len(D_ans) == 2:
        #  R=2
        if I_ans[0] in D_ans and I_ans[1] in D_ans:
            return ap.append_ans_single("R", R_ans)
        else:
            return ap.append_ans_error("I=2,D=2は許容しない")
    # どれも一致しない時
    else:
        return ap.append_ans_error("どれにも一致しない")


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
        print("---------------")
        line = f2.readline().rstrip('\r\n')
        file.writefile("a", 12)

    f2.close()
