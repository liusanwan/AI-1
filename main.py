import json
from lxml import etree
from getAllData import getAllElements
# from selenium.webdriver.common.by import By
# yang
from logistic_match import logistic_match
from logistic_match import deepNetwork_match

def loadChrome(driver):
    objJson,areaRange,color_list = getAllElements(driver)
    global inputJson 
    global btn_list
    global input_list
    global lable_list



    inputJson = {"A": objJson["A"], "B": objJson["B"]}
    btn_list = objJson["C"]
    input_list = objJson["B"]
    lable_list = objJson["A"]

    # 调用logistic_match 算法
    res = deepNetwork_match(objJson, "5_layers_64\match_64-64-64-64_tf9740")
    # res = logistic_match(objJson, "best_para_w_b.txt")
    input_list = res
    # print("sddsddd"+str(res))

    # button的颜色标记
    for element in btn_list:
        xpath = element['B_xPath']
        b = driver.find_element_by_xpath(xpath)
        js_code = 'arguments[0].style.border = "2px red solid"'
        driver.execute_script(js_code, b)

    # areaRange的颜色标记
    color_index = 0
    for element in areaRange:
        xpath = element
        b = driver.find_element_by_xpath(xpath)
        js_code = 'arguments[0].style.backgroundColor = "' + color_list[color_index] + '"' 
        driver.execute_script(js_code, b)
        color_index += 1
    # 入力框的颜色标记

    for element in input_list:
        xpath = element['B_xPath']
        # text = element['B_text']
        b = driver.find_element_by_xpath(xpath)
        js_code = 'arguments[0].style.border = "2px green solid";arguments[0].style.color = "#0cf373";arguments[0].type="text";'
        
        driver.execute_script(js_code, b)
        # b.send_keys(text)
        
    return input_list,btn_list

