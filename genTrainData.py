import copy
import random
import json
import datetime
TrainingDataSet = []

# rawdata = {}

def moveAll(rawdata):
    x = random.randint(0, 200)
    y = random.randint(0, 200)
    rawdata["A"]["position"]["left_up"][0] += x
    rawdata["A"]["position"]["left_up"][1] += y
    rawdata["A"]["position"]["right_down"][0] += x
    rawdata["A"]["position"]["right_down"][1] += y
    rawdata["B"]["position"]["left_up"][0] += x
    rawdata["B"]["position"]["left_up"][1] += y
    rawdata["B"]["position"]["right_down"][0] += x
    rawdata["B"]["position"]["right_down"][1] += y
    return rawdata


def MoveB(rawData):
    length = random.randint(0, 5)
    if rawData["B"]["position"]["left_up"][0] - rawData["A"]["position"]["left_up"][0] > \
            rawData["B"]["position"]["left_up"][1] - rawData["A"]["position"]["left_up"][1]:
        # 说明此种情况A、B两控件为横置
        rawData["B"]["position"]["left_up"][0] += length
        rawData["B"]["position"]["right_down"][0] += length
        return rawData, '横置'
    else:
        # 说明此种情况A、B两控件为纵置
        rawData["B"]["position"]["left_up"][1] += length
        rawData["B"]["position"]["right_down"][1] += length
        return rawData, '纵置'


def CreateRowRight(rawData):
    newData = copy.deepcopy(rawData)
    # 计算原来 A 的宽度和高度：
    width = newData["A"]["position"]["right_down"][0] - newData["A"]["position"]["left_up"][0]
    height = newData["A"]["position"]["right_down"][1] - newData["A"]["position"]["left_up"][1]
    # A左上角X移动到B右下X的右侧  Y轴不变
    newData["A"]["position"]["left_up"][0] = newData["B"]["position"]["right_down"][0] + \
                                             newData["B"]["position"]["left_up"][0] - \
                                             newData["A"]["position"]["right_down"][0]
    # 重新计算A的右下角
    newData["A"]["position"]["right_down"][0] = newData["A"]["position"]["left_up"][0] + width
    newData["A"]["position"]["right_down"][1] = newData["A"]["position"]["left_up"][1] + height
    newData["Result"] = '0'
    return newData


def CreateRowDown(rawData):
    newData = copy.deepcopy(rawData)
    # 计算原来 A 的宽度和高度：
    width = newData["A"]["position"]["right_down"][0] - newData["A"]["position"]["left_up"][0]
    height = newData["A"]["position"]["right_down"][1] - newData["A"]["position"]["left_up"][1]
    # A左上角Y移动到B的左下角Y的下方 其间距等于原来横向X轴的间距
    newData["A"]["position"]["left_up"][1] = newData["B"]["position"]["right_down"][1] + \
                                             newData["B"]["position"]["left_up"][0] - \
                                             newData["A"]["position"]["right_down"][0]
    # A左上角X移动到B的左上角X
    #newData["A"]["position"]["left_up"][0] = newData["B"]["position"]["left_up"][0] + random.randint(-10, 50)
    newData["A"]["position"]["left_up"][0] = newData["B"]["position"]["left_up"][0]
    # 重新计算A的右下角
    newData["A"]["position"]["right_down"][0] = newData["A"]["position"]["left_up"][0] + width
    newData["A"]["position"]["right_down"][1] = newData["A"]["position"]["left_up"][1] + height
    newData["Result"] = '0'
    return newData


def CreateRowUp(rawData):
    newData = copy.deepcopy(rawData)
    # 计算原来 A 的宽度和高度：
    width = newData["A"]["position"]["right_down"][0] - newData["A"]["position"]["left_up"][0]
    height = newData["A"]["position"]["right_down"][1] - newData["A"]["position"]["left_up"][1]
    # A左上角Y移动到B的左上角Y的上方 其间距等于原来横向X轴的间距
    newData["A"]["position"]["left_up"][1] = newData["B"]["position"]["left_up"][1] - (
            newData["B"]["position"]["left_up"][0] - newData["A"]["position"]["right_down"][0] + height)
    # A左上角X移动到B的左上角X
    #newData["A"]["position"]["left_up"][0] = newData["B"]["position"]["left_up"][0] + random.randint(-5, 50)
    newData["A"]["position"]["left_up"][0] = newData["B"]["position"]["left_up"][0]
    # 重新计算A的右下角
    newData["A"]["position"]["right_down"][0] = newData["A"]["position"]["left_up"][0] + width
    newData["A"]["position"]["right_down"][1] = newData["A"]["position"]["left_up"][1] + height
    return newData


