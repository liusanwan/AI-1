# 本文档用于接收 孙佳 的前端数据，并用于预测判断值

import json
import tensorflow as tf
import numpy as np
from xpath import handleXpath
from context import handleContext
from position import handlePosition
from position_tf import handlePosition_tf
import tflearn
import argparse



# Same parameters as of 'ApeNet'
inputData = tflearn.input_data(shape=[None, 9])
layer_1 = tflearn.fully_connected(
    inputData, 32, activation='sigmoid', name='layer_1')
layer_2 = tflearn.fully_connected(
    layer_1, 108, activation='sigmoid', name='layer_2')
layer_3 = tflearn.fully_connected(
    layer_2, 64, activation='sigmoid', name='layer_3')
outputData = tflearn.fully_connected(
    layer_3, 2, activation='softmax', name='output')
net = tflearn.regression(outputData)

# Load the trained model
model = tflearn.DNN(net)
# model.load(model_url)



def sigmoid(num):
    return 1/(1+np.exp(-num))


def loadDataJson(url):
    # 加载文件夹
    data = []
    with open(url, encoding='utf_8_sig') as load_f:
        lines = load_f.readlines()
        for l in lines:
            data.append(json.loads(l))
    return data


def handleTestData(listA, listB):
    test = []
    for i in listB:
        temp = []
        for j in listA:
            # t = {
            #     "id": -1,
            #     "mid_dist": -1,
            #     "nearest_dist": -1,
            #     "anceMatchRate": -1,
            #     "contMatchRate": -1,
            #     "row": 0,
            # }
            t = []
            t1, t2, t5 = handlePosition(
                j["position"], i["position"])
            t3 = handleXpath(
                j["xpath"], i["xpath"])
            t4 = handleContext(
                j["context"], i["context"])
            t.append(t1)
            t.append(t2)
            t.append(t3)
            t.append(t4)
            t.append(t5)
            temp.append(t)
        test.append(temp)
    print("A 和 B 一一对应已完成！")
    return np.array(test)


def handleTestData_tf(listA, listB):
    test = []
    for i in listB:
        temp = []
        for j in listA:
            # t = {
            #     "id": -1,
            #     "mid_dist": -1,
            #     "nearest_dist": -1,
            #     "anceMatchRate": -1,
            #     "contMatchRate": -1,
            #     "row": 0,
            # }
            t = []
            t1, t2, t5, t6, t7, t8, t9 = handlePosition_tf(
                j["position"], i["position"])
            t3 = handleXpath(
                j["xpath"], i["xpath"])
            t4 = handleContext(
                j["context"], i["context"])
            t.append(t1)
            t.append(t2)
            t.append(t3)
            t.append(t4)
            t.append(t5)
            t.append(t6)
            t.append(t7)
            t.append(t8)
            t.append(t9)
            temp.append(t)
        test.append(temp)
    print("A 和 B 一一对应已完成！")
    return np.array(test)


def getData(url):
    data = loadDataJson(url)
    return data["A"], data["B"]


def getWB(url):
    data = loadDataJson(url)
    # print("data in getWB:", data)
    return data[0]["w"], data[0]["b"]


def logistic_match(data, url_w_b):
    # 输入参数：需要判断数据的地址 & 使用的 w 和 b
    # 输出参数：res=[{A_text=" ", A_id=num, btn= },{},...,{}]
    # 第一步：提取需要处理的数据    data = { A=[A1,A2,...,An], B=[B1,B2,...,Bn] }
    # A, B = getData(url_data)
    print("正在进行逻辑回归算法匹配!")
    A = data["A"]
    B = data["B"]
    # 第二步：提取需要的 w, b       w=[], b=[]
    w, b = getWB(url_w_b)

    # 第三步：计算每个B对应的每个A的维度值
    # test = np.arr格式 [ [[x11,x12,x13,x14,x15],[x21,x22,x23,x24,x25],...,[xn1,xn2,xn3,xn4,xn5]]  ,..., ]
    test = handleTestData(A, B)
    len_test = len(test)
    res = []  # res记录每个B对应的最优匹配的A所需的内容
    for i in range(len_test):  # 循环每个B
        # 计算每个A对于B的sig()值
        temp_res = []
        for j in range(len(test[i])):
            val = w*(test[i][j].T)+b
            sig = sigmoid(sum(val))
            temp_res.append(sig)

        max_t_res = max(temp_res)
        if max_t_res < 0.68:

            res.append({
                "A_text": "",
                "btn": "input",
                "B_xPath": B[i]["xpath"],
                "B_type": B[i]["type"]})  # 如果认为没有与B匹配的A, 传入“null”
        else:  # 如果认为有与B匹配的A, 传入对应的信息
            max_index = temp_res.index(max_t_res)

            res.append({
                "A_text": A[max_index]["context"]["data"],
                "btn": "input",
                "B_xPath": B[i]["xpath"],
                "B_type": B[i]["type"]})

    return res


def deepNetwork_match(data, model_url):
    print("正在进行神经网络算法匹配!")
    A = data["A"]
    B = data["B"]

    test = handleTestData_tf(A, B)

    # # Same parameters as of 'ApeNet'
    # inputData = tflearn.input_data(shape=[None, 9])
    # layer_1 = tflearn.fully_connected(
    #     inputData, 32, activation='sigmoid', name='layer_1')
    # layer_2 = tflearn.fully_connected(
    #     layer_1, 108, activation='sigmoid', name='layer_2')
    # layer_3 = tflearn.fully_connected(
    #     layer_2, 64, activation='sigmoid', name='layer_3')
    # outputData = tflearn.fully_connected(
    #     layer_3, 2, activation='softmax', name='output')
    # net = tflearn.regression(outputData)

    # # Load the trained model
    # model = tflearn.DNN(net)
    model.load(model_url)

    # Prob存着每个B与每个A对应的匹配概率值
    Prob = []
    res = []  # res记录每个B对应的最优匹配的A所需的内容
    for i in range(len(test)):
        prediction = model.predict(test[i])
        # 选择概率最大的A
        max_A_val = prediction.min(axis=0)
        if max_A_val[0] > 0.5:  # 可认为没有A能代表这个B
            res.append({
                "A_text": "",
                "btn": "input",
                "B_xPath": B[i]["xpath"]})  # 如果认为没有与B匹配的A, 传入“null”
        else:  # 可认为这个A能代表这个B
            max_index = -1
            # 从每个组数据中选择概率判断最大的A作为B的结果
            for j in range(len(prediction)):
                if prediction[j][0] == max_A_val[0]:
                    max_index = j
                    break
            res.append({
                "A_text": A[max_index]["context"]["data"],
                "btn": "input",
                "B_xPath": B[i]["xpath"],
                "A_xPath": A[max_index]["xpath"],
                "area": B[i]["area"]})
        Prob.append(prediction)

    return res
