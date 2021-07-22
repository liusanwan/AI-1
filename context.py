from math import sqrt


def method_1(A_text, B_text):  # 短文本逐字符传递匹配算法
    A_chars = list(A_text)
    res = 0.0           # 返回值：res表示匹配率，是一个[0.0,1.0]的浮点数
    hitCount = 0        # 命中数：hitCount表示匹配字符的个数

    p_B = 0
    p_A = 0
    while p_A < len(A_text):
        for i in range(p_B, len(B_text)):
            if A_chars[p_A] == B_text[i]:  # 如果这个字符匹配上了
                p_B = i+1
                hitCount += 1
                break
        p_A += 1
    # 计算res评分: 使用了对数组 先开根号再*10 的操作（体现每次命中带来不同的评分）
    return sqrt(hitCount/len(A_chars)*100)/10


def method_2(A_text, B_text):  # 长文本逐字符传递匹配算法
    return max(method_1(A_text[:5], B_text), method_1(A_text[-5:], B_text))


def handleContext(A_cont, B_cont):
    A_text = A_cont['data']
    B_text = B_cont['data']
    # 文本处理
    # 如果 A_cont 或者 B_cont 存在空字符串 ""
    if A_text == "" or B_text == "" or A_text == " " or B_text == " ":
        return 0.0

    # 如果二者都不是空字符串：
    # 以A_cont为匹配项，B_cont为待匹配项
    else:
        if len(A_text) <= 5:    # 如果A_cont的字符长度小于等于5, 调用短文本逐字符传递匹配算法 method_1(A_text,B_text)
            # 返回文字匹配率 conMatchRate
            return method_1(A_text, B_text)
        else:                   # 如果A_cont的字符长度大于5, 取A_cont前5个字符与后5个字符分别使用method_1算法与B_text进行匹配
            return method_2(A_text, B_text)
