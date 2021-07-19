from position import handlePosition
from context import handleContext
from xpath import handleXpath
import pandas as pd
import json
# handleMessage()是本文件的主要输出内容


def loadData(url):
    # 第一步：获取信息
    # A = {
    #     "position": {
    #         "left_up": (100, 100),
    #         "right_down": (200, 50)
    #     },
    #     "xpath": "",
    #     "context": {
    #         "data": "用户的账号"
    #     }
    # }
    # B = {
    #     "position": {
    #         "left_up": (250, 100),
    #         "right_down": (500, 50)
    #     },
    #     "xpath": "",
    #     "context": {
    #         "data": "请输入您的账号~"
    #     }
    # }
    data = pd.read_csv(url, header=None, encoding='gb2312')
    data = tran_to_dics(data)
    return data


def loadDataJson(url):
    f = open('dataset/demo_data/test_json/jsonData20210628161515.json')
    # 将json格式的数据映射成list的形式
    data = json.load(f)
    return data


def tran_to_dics(data):
    df = pd.DataFrame(data)
    print("df:", df)
    d_list = []
    for i_rows in data.index:
        temp = ""
        for i_cols in data.columns:
            temp += data[i_cols][i_rows]
        d_list.append(createDic(delTra(temp)))

    # 已将数据转化为一个字典元素的列表 d_list
    # print("d_list:", d_list)

    return d_list


def createDic(text):
    res = {
        "A": {
            "position": {
                "left_up": (0, 0),
                "right_down": (0, 0)
            },
            "xpath": "",
            "context": {
                "data": ""
            }
        },
        "B": {
            "position": {
                "left_up": (0, 0),
                "right_down": (0, 0)
            },
            "xpath": "",
            "context": {
                "data": ""
            }
        },
        "Result": False
    }
    # 将 "A","B","Result"分割
    ind_A = text.find("\"A\":")
    ind_B = text.find("\"B\":")
    ind_Res = text.find("\"Result\":")
    t_A = text[ind_A:ind_B]
    t_B = text[ind_B:ind_Res]
    t_Res = text[ind_Res:-1]

    # 在 A 中寻找 "left_up","right_down","xpath","context","data","Text:"
    ind_left_up_A = t_A.find("\"left_up\":")
    ind_right_down_A = t_A.find("\"right_down\":")
    ind_xpath_A = t_A.find("\"xpath\":")
    ind_context_A = t_A.find("\"context\":")
    #ind_data_A = t_A.find("\"data\":")
    ind_text_A = t_A.find("Text:")

    num = t_A[ind_left_up_A+12:ind_right_down_A-2].split(" ")
    res["A"]["position"]["left_up"] = (int(num[0]), int(num[1]))
    num = t_A[ind_right_down_A+15:ind_xpath_A-3].split(" ")
    res["A"]["position"]["right_down"] = (int(num[0]), int(num[1]))
    res["A"]["xpath"] = t_A[ind_xpath_A+10:ind_context_A-2]
    res["A"]["context"]["data"] = t_A[ind_text_A+5:-5]
    print("res[A][context][data]:", res["A"]["context"]["data"])

    # 在 B 中寻找 "left_up","right_down","xpath","context","data","Placeholder"
    ind_left_up_B = t_B.find("\"left_up\":")
    ind_right_down_B = t_B.find("\"right_down\":")
    ind_xpath_B = t_B.find("\"xpath\":")
    ind_context_B = t_B.find("\"context\":")
    ind_data_B = t_B.find("Placeholder:")

    num = t_B[ind_left_up_B+12:ind_right_down_B-2].split(" ")
    res["B"]["position"]["left_up"] = (int(num[0]), int(num[1]))
    num = t_B[ind_right_down_B+15:ind_xpath_B-3].split(" ")
    res["B"]["position"]["right_down"] = (int(num[0]), int(num[1]))
    res["B"]["xpath"] = t_B[ind_xpath_B+10:ind_context_B-2]
    res["B"]["context"]["data"] = t_B[ind_data_B+12:-5]
    print("res[B][context][data]")
    # 将 Result 中的 Result 信息添加进去
    res["Result"] = t_Res[10:]

    return res


def delTra(text):
    authority = True
    # for i in range(len(text)-1):
    i = 0
    while i < len(text)-1:
        if text[i] == "\\" and authority == True:
            text = text[:i]+text[i+1:]
            authority = False
        else:
            authority = True
            i += 1
        if text[i] == "\\" and text[i+1] == "t":
            text = text[:i]+text[i+2:]
    return text


def createRes(nums):
    res = []

    for i in range(nums):
        t = {
            "mid_dist": -1,
            "nearest_dist": -1,
            "anceMatchRate": -1,
            "contMatchRate": -1,
            "row": 0,
            "col": 0,
            "ifMatch": False
        }
        res.append(t)
    return res


def extractData(url):
    print("--正在执行 handleMessage()")

    # 第一步：获取信息 并 将数据转化为字典格式
    data = loadData(url)

    print(" 1.数据已被加载为字典格式~")
    #print("1.data:", data)

    # 第二步：根据data的大小，建立res返回数据集
    res = createRes(len(data))
    #print("res:", res)
    print(" 2.返回数据集res创建完成~")
    #print("2.res:", res)
    # res--一个元素为对象的列表
    # 对象是每一对 A和 B：
    # {
    #   mid_dist: XXX,
    #   nearest_dist: XXX,
    #   anceMatchRate: XXX,
    #   contMatchRate: XXX,
    #   ifMatch: True or False
    #  }

    # 第三步：位置信息处理   mid_dist-中心点距离，[10^2~10^4]
    # 调用position.py，输入参数：( A.position, B.position)
    # A.position: {
    #     left_up : (x_l, y_l),
    #     right_down : (x_r, y_r)
    # }
    #mid_dist, nearest_dist = handlePosition(A["position"], B["position"])

    # 第四步：祖先信息处理  anceMatchRate~[0,1]
    # 调用ancestor.py，输入参数：( A.ancestor, B.ancestor)
    # A.ancestor: {
    #     url:"XXXXX"
    # }
    #anceMatchRate = handleAncestor(A["ancestor"], B["ancestor"])

    # 第五步：内容信息处理  contMatchRate~[0,1]
    # 调用context.py，输入参数：( A.context, B.context)
    # A.context:{
    #     data:"XXXXX"
    # }
    #contMatchRate = handleContext(A["context"], B["context"])
    # print("res[0]", res[0])
    # print("handlePos:", handlePosition(
    #     data[0]["A"]["position"], data[0]["B"]["position"]))
    # print("len(res):", len(res))
    # print("len(data):", len(data))
    for i in range(len(data)):
        res[i]["mid_dist"], res[i]["nearest_dist"], res[i]["row"], res[i]["col"] = handlePosition(
            data[i]["A"]["position"], data[i]["B"]["position"])
        res[i]["anceMatchRate"] = handleXpath(
            data[i]["A"]["xpath"], data[i]["B"]["xpath"])
        res[i]["contMatchRate"] = handleContext(
            data[i]["A"]["context"], data[i]["B"]["context"])
    print(" 3.位置信息已处理并加载~")
    print(" 4.祖先信息已处理并加载~")
    print(" 5.内容信息已处理并加载~")

    print("res:", res)
    return res
