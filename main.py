from selenium import webdriver
import json
from lxml import etree
from getAllData import getAllElements
from tkinter import *
from selenium.webdriver.common.by import By
from logistic_match import logistic_match
driver = webdriver.Chrome(
    executable_path=r"G:\anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
url = "https://www.hnsrmyy.net/Register.html"
driver.get(url)
driver.maximize_window()
objJson = getAllElements(url)
inputJson = {"A": objJson["A"], "B": objJson["B"]}
print(objJson)
btn_list = objJson["C"]
input_list = objJson["B"]

# 调用logistic_match 算法
res = logistic_match(objJson, 'best_para_w_b.txt')
print("匹配结果：", res)
# button的颜色标记
for element in btn_list:
    xpath = element['xpath']
    b = driver.find_element_by_xpath(xpath)
    js_code = 'arguments[0].style.border = "2px red solid"'
    driver.execute_script(js_code, b)
# 入力框的颜色标记
for element in input_list:
    xpath = element['xpath']
    b = driver.find_element_by_xpath(xpath)
    js_code = 'arguments[0].style.border = "2px green solid"'
    driver.execute_script(js_code, b)
