import verify as ver
import Levenshtein as Lev
import password as pw
import file


def main():
    f = open('pw.txt', 'r')
    line = f.readline().rstrip('\r\n')
    while line:
        rg_pw = "abcdef"  # 登録パスワード
        table = Lev.initialize_table(line, rg_pw)
        calculated_table = Lev.calculate_cost(table, line, rg_pw)
        results = Lev.judge_result(calculated_table, line, rg_pw)
        Lev.print_results(results)
        i = ver.compare(pw.change_register_pw(rg_pw), pw.change_enter_pw(line, len(rg_pw)), len(rg_pw), len(line))
        print(i)
        print("---------------")
        line = f.readline().rstrip('\r\n')
        file.writefile("a", 12)

    f.close()

    # Detail.txtを作る処理


if __name__ == '__main__':
    main()
