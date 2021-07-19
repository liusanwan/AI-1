import math


def handlePosition(A_pos, B_pos):
    # A.position: {
    #     left_up : (x_l, y_l),
    #     right_down : (x_r, y_r)
    # }
    A_left_up_x, A_left_up_y = A_pos["left_up"]
    A_right_down_x, A_right_down_y = A_pos["right_down"]
    B_left_up_x, B_left_up_y = B_pos["left_up"]
    B_right_down_x, B_right_down_y = B_pos["right_down"]

    row = 0
    col = 0
# midPoin_dist	中心点距离
    A_midPoin = ((A_left_up_x+A_right_down_x)/2,
                 (A_left_up_y+A_right_down_y)/2)
    B_midPoin = ((B_left_up_x+B_right_down_x)/2,
                 (B_left_up_y+B_right_down_y)/2)
    mid_dist = math.sqrt(
        pow((A_midPoin[0]-B_midPoin[0]), 2) + pow((A_midPoin[1]-B_midPoin[1]), 2))
# nearest_dist	最近距离
    if (A_midPoin[0] < B_midPoin[0]):
        # 如果A在B左边，比较A_r_x和B_l_x
        x_dist = B_left_up_x-A_right_down_x
        row = 1
    else:
        # 如果A在B右边，比较A_l_x和B_r_x
        x_dist = A_left_up_x-B_right_down_x
        row = -1
    if (A_midPoin[1] > B_midPoin[1]):
        # 如果A在B下边，比较A_u_y和B_d_y
        y_dist = A_left_up_y-B_right_down_y
        col = -1
    else:
        # 如果A在B上边，比较A_d_y和B_u_y
        y_dist = B_left_up_y-A_right_down_y
        col = 1

    if (x_dist <= 0 and y_dist <= 0):
        nearest_dist = 0
    elif(x_dist <= 0 and y_dist > 0):
        nearest_dist = y_dist
    elif(x_dist > 0 and y_dist <= 0):
        nearest_dist = x_dist
    else:
        nearest_dist = min(x_dist, y_dist)

    # 返回元组：（第一项：中心点距离，第二项：最近距离）
    # return mid_dist*0.005, nearest_dist*0.005, row, col
    # return mid_dist*0.005, nearest_dist*0.005, row,A_midPoin[0],A_midPoin[1],B_midPoin[0],B_midPoin[1]
    return mid_dist*0.005, nearest_dist*0.005, row
