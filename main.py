import verify as ver
import Levenshtein as Lev
import password as pw
import file


def main():
    f = open('pw.txt', 'r')
    line = f.readline().rstrip('\r\n')
    while line:
        rg_pw = "abcdef"  # 登録パスワード
        cor_ans = Lev.make_correct_ans(line, rg_pw)
        ans = ver.compare(pw.change_register_pw(rg_pw), pw.change_enter_pw(line, len(rg_pw)), len(rg_pw), len(line))
        print(ans)
        print("---------------")
        file.make_result(line, ans, cor_ans)
        line = f.readline().rstrip('\r\n')
        file.writefile("a", 12)

    f.close()

    # Detail.txtを作る処理


if __name__ == '__main__':
    main()
