
def getArea(input_list):
    #input_list= ['/html/body/div[2]/div[1]/div[1]/form/ul/li[1]/input', '/html/body/div[2]/div[1]/div[1]/form/ul/li[2]/input', '/html/body/div[2]/div[1]/div[1]/form/ul/li[3]/input', '/html/body/div[2]/div[1]/div[1]/form/ul/li[4]/input', '/html/body/div[2]/div[1]/div[1]/form/ul/li[5]/input', '/html/body/div[2]/div[1]/div[1]/form/ul/li[6]/input', '/html/body/div[2]/div[1]/div[1]/form/ul/li[7]/label/input', '/html/body/div[1]/div/ul[1]/li[1]/a', '/html/body/div[1]/div/ul[1]/li[2]/a', '/html/body/div[1]/div/ul[1]/li[3]/a', '/html/body/div[1]/div/ul[2]/li[1]/a', '/html/body/div[1]/div/ul[2]/li[2]/a', '/html/body/div[1]/div/ul[2]/li[3]/a', '/html/body/div[1]/div/ul[2]/li[4]/a', '/html/body/div[2]/div[1]/div[1]/form/ul/li[5]/a[2]/span', '/html/body/div[2]/div[1]/div[1]/form/ul/li[7]/label/a', '/html/body/div[2]/div[1]/div[1]/form/ul/li[8]/input', '/html/body/div[2]/div[3]/ul/li[1]/a', '/html/body/div[2]/div[3]/ul/li[2]/a', '/html/body/div[2]/div[3]/ul/li[3]/a', '/html/body/div[2]/div[3]/ul/li[4]/a', '/html/body/div[2]/div[3]/ul/li[5]/a', '/html/body/div[2]/div[3]/ul/li[6]/a', '/html/body/div[1]/div/div/span', '/html/body/div[2]/div[1]/div[1]/div', '/html/body/div[2]/div[1]/div[1]/form/ul/li[1]/span', '/html/body/div[2]/div[1]/div[1]/form/ul/li[2]/span', '/html/body/div[2]/div[1]/div[1]/form/ul/li[3]/span', '/html/body/div[2]/div[1]/div[1]/form/ul/li[4]/span', '/html/body/div[2]/div[1]/div[1]/form/ul/li[5]/span', '/html/body/div[2]/div[1]/div[1]/form/ul/li[6]/span', '/html/body/div[2]/div[1]/div[1]/form/ul/li[6]/div/span[1]', '/html/body/div[2]/div[1]/div[1]/form/ul/li[7]/label/span', '/html/body/div[2]/div[1]/div[2]/div/p', '/html/body/div[2]/div[1]/div[2]/p[1]/span', '/html/body/div[2]/div[1]/div[2]/p[2]', '/html/body/div[2]/div[1]/div[2]/p[3]', '/html/body/div[2]/div[3]/span', '/html/body/div[2]/div[3]/ul/li[1]/div[1]', '/html/body/div[2]/div[3]/ul/li[1]/div[2]', '/html/body/div[2]/div[3]/ul/li[2]/div[1]', '/html/body/div[2]/div[3]/ul/li[2]/div[2]', '/html/body/div[2]/div[3]/ul/li[3]/div[1]', '/html/body/div[2]/div[3]/ul/li[3]/div[2]', '/html/body/div[2]/div[3]/ul/li[4]/div[1]', '/html/body/div[2]/div[3]/ul/li[4]/div[2]', '/html/body/div[2]/div[3]/ul/li[5]/div[1]', '/html/body/div[2]/div[3]/ul/li[5]/div[2]', '/html/body/div[2]/div[3]/ul/li[6]/div[1]', '/html/body/div[2]/div[3]/ul/li[6]/div[2]']

    result_list = []
    for il in input_list:
        input = il.split("/")
        k_list=[]
        v_list=[]
        for i in input:
            if i == "":
                continue
            kv = i.split("[")
            k = kv[0]
            if len(kv) > 1:
                v = kv[1].split("]")[0]
            else:
                v = '0'
            k_list.append(k)
            v_list.append(v)
        result_list.append({"k_list": k_list, "v_list": v_list,'original':il})
    area_list = []
    for i in range(len(result_list)):
        for j in range(i + 1, len(result_list)):
            if result_list[i]['k_list'] == result_list[j]['k_list']:
                m = 0
                area = ''
                for k in range(len(result_list[i]['v_list'])):
                    if result_list[i]['v_list'][k] != result_list[j]['v_list'][k]:
                        m += 1
                        if m > 1:
                            break
                    if m < 1:
                        if result_list[i]['v_list'][k] == '0':
                            area = area + "/" + result_list[i]['k_list'][k]
                        else:
                            area = area + "/" + result_list[i]['k_list'][k] + '[' + result_list[i]['v_list'][k] + ']'
                if m > 1:
                    continue
            else:
                continue
            if area not in area_list:
                area_list.append(area)

    final_list = {}
    for i in range(len(area_list)):
        cancel_flag = True
        for j in range(len(area_list)):
            if i == j:
                continue
            if  area_list[j] in area_list[i]:
                cancel_flag = False
                break
        if cancel_flag:
            final_list[area_list[i]] = []
    #print(final_list)


    for i in range(len(input_list)):
        for k in final_list:
            if k in input_list[i]:
                final_list[k].append(input_list[i])
    print(final_list)
    return final_list



