# 本文档为判断新页面区域着色匹配算法
import json


def loadDataJson(url):
    # 加载文件夹
    with open(url, encoding='utf_8_sig') as load_f:
        data = []
        lines = load_f.readlines()
        for l in lines:
            data.append(json.loads(l))
    return data[0]


def score(area_A, area_B):
    # area_A={"width":XX,
    #        "height":XX,
    #        "context":[text1,text2,...,textn],
    #        "A_num":XX,
    #        "input_num":XX,
    #        "button_num":XX,
    #        "select_num":XX,
    #        "width_all":XX,
    #        "height_all":XX}
    # 1) 面积比较           : 0.0~1.0
    # 2) 宽度占比比较   : 0.0~1.0
    # 3) 控件高度占比比较   : 0.0~1.0
    # 4) A签个数比较        : 0.0~1.0
    # 5) input签个数比较    : 0.0~1.0
    # 6) button签个数比较   : 0.0~1.0
    # 7) select签个数比较   : 0.0~1.0

    return 0


def area_match():

    # 传入值：
    # 文件读取：                     文件中保存着上次区域赋值的着色情况
    # 文件数据格式：
    # {
    # "红色":{红色区域的各种参数信息},
    # "蓝色":{蓝色区域的各种参数信息},
    # }

    # 颜色池：
    cols_list = ['红色', '灰色', '粉色', '绿色', '橙色', '橘色', '黄色', '蓝色', '紫色', '深灰色']

    # 第二次刷页面匹配后输出：  [ {"url"："红色" },  {"url":"蓝色"},...,{"url":"粉色"}]
    # 写入文件中：
    # {
    # "红色":{红色区域的各种参数信息},
    # "蓝色":{蓝色区域的各种参数信息},
    # }

    # 第一步：读取 "areas_color.txt"文件
    last_areas_clo = loadDataJson("areas_color.txt")
    print("last_areas_clo:", last_areas_clo)
    # 第二步：将与传入的 [区域1的各种参数信息, 区域2的各种参数信息, ..., 区域n的各种参数信息]
    #
    return []


if __name__ == '__main__':
    data = area_match()
