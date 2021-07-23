from selenium import webdriver
import json
from lxml import etree
from getAllData import getAllElements
import tkinter
import tkinter.messagebox
from selenium.webdriver.common.by import By
# yang
# from logistic_match import logistic_match
# from logistic_match import deepNetwork_match
from text_match import text_match
import time
import re

driver = webdriver.Chrome()
# yang
# driver = webdriver.Chrome(
#     executable_path=r"G:\anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
url = "https://www.hnsrmyy.net/Register.html"  # 河南人民医院注册网页
# url = "https://www.landiannews.com/wp-login.php?action=register"      #
# url = "http://172.27.234.198/zentao/user-login-L3plbnRhby8=.html"     #禅道登入页面
# url = "https://upass.10jqka.com.cn/register"  # 同花顺注册界面
driver.get(url)
driver.maximize_window()
objJson = getAllElements(driver)
inputJson = {"A": objJson["A"], "B": objJson["B"]}
btn_list = objJson["C"]
input_list = objJson["B"]
lable_list = objJson["A"]

# yang
# 调用logistic_match 算法
# res = deepNetwork_match(objJson, "match_deepNetworks_tf9589")
# res = logistic_match(objJson, "best_para_w_b.txt")
# input_list = res

# button的颜色标记
for element in btn_list:
    xpath = element['B_xPath']
    b = driver.find_element_by_xpath(xpath)
    js_code = 'arguments[0].style.border = "2px red solid"'
    driver.execute_script(js_code, b)
# 入力框的颜色标记

for element in input_list:
    xpath = element['B_xPath']
    text = element['A_text']
    b = driver.find_element_by_xpath(xpath)
    js_code = 'arguments[0].style.border = "2px green solid";arguments[0].style.color = "#0cf373";arguments[0].type="text";'
    
    driver.execute_script(js_code, b)
    b.send_keys(text)

# 弹窗，修改值

win = tkinter.Tk()
win.title("输入值")
win.geometry("300x250+10+20")
# label = tkinter.Label(win, text="例：在XX输入XX", fg="black",
#                       font=("黑体", 10), anchor="ne")
# label.grid(row=0,column=0,padx=10)
# 绑定变量
e = tkinter.Variable()
entry = tkinter.Entry(win, textvariable=e)
entry.grid(row=1,column=0,padx=15)
jsonInfo = {}

def showinfo():
    inputValue = entry.get()
    value = (re.findall(r"输入(.+)",inputValue))[0]
    print(value)
    text = (re.findall(r"在(.+?)输入",inputValue))[0]
    
    # value = entry1.get()
    temp_elem = text_match(input_list, text)
    if temp_elem == "space":
        # 做出 "提示指令为空" 的反应
        tkinter.messagebox.showinfo("提示", "指令不能为空~")
    else:
        element = temp_elem
        print("element:", element)
        xpath = element['B_xPath']
        b = driver.find_element_by_xpath(xpath)
        b.clear()
        b.send_keys(value)
        js_code = 'arguments[0].style.border = "2px yellow solid";arguments[0].style.color = "black";'
        driver.execute_script(js_code, b)
        time.sleep(1)
        js_code1 = 'arguments[0].style.border = "2px green solid";arguments[0].style.color = "black";'
        driver.execute_script(js_code1, b)
        


button = tkinter.Button(win, text="确定", width=8, command=showinfo)
button.grid(row=1, column=1,padx=5)


def showinfoBtn():
    inputValue = entryBtn.get()
    text = (re.findall(r"点击(.+)",inputValue))[0]
    temp_elem = text_match(btn_list, text)
    if temp_elem == "space":
        # 做出 "提示指令为空" 的反应
        tkinter.messagebox.showinfo("提示", "指令不能为空~")
    else:
        element = temp_elem
        print("element:", element)
        xpath = element['B_xPath']
        b = driver.find_element_by_xpath(xpath)
        js_code = 'arguments[0].style.border = "2px yellow solid"'
        driver.execute_script(js_code, b)
        time.sleep(1)
        js_code1 = 'arguments[0].click();arguments[0].style.border = "2px red solid";'
        driver.execute_script(js_code1, b)


# label = tkinter.Label(win, text="例：点击XX", fg="black", font=(
#     "黑体", 10), anchor="ne")
# label.grid(row=2, column=0)
entryBtn = tkinter.Entry(win)
entryBtn.grid(row=3, column=0,padx=15)

buttonClick = tkinter.Button(win, text="确定", width=8, command=showinfoBtn)
buttonClick.grid(row=3, column=1,padx=5)

textBox = tkinter.Text(win)
text.pack()
win.mainloop()
