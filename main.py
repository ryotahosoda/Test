import verify as ver
import Levenshtein as Lev
import password as pw
import file
import csv


def main():
    f = open('pw.txt', 'r')
    line = f.readline().rstrip('\r\n')
    while line:
        rg_pw = "abcdef"  # 登録パスワード
        cor_ans = Lev.make_correct_ans(line, rg_pw)
        ans = ver.compare(pw.change_register_pw(rg_pw), pw.change_enter_pw(line, len(rg_pw)), len(rg_pw), len(line))
        print(ans)
        print("---------------")
        if len(ans) == 1:
            file.make_error(ans)
        else:
            file.make_result(line, ans, cor_ans)
        line = f.readline().rstrip('\r\n')
        # file.writefile("a", 12)

    ff = open('Result.csv', 'r')
    line2 = list(csv.reader(ff))
    count_match = [0, 0, 0]
    for m in line2:
        if len(m) != 1:
            if m[5] == "〇":
                count_match[0] += 1
            elif m[5] == "△":
                count_match[1] += 1
            elif m[5] == "×":
                file.make_not_match_txt(pw.change_register_pw(rg_pw), pw.change_enter_pw(m[0], len(rg_pw)),
                                        file.make_type(m[3], m[4]), m[0])
                file.make_not_pw(m[0])
                count_match[2] += 1
    file.make_detail(count_match)
    f.close()
    ff.close()


if __name__ == '__main__':
    main()
