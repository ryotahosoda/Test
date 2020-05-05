import file


# typeは"I""D""R" ansは[3][3,4]とか
def append_ans_single(ans_type, ans_num):
    Total_ans = [[ans_type, ans_num], []]
    file.writefile(Total_ans, 10)
    return Total_ans


def append_ans_double(ans_type1, ans_num1, ans_type2, ans_num2):
    Total_ans = [[ans_type1, ans_num1], [ans_type2, ans_num2]]
    file.writefile(Total_ans, 10)
    return Total_ans


def append_ans_error(err):
    Total_ans = [err]
    file.writefile(Total_ans, 11)
    return Total_ans