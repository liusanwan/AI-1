def handleXpath(A_xpath, B_xpath):
    res = 0.0
    A_tabs = A_xpath.split("/")
    B_tabs = B_xpath.split("/")
    #print("A_tabs:", A_tabs)
    #print("B_tabs:", B_tabs)
    min_len = min(len(A_tabs), len(B_tabs))
    max_len = max(len(A_tabs), len(B_tabs))
    match_nums = 0
    for i in range(min_len):
        if A_tabs[i] != B_tabs[i]:
            match_nums = i
            break
    if max_len-match_nums >= 7:
        return 0.0
    else:
        # 除以10，再取平方
        return pow((match_nums/max_len*100)/10, 2)/100
