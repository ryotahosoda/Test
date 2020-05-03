def pattern_ans_size(all_ans_size, check_ans):
    II_DD_RR = 0
    II_DD_R = 0
    II_D_R = 0
    I_DD_R = 0
    I_D_R = 0

    II_DD_Z = 0

    II_D_Z = 0
    I_DD_Z = 0

    II_Z_Z = 0
    Z_DD_Z = 0

    I_D_Z = 0

    Z_D_Z = 0
    I_Z_Z = 0

    Z_Z_Z = 0
    for m in check_ans:
        if m == [2, 2, 2]:
            II_DD_RR += 1
        elif m == [2, 2, 1]:
            II_DD_R += 1
        elif m == [2, 1, 1]:
            II_D_R += 1
        elif m == [1, 2, 1]:
            I_DD_R += 1
        elif m == [1, 1, 1]:
            I_D_R += 1
        elif m == [2, 2, 0]:
            II_DD_Z += 1
        elif m == [2, 1, 0]:
            II_D_Z += 1
        elif m == [1, 2, 0]:
            I_DD_Z += 1
        elif m == [2, 0, 0]:
            II_Z_Z += 1
        elif m == [0, 2, 0]:
            Z_DD_Z += 1
        elif m == [1, 1, 0]:
            I_D_Z += 1
        elif m == [0, 1, 0]:
            Z_D_Z += 1
        elif m == [1, 0, 0]:
            I_Z_Z += 1
        elif m == [0, 0, 0]:
            Z_Z_Z += 1
        else:
            return "error"

    if II_DD_RR >= 1 or II_DD_R >= 1 or II_D_R >= 1 or I_DD_R >= 1 or I_D_R >= 1:
        delete_1(all_ans_size, check_ans)
        return all_ans_size
    elif II_DD_Z >= 1:
        delete_2(all_ans_size, check_ans)
        return all_ans_size
    elif II_D_Z >= 1 or I_DD_Z >= 1:
        delete_3(all_ans_size, check_ans)
        return all_ans_size
    elif II_Z_Z >= 1:
        delete_4_1(all_ans_size, check_ans)
        return all_ans_size
    elif Z_DD_Z >= 1:
        delete_4_2(all_ans_size, check_ans)
        return all_ans_size
    elif I_D_Z >= 1:
        delete_5(all_ans_size, check_ans)
        return all_ans_size
    else:
        return all_ans_size


# 5/2 Rが存在する場合、Rが存在しないペアは削除する
def delete_1(all_ans_size, check_ans):
    for m in range(len(check_ans)):
        if check_ans[m][2] < 1:
            all_ans_size[m] = 0


# 5/2 サイズが1のペアを削除する 5/3 I=2D=2の時それ以下を全部0に
def delete_2(all_ans_size, check_ans):
    for m in range(len(check_ans)):
        if check_ans[m][0] != 2 and check_ans[m][1] != 2:
            all_ans_size[m] = 0


# 5/3 I=1D=2かI=2D=1の時それ以下を全部0に
def delete_3(all_ans_size, check_ans):
    for m in range(len(check_ans)):
        if check_ans[m][0] <= 1 and check_ans[m][1] <= 1:
            all_ans_size[m] = 0


# 5/3 I=2の時それ以下を全部0に
def delete_4_1(all_ans_size, check_ans):
    for m in range(len(check_ans)):
        if check_ans[m][0] <= 1:
            all_ans_size[m] = 0


# 5/3 D=2の時それ以下を全部0に
def delete_4_2(all_ans_size, check_ans):
    for m in range(len(check_ans)):
        if check_ans[m][1] <= 1:
            all_ans_size[m] = 0


# 5/3 I=1D=1の時それ以下を全部0に
def delete_5(all_ans_size, check_ans):
    for m in range(len(check_ans)):
        if (check_ans[m][0] == 1 and check_ans[m][1] == 0) or (check_ans[m][0] == 0 and check_ans[m][0] == 1):
            all_ans_size[m] = 0
