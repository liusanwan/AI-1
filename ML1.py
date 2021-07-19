# 本文当用于为输入字符串提取关键词，并判断该关键词是否可以代表某个控制主件的功能
# 输入参数：一段string类型的字符串
# 输出参数：(可以代表某个控件功能的关键词, 关键词能代表组件功能表述的概率）
import pynlpir


def keywordsExtract(text):

    s = ["请不要输入您的账号！", "禁止填写", "用户密码", "请填写密码", "搜索", "复制代码前请填写您的账号"]
    # open API
    pynlpir.open()
    # segmention word
    segments = pynlpir.segment(
        s[0], pos_tagging=True, pos_names='all', pos_english=False)

    # segments--一个元素为[分词,词性]的数组

    # print("Type of segmention words: {}".format(type(segments)))
    # print("Segmention words: {}".format(segments))
    # print("分词", '\t', 'parent:child')
    # for segment in segments:
    #     print(segment[0], '\t', segment[1])

    # close API
    pynlpir.close()

    # banWordSet 记录了一些特殊必要过滤掉的词
    banWordSet = ["请", "注意"]
    # imporWordSet 记录了一些十分重要的词（很大概率能代表空间功能）
    imporWordSet = ["账号", "账户", "密码", "password", "Password", "PASSWORD", "留言"]
    # 按顺序返回所有 动词/名词/副词，返回结果记录在 res 中
    res = ""
    ifEnough = False
    for segment in segments:
        if segment[0] in imporWordSet:
            ifEnough = True
            res += segment[0]
            continue
        if (segment[1] == "动词" or segment[1] == "名词" or segment[1] == "副词") and (segment[0] not in banWordSet):
            res += segment[0]

    print(res)

    return ifEnough, res

# ML1-使用逻辑回归方法，输入参数：keywordsExtract()返回的"关键词"信息对象{}，输出变量：属于“功能描述”的概率


def getProb(text):
    res = 0.0  # 概率值

    return res


if __name__ == '__main__':
    keywordsExtract("dd")
