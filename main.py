from selenium import webdriver
import json
from lxml import etree
from getAllData import getAllElements
import tkinter
import tkinter.messagebox
from selenium.webdriver.common.by import By
from logistic_match import logistic_match
from logistic_match import deepNetwork_match
from text_match import text_match

driver = webdriver.Chrome(
    executable_path=r"G:\anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
url = "https://www.hnsrmyy.net/Register.html"  # 河南人民医院注册网页
# url = "https://www.landiannews.com/wp-login.php?action=register"      #
# url = "http://172.27.234.198/zentao/user-login-L3plbnRhby8=.html"     #禅道登入页面
# url = "https://upass.10jqka.com.cn/register"  # 同花顺注册界面
driver.get(url)
driver.maximize_window()
objJson = getAllElements(driver)
inputJson = {"A": objJson["A"], "B": objJson["B"]}
btn_list = objJson["C"]


# 调用logistic_match 算法
res = deepNetwork_match(objJson, "match_deepNetworks_tf9589")
# res = logistic_match(objJson, "best_para_w_b.txt")
input_list = res

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
    js_code = 'arguments[0].style.border = "2px green solid";arguments[0].style.color = "#0cf373";arguments[0].type="text"'
    # js_code1 = 'arguments[0].value = "text"'
    driver.execute_script(js_code, b)
    b.send_keys(text)

# 弹窗，修改值

win = tkinter.Tk()
win.title("输入值")
win.geometry("300x250+10+20")
label = tkinter.Label(win, text="lable名", fg="black",
                      font=("黑体", 10), justify="left", anchor="ne")
label.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=2)
# 绑定变量
e = tkinter.Variable()
entry1 = tkinter.Entry(win, textvariable=e)
entry1.grid(row=0, column=1, padx=5, pady=10, ipadx=1, ipady=2)
label = tkinter.Label(win, text="输入值", fg="black", font=(
    "黑体", 10), justify="left", anchor="ne")
label.grid(row=1, column=0, padx=5, pady=5, ipadx=1, ipady=2)
entry = tkinter.Entry(win)
entry.grid(row=1, column=1, padx=5, pady=5, ipadx=1, ipady=2)
jsonInfo = {}


def showinfo():
    text = entry1.get()
    value = entry.get()
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
        js_code = 'arguments[0].style.border = "2px green solid";arguments[0].style.color = "black";'
        driver.execute_script(js_code, b)
        b.send_keys(value)


button = tkinter.Button(win, text="提交", width=8, command=showinfo)
button.grid(row=2, column=1, columnspan=2, padx=5, pady=0, ipadx=1, ipady=2)


def showinfoBtn():
    text = entryBtn.get()
    value = entryBtn.get()
    temp_elem = text_match(btn_list, text)
    if temp_elem == "space":
        # 做出 "提示指令为空" 的反应
        tkinter.messagebox.showinfo("提示", "指令不能为空~")
    else:
        element = temp_elem
        print("element:", element)
        xpath = element['B_xPath']
        b = driver.find_element_by_xpath(xpath)
        js_code = 'arguments[0].click()'
        driver.execute_script(js_code, b)


label = tkinter.Label(win, text="按钮名", fg="black", font=(
    "黑体", 10), justify="left", anchor="ne")
label.grid(row=4, column=0, padx=15, pady=10, ipadx=1, ipady=2)
entryBtn = tkinter.Entry(win)
entryBtn.grid(row=4, column=1, padx=15, pady=10, ipadx=1, ipady=2)

buttonClick = tkinter.Button(win, text="点击", width=8, command=showinfoBtn)
buttonClick.grid(row=5, column=1, columnspan=2,
                 padx=5, pady=10, ipadx=1, ipady=2)
win.mainloop()
