# 本文件用于生成 应用于“ML2_deepLearning.py”文件的数据集
from xpath import handleXpath
import pandas as pd
from context import handleContext
from position import handlePosition
import json


def loadDataJson(url):
    # 加载文件夹
    data = []
    with open(url, encoding='utf_8_sig') as load_f:
        lines = load_f.readlines()
        for l in lines:
            data.append(json.loads(l))
    return data


def handleTrainData(data):
    # 创建：输出数据的格式
    res = []
    for i in range(len(data)):
        # t = {
        #     "mid_dist": -1,
        #     "nearest_dist": -1,
        #     "anceMatchRate": -1,
        #     "contMatchRate": -1,
        #     "row": 0,
        #     "colon": 0,
        #     "ifMatch": -1,
        #     ""
        # }
        t = []
        t1, t2, t5, t6, t7, t8, t9 = handlePosition(
            data[i]["A"]["position"], data[i]["B"]["position"])
        t3 = handleXpath(
            data[i]["A"]["xpath"], data[i]["B"]["xpath"])
        t4 = handleContext(
            data[i]["A"]["context"], data[i]["B"]["context"])
        t10 = data[i]["Result"]
        t.append(t1)
        t.append(t2)
        t.append(t3)
        t.append(t4)
        t.append(t5)
        t.append(t6)
        t.append(t7)
        t.append(t8)
        t.append(t9)
        t.append(t10)
        res.append(t)

    # 处理：处理数据并赋值给返回变量res
    return res


def loadDataJson(url):
    # 加载文件夹
    data = []
    with open(url, encoding='utf_8_sig') as load_f:
        lines = load_f.readlines()
        for l in lines:
            data.append(json.loads(l))
    return data


def extractTrainData(url):
    # 加载训练 train_set 数据集
    data = loadDataJson(url)
    # 处理数据集
    res = handleTrainData(data)
    print("res", res)
    res = pd.DataFrame(data=res)
    res.to_csv('dataset/tfLearn_data/data3.csv', encoding='utf-8')
    return res


if __name__ == '__main__':
    extractTrainData('dataset/demo_data/test7/trainData_part2.txt')
