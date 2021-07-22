from math import sqrt


def score(elem_text, text):

    elem_text = list(elem_text)

    if len(elem_text) == 0:
        return 0
    text = list(text)
    hitCount = 0        # 命中数：hitCount表示匹配字符的个数
    p_B = 0
    p_A = 0
    while p_A < len(elem_text):
        for i in range(p_B, len(text)):
            if elem_text[p_A] == text[i]:  # 如果这个字符匹配上了
                p_B = i+1
                hitCount += 1
                break
        p_A += 1
    # 计算res评分: 使用了对数组 先开根号再*10 的操作（体现每次命中带来不同的评分）
    return hitCount/max(len(elem_text), len(text))


def text_match(elements, text):
    # 传入参数：(elements--[element1,element2,...], text--"string")
    # 选择一个 element['A_text'] 与 text文本 最匹配的element
    max_score = 0
    max_index = -1
    for i in range(len(elements)):
        new_score = score(elements[i]["A_text"], text)
        if max_score < new_score:
            max_score = new_score
            max_index = i
    if text == "" or text.isspace() == True:
        return "space"      # text是无效搜索, 前端main.py里面需要做出反应
    return elements[max_index]
