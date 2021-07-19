# 本文档用于模拟真实应用场景的结构数据，以测试w、b参数的效果
# [ { A={A1={属性},A2={属性},A3={属性},...,Aj}, B={属性}}, rel=4 },   ]
# {"A": [{"id_A": "1",
#       "position": {"left_up": [160, 208], "right_down": [290, 248]}, "xpath": "/html/body/form/div[2]/div[1]/div/ul/li[1]/label", "context": {"data": "* 手机号码："}}, {"id_A": "2", "position": {"left_up": [160, 278], "right_down": [290, 318]}, "xpath": "/html/body/form/div[2]/div[1]/div/ul/li[2]/label", "context": {"data": "*手机验证码："}}, {"id_A": "3", "position": {"left_up": [160, 348], "right_down": [290, 388]}, "xpath": "/html/body/form/div[2]/div[1]/div/ul/li[4]/label", "context": {"data": "用户名："}}, {"id_A": "4", "position": {"left_up": [160, 418], "right_down": [290, 458]}, "xpath": "/html/body/form/div[2]/div[1]/div/ul/li[5]/label", "context": {"data": "密码："}}, {"id_A": "5", "position": {"left_up": [160, 488], "right_down": [290, 528]}, "xpath": "/html/body/form/div[2]/div[1]/div/ul/li[6]/label", "context": {"data": " "}}, {"id_A": "6", "position": {"left_up": [224, 87], "right_down": [335, 113]}, "xpath": "/html/body/form/div[1]/span", "context": {"data": "注册账号"}}, {"id_A": "7", "position": {"left_up": [481, 820], "right_down": [563, 835]}, "xpath": "/html/body/form/div[3]/div/div[1]/span", "context": {"data": "房天下家族‖"}}], "B": {"id_B": "1", "position": {"left_up": [0, 0], "right_down": [0, 0]}, "xpath": "/html/body/div[1]/div/input[1]", "context": {"data": ""}, "realId": "channelDsy"}, "Result": "0"}
# 步骤：
# 1. 解析数据：将输入数据解析为：[j*6] and [j]；
# [[mid_dist, nearest_dist, anceMatchRate, contMatchRate, row, col],
#  [mid_dist, nearest_dist, anceMatchRate, contMatchRate, row, col],
#  [mid_dist, nearest_dist, anceMatchRate, contMatchRate, row, col],
#  ...,
#  [mid_dist, nearest_dist, anceMatchRate, contMatchRate, row, col]]
# [ ifMatch, ifMatch, ifMatch, ifMatch, ifMatch, ifMatch, ifMatch]
# 2.将解析后的数据带入逻辑回归的公式，计算B与每个A的逻辑回归数值，选择值最大的那一个，并附上概率值；
# 3.
from loadDataJson import extractTestData
import tensorflow as tf
import numpy as np


def sigmoid(num):
    return 1/(1+tf.exp(-num))


def translate(data):
    # [{
    # 'id': '1',
    # 'mid_dist': 1.6016319802001957,
    # 'nearest_dist': 0.8,
    # 'anceMatchRate': 0.0,
    # 'contMatchRate': 0.0,
    # 'row': -1,
    # 'col': -1
    # },
    # ] (lenth = the num of A for one B)
    data_arr = np.zeros((len(data), 5))
    # 赋值
    for i in range(len(data)):
        data_arr[i][0] = data[i]["mid_dist"]
        data_arr[i][1] = data[i]["nearest_dist"]
        data_arr[i][2] = data[i]["anceMatchRate"]
        data_arr[i][3] = data[i]["contMatchRate"]
        data_arr[i][4] = data[i]["row"]
        #data_arr[i][5] = data[i]["colon"]
    return data_arr


def bingoRate(url, w, b, valve):
    # 输入参数：data,w,b
    # 输出参数：bingoNum,allNum
    para_set, label_set = extractTestData(url)
    bingoNum = 0
    for i in range(len(para_set)):
        len_As = len(para_set[i])
        # 将每个 B对应的 n个A数据转化为 np.arr格式 [[],[],...,[]]
        one_set_A = translate(para_set[i])
        max_sig = 0
        max_A_id = 0
        # 从每个B对应的一组A中，选择匹配度最高的A
        for j in range(len_As):
            val = w*(one_set_A[j].T)+b
            if max_sig < sigmoid(sum(val)):
                max_sig = sigmoid(sum(val))
                max_A_id = para_set[i][j]['id']
        if (float(max_sig) >= valve) and (max_A_id == label_set[i]):
            bingoNum += 1
            print(i+1, "- A guess:", max_A_id, " real:", label_set[i])
        elif (float(max_sig) < valve) and ((label_set[i] == "-1") or (label_set[i] == "0")):
            bingoNum += 1
            print(i+1, "- A guess:", -1, " real:", -1)
        else:
            print(i+1, "- A guess:", max_A_id,
                  " real:", label_set[i], "-----X")

    print("bingoNum:", bingoNum, " allNum:", len(para_set))
    print("w:", w)
    print("b:", b)

    return bingoNum, len(para_set)


# if __name__ == '__main__':
#     bingoNum, allNum = bingoRate(
#         'dataset/demo_data/nA1B_testData/NA1B-0706.txt',)
#     print("命中率：", float(bingoNum/allNum))
