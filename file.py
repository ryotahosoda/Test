import csv


def writefile(x, num):
    path = 'result.txt'
    f = open(path, mode='a')
    if num == 1:
        f.write("登録パスワード：")
        f.write(str(x))
        f.write("\n")
    elif num == 2:
        f.write("入力パスワード：")
        f.write(str(x))
        f.write("\n")
    elif num == 3:
        f.write("登録パスワードの部分文字列：")
        f.write(str(x))
        f.write("\n")
    elif num == 4:
        f.write("入力パスワードの部分文字列：")
        f.write(str(x))
        f.write("\n")
    elif num == 5:
        f.write("一致した登録パスワードの部分文字列：")
        f.write(str(x))
        f.write("\n")
    elif num == 6:
        f.write("一致した入力パスワードの部分文字列：")
        f.write(str(x))
        f.write("\n")
    elif num == 7:
        f.write("I_ans = ")
        f.write(str(x))
        f.write("\n")
    elif num == 8:
        f.write("D_ans = ")
        f.write(str(x))
        f.write("\n")
    elif num == 9:
        f.write("R_ans = ")
        f.write(str(x))
        f.write("\n")
    elif num == 10:
        make_csv(x)
        f.write("ans = ")
        f.write(str(x))
        f.write("\n")
    elif num == 11:
        make_csv(x)
        f.write(str(x))
        f.write("\n")
    elif num == 12:
        f.write("\n")

    f.close()


def make_csv(x):
    f = open('ans.csv', 'a', newline="")
    writer = csv.writer(f)
    writer.writerow(x)
    f.close()


def make_match(en_pw, ans_type):
    fp = open('data/NotMatch_%s.txt' % ans_type, mode='a')
    fp.write("入力パスワード:")
    fp.write(str(en_pw))
    fp.write("\n")
    fp.close()


def make_match2(r_result, e_result, ans_type):
    fp = open('data/NotMatch_%s.txt' % ans_type, mode='a')
    for i in range(len(r_result)):
        fp.write(str(r_result[i]))
        fp.write("=")
        fp.write(str(e_result[i]))
        fp.write("\n")
    fp.write("--------------------------------------")
    fp.write("\n")
    fp.close()


def make_result(ent_pw, ans, cor_ans):
    f = open('Result.csv', 'a', newline="")
    writer = csv.writer(f)
    isMatch = "×"
    if ans == cor_ans:
        isMatch = "〇"
    else:  # あってるけど今回表記できないものを正解にする
        if ans[0][0] == cor_ans[0][0] and ans[1][0] == cor_ans[1][0]:
            if ans[0][1] == cor_ans[1][1] and ans[1][1] == cor_ans[0][1]:
                isMatch = "△"
        elif ans[1] != [] and cor_ans[1] == [] and len(cor_ans[0][1]) == 2:
            if ans[0][1] in cor_ans[0][1] and ans[1][1] in cor_ans[0][1]:
                isMatch = "△"
        elif ans[1] == [] and cor_ans[1] != [] and len(ans[0][1]) == 2:
            if cor_ans[0][1] in ans[0][1] and cor_ans[0][1] in ans[1][1]:
                isMatch = "△"
    tmp = [ent_pw, ans[0], ans[1], cor_ans[0], cor_ans[1], isMatch]
    if tmp[5] == "×":
        make_not_match_Z(tmp)
    writer.writerow(tmp)
    f.close()


def make_not_match_Z(tmp):
    p = [tmp[3][0]]
    if tmp[4]:
        p.append(tmp[4][0])
    print(p)
    if p == ['R']:
        f = open('data/NotMatch_R.csv', 'a', newline="")
    elif p == ['D']:
        f = open('data/NotMatch_D.csv', 'a', newline="")
    elif p == ['I']:
        f = open('NotMatch_I.csv', 'a', newline="")
    elif p == ['R', 'I']:
        f = open('data/NotMatch_RI.csv', 'a', newline="")
    elif p == ['R', 'D']:
        f = open('data/NotMatch_RD.csv', 'a', newline="")
    elif p == ['D', 'I']:
        f = open('data/NotMatch_DI.csv', 'a', newline="")
    writer = csv.writer(f)
    writer.writerow(tmp)


def make_not_match_txt(r_pw, e_pw, ans_type, enter_pw):
    r_result = []
    e_result = []

    for i in r_pw:
        for j in e_pw:
            if i[0] == j[0]:
                r_result.append(i)
                e_result.append(j)

    make_match(enter_pw, ans_type)
    make_match2(r_result, e_result, ans_type)


def make_type(cor_ans1, cor_ans2):
    p = [cor_ans1[2]]
    if cor_ans2 != '[]':
        p.append(cor_ans2[2])
    if p == ['R']:
        return 'R'
    elif p == ['D']:
        return 'D'
    elif p == ['I']:
        return 'I'
    elif p == ['R', 'I']:
        return 'RI'
    elif p == ['R', 'D']:
        return 'RD'
    elif p == ['D', 'I']:
        return 'DI'


def make_detail(count_match):
    f = open('data/Detail.txt', 'a')
    f.write("一致数(〇+△):")
    f.write(str(count_match[0] + count_match[1]))
    f.write("\n")
    f.write("表記違い(△):")
    f.write(str(count_match[1]))
    f.write("\n")
    f.write("不一致(×):")
    f.write(str(count_match[2]))
    f.write("\n")
    f.close()


def make_not_pw(enter_pw):
    f = open('data/NotMatchPw.txt', 'a')
    f.write(str(enter_pw))
    f.write("\n")
    f.close()


def make_error(ms):
    f = open('Result.csv', 'a', newline="")
    writer = csv.writer(f)
    writer.writerow(ms)
    f.close()