def CreateColRight(rawData):
    newData = copy.deepcopy(rawData)
    # 计算原来 A 的宽度和高度：
    width = newData["A"]["position"]["right_down"][0] - newData["A"]["position"]["left_up"][0]
    height = newData["A"]["position"]["right_down"][1] - newData["A"]["position"]["left_up"][1]
    # A左上角X移动到B右下X的右侧 其间距等于原来纵向Y轴的间距
    newData["A"]["position"]["left_up"][0] = newData["B"]["position"]["right_down"][0] + \
                                             newData["B"]["position"]["left_up"][1] - \
                                             newData["A"]["position"]["right_down"][1]
    # A左上角Y移动到B的左上角Y
    newData["A"]["position"]["left_up"][1] = newData["B"]["position"]["left_up"][1]
    # 重新计算A的右下角
    newData["A"]["position"]["right_down"][0] = newData["A"]["position"]["left_up"][0] + width
    newData["A"]["position"]["right_down"][1] = newData["A"]["position"]["left_up"][1] + height
    newData["Result"] = '0'
    return newData


def CreateColDown(rawData):
    newData = copy.deepcopy(rawData)
    # 计算原来 A 的宽度和高度：
    width = newData["A"]["position"]["right_down"][0] - newData["A"]["position"]["left_up"][0]
    height = newData["A"]["position"]["right_down"][1] - newData["A"]["position"]["left_up"][1]
    # A左上角Y移动到B右下角Y的下方
    newData["A"]["position"]["left_up"][1] = newData["B"]["position"]["right_down"][1] + \
                                             newData["B"]["position"]["left_up"][1] - \
                                             newData["A"]["position"]["right_down"][1] 
    # 重新计算A的右下角
    newData["A"]["position"]["right_down"][0] = newData["A"]["position"]["left_up"][0] + width
    newData["A"]["position"]["right_down"][1] = newData["A"]["position"]["left_up"][1] + height
    newData["Result"] = '0'
    return newData


def CreateColLeft(rawData):
    newData = copy.deepcopy(rawData)
    # 计算原来 A 的宽度和高度：
    width = newData["A"]["position"]["right_down"][0] - newData["A"]["position"]["left_up"][0]
    height = newData["A"]["position"]["right_down"][1] - newData["A"]["position"]["left_up"][1]
    width = 50
    # A左上角X移动到B的左上角X 的左侧
    newData["A"]["position"]["left_up"][0] = newData["B"]["position"]["left_up"][0] - (
            newData["B"]["position"]["left_up"][1] - newData["A"]["position"]["right_down"][1] + width)
    # A左上角Y移动到B的左上角Y
    newData["A"]["position"]["left_up"][1] = newData["B"]["position"]["left_up"][1]
    # 重新计算A的右下角
    newData["A"]["position"]["right_down"][0] = newData["A"]["position"]["left_up"][0] + width
    newData["A"]["position"]["right_down"][1] = newData["A"]["position"]["left_up"][1] + height
    return newData

def domain():
    f = open("C:/jsonData/broadwise/001.txt",'r',encoding='UTF-8')
    lines=f.readlines()
    for i in lines :
        rawdata = json.loads(i)
        print(rawdata)
        rawdata = moveAll(rawdata)
        rawdata, way = MoveB(rawdata)

        TrainingDataSet.append(rawdata)

        if way == '横置':
            TrainingDataSet.append(CreateRowRight(rawdata))
            TrainingDataSet.append(CreateRowDown(rawdata))
            TrainingDataSet.append(CreateRowUp(rawdata))
        elif way == '纵置':
            TrainingDataSet.append(CreateColRight(rawdata))
            TrainingDataSet.append(CreateColDown(rawdata))
            TrainingDataSet.append(CreateColLeft(rawdata))

    for trainingData in TrainingDataSet:
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        path = 'D:/trainData/'
        fileName = path +"trainData" + str(dt)
        with open(fileName + '.txt', 'a') as file_object:
            file_object.write(json.dumps(trainingData,ensure_ascii=False) + "\n")


domain()

