# coding:utf-8
import pandas as pd
from xpath import handleXpath
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
    # 输入数据的字典形式
    # 输出数据集的关键数据点
    # 返回值=[{
    #   mid_dist: XXX,
    #   nearest_dist: XXX,
    #   anceMatchRate: XXX,
    #   contMatchRate: XXX,
    #   "row": 0,
    #   "col": 0,
    #   ifMatch: True or False
    #  },...]

    # 创建：输出数据的格式
    res = []
    for i in range(len(data)):
        t = {
            "mid_dist": -1,
            "nearest_dist": -1,
            "anceMatchRate": -1,
            "contMatchRate": -1,
            "row": 0,
            "ifMatch": -1
        }

        t["mid_dist"], t["nearest_dist"], t["row"] = handlePosition(
            data[i]["A"]["position"], data[i]["B"]["position"])
        t["anceMatchRate"] = handleXpath(
            data[i]["A"]["xpath"], data[i]["B"]["xpath"])
        t["contMatchRate"] = handleContext(
            data[i]["A"]["context"], data[i]["B"]["context"])
        t["ifMatch"] = data[i]["Result"]
        res.append(t)

    # 处理：处理数据并赋值给返回变量res
    return res


def extractTrainData(url):
    # 加载训练 train_set 数据集
    data = loadDataJson(url)
    # 处理数据集
    res = handleTrainData(data)
    return res


def handleTestData(data):
    para_set = []
    label_set = []
    for i in range(len(data)):
        temp = []
        for j in range(len(data[i]["A"])):
            t = {
                "id": -1,
                "mid_dist": -1,
                "nearest_dist": -1,
                "anceMatchRate": -1,
                "contMatchRate": -1,
                "row": 0,
            }
            t["id"] = data[i]["A"][j]["id_A"]
            t["mid_dist"], t["nearest_dist"], t["row"] = handlePosition(
                data[i]["A"][j]["position"], data[i]["B"]["position"])
            t["anceMatchRate"] = handleXpath(
                data[i]["A"][j]["xpath"], data[i]["B"]["xpath"])
            t["contMatchRate"] = handleContext(
                data[i]["A"][j]["context"], data[i]["B"]["context"])
            temp.append(t)
        para_set.append(temp)
        label_set.append(data[i]["Result"])
    return para_set, label_set


def updateData(data):
    # 删掉
    return data


def extractTestData(url):
    # 加载训练 test_set 数据集
    data = loadDataJson(url)
    # 删除掉 data 中没有匹配的 B，以及与B距离过大的A
    data = updateData(data)
    # 处理数据集
    para_set, label_set = handleTestData(data)

    return para_set, label_set

# if __name__ == '__main__':
#     data = extractData(
#         'dataset/demo_data/test4/jsonData20210629093739.txt')
