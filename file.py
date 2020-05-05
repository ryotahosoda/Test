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


def make_match(rg_pw, en_pw):
    fp = open('match.txt', mode='a')
    fp.write("登録パスワード:")
    fp.write(str(rg_pw))
    fp.write("入力パスワード:")
    fp.write(str(en_pw))
    fp.write("\n")


def make_match2(r_result, e_result):
    #  match.txtを作成
    fp = open('match.txt', mode='a')
    for i in range(len(r_result)):
        fp.write(str(r_result[i]))
        fp.write("=")
        fp.write(str(e_result[i]))
        fp.write("\n")
    fp.write("--------------------------------------")
    fp.write("\n")
    fp.close()
    #  重複を数える


def make_result(ent_pw, ans, cor_ans):
    f = open('Result.csv', 'a', newline="")
    writer = csv.writer(f)
    isMatch = "×"
    if ans == cor_ans:
        isMatch = "〇"
    else:  # あってるけど今回表記できないものを正解にする
        if ans[0][0] == cor_ans[0][0] and ans[1][0] == cor_ans[1][0]:
            if ans[0][1] == cor_ans[1][1] and ans[1][1] == cor_ans[0][1]:
                isMatch = "〇"
        elif ans[1] != [] and cor_ans[1] == [] and len(cor_ans[0][1]) == 2:
            if ans[0][1] in cor_ans[0][1] and ans[1][1] in cor_ans[0][1]:
                isMatch = "〇"
        elif ans[1] == [] and cor_ans[1] != [] and len(ans[0][1]) == 2:
            if cor_ans[0][1] in ans[0][1] and cor_ans[0][1] in ans[1][1]:
                isMatch = "〇"
    tmp = [ent_pw, ans[0], ans[1], cor_ans[0], cor_ans[1], isMatch]
    writer.writerow(tmp)
    f.close()


if __name__ == '__main__':
    make_result("abcdef", [["I", [1]], ["D", [2]]], [["R", [1, 2]], []])
