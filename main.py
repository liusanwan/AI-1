from selenium import webdriver
import json
from lxml import etree
from getAllData import getAllElements
import tkinter
import tkinter.messagebox
from selenium.webdriver.common.by import By
# yang
from logistic_match import logistic_match
from logistic_match import deepNetwork_match
from text_match import text_match
import time
import re



driver = webdriver.Chrome()
# yang
# driver = webdriver.Chrome(
#     executable_path=r"G:\anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
# url = "https://www.hnsrmyy.net/Register.html"  # 河南人民医院注册网页
# url = "https://www.landiannews.com/wp-login.php?action=register"      #
# url = "http://172.27.234.198/zentao/user-login-L3plbnRhby8=.html"     #禅道登入页面
# url = "https://upass.10jqka.com.cn/register"  # 同花顺注册界面
# url = "https://www.mycar168.com/member/register.php"

# testdata1
# url = "http://www.gezhongji.com/user/register"

# testdata2
# url = "http://u.pageadmin.net/Reg/"
# 1
url = "http://wlwz.changsha.gov.cn/webapp/cs/register/register_2.htm"

# url = "http://member.djjlll.com/register.html"

#http://hi.jiameng.com/register/register.html


# url = ''
#https://www.landiannews.com/wp-login.php?action=register
driver.get(url)
driver.maximize_window()
objJson,areaRange = getAllElements(driver)
global inputJson 
global btn_list
global input_list
global lable_list
color_list_index = ['rgb(224 22 22 / 39%)','rgb(229 229 243 / 45%)','rgb(226 110 236 / 33%)','rgb(162 243 83 / 33%)','rgb(255 231 3 / 50%)','rgb(255 137 3 / 50%)','rgb(245 255 3 / 53%)'
,'rgb(15 224 191 / 53%)','rgb(157 70 228 / 26%)','rgb(8 8 8 / 26%)']

color_list = {'红色':"rgb(224 22 22 / 39%)",'灰色':"rgb(229 229 243 / 45%)",'粉色':"rgb(226 110 236 / 33%)"
,'绿色':"rgb(162 243 83 / 33%)",'橙色':"rgb(255 231 3 / 50%)",'橘色':"rgb(255 137 3 / 50%)",'黄色':"rgb(245 255 3 / 53%)"
,'蓝色':"rgb(15 224 191 / 53%)",'紫色':"rgb(157 70 228 / 26%)",'深灰色':"rgb(8 8 8 / 26%)"}

inputJson = {"A": objJson["A"], "B": objJson["B"]}
btn_list = objJson["C"]
input_list = objJson["B"]
lable_list = objJson["A"]


def reloadChrome():
    global inputJson 
    global btn_list
    global input_list
    global lable_list
    inputJson ,btn_list ,input_list ,lable_list = loadChrome()

def loadChrome():
    url= entry_url.get()
    driver.get(url)
    driver.maximize_window()
    objJson,areaRange = getAllElements(driver)
    inputJson = {"A": objJson["A"], "B": objJson["B"]}
    btn_list = objJson["C"]
    # yang
    # 调用logistic_match 算法
    res = deepNetwork_match(objJson, "match_deepNetworks_tf9589")
    # res = logistic_match(objJson, "best_para_w_b.txt")
    input_list = res
    

# areaRange的颜色标记
    color_index = 0
    for element in areaRange:
        xpath = element
        b = driver.find_element_by_xpath(xpath)
        js_code = 'arguments[0].style.backgroundColor = "' + color_list_index[color_index] + '"' 
        driver.execute_script(js_code, b)
        color_index += 1
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
    return  inputJson ,btn_list ,input_list ,lable_list



# yang
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

# areaRange的颜色标记
color_index = 0

for element in areaRange:
    xpath = element
    b = driver.find_element_by_xpath(xpath)
    js_code = 'arguments[0].style.backgroundColor = "' + color_list_index[color_index] + '"' 
    driver.execute_script(js_code, b)
    color_index += 1
# 入力框的颜色标记

for element in input_list:
    xpath = element['B_xPath']
    text = element['A_text']
    print(text)
    b = driver.find_element_by_xpath(xpath)
    js_code = 'arguments[0].style.border = "2px green solid";arguments[0].style.color = "#0cf373";arguments[0].type="text";'
    
    driver.execute_script(js_code, b)
    b.send_keys(text)

# 弹窗，修改值

win = tkinter.Tk()
win.title("输入值")
win.geometry("500x300+10+20")
# 绑定变量
label = tkinter.Label(win, text="Url", fg="black",
                      font=("黑体", 10), anchor="ne")
label.place(x=10,y=10)
entry_url = tkinter.Entry(win,width=39)
entry_url.place(x=50,y=10)
parseCmd = tkinter.Button(win, text="执行", width=8,height=1, command=reloadChrome)
parseCmd.place(x=340,y=10)

labelCmd = tkinter.Label(win, text="Cmd", fg="black",
                      font=("黑体", 10), anchor="ne")
labelCmd.place(x=10,y=50)
e = tkinter.Variable()
entry1 = tkinter.Entry(win, width=39)
entry1.place(x=50,y=50)
jsonInfo = {}
textinsert = ''

def showinfo(i):
    if i =="":
        inputValue = entry1.get()
    else:
        inputValue = i
    if "输入" in inputValue:
        input_color_list = []
        areaCol = (re.findall(r"在(.+?)区域",inputValue))[0]
        value = (re.findall(r"输入(.+)",inputValue))[0]
        text = (re.findall(r"在(.+?)输入",inputValue))[0]
        if areaCol == "粉色":
            i=0
        elif areaCol == "黄色":
            i=1
        elif areaCol == "绿色":
            i=2
        elif areaCol == "蓝色":
            i=3
        elif areaCol == "紫色":
            i=4
        elif areaCol == "天蓝色":
            i=5
        else :
            i=-1
        if areaCol !="" and i!=-1:
            for inp in input_list:
                if inp['area']== color_list[i]:
                    input_color_list.append(inp)
            try:
                temp_elem = text_match(input_color_list, text)
            except:
                return
            global textinsert
            textinsert = inputValue +"\n"
            if i =="":
                textBox.insert('end', textinsert)
            element = temp_elem
            xpath = element['B_xPath']
            b = driver.find_element_by_xpath(xpath)
            b.clear()
            b.send_keys(value)
            js_codeB = 'arguments[0].style.border = "2px green solid";arguments[0].style.color = "black";'
            driver.execute_script(js_codeB, b)
            xpathA = element['A_xPath']
            a = driver.find_element_by_xpath(xpathA)
            js_codeA = 'arguments[0].style.border = "2px yellow solid";'
            driver.execute_script(js_codeA, a)
            time.sleep(1)
            js_code1 = 'arguments[0].style.border = "0px white solid";'
            driver.execute_script(js_code1, a)
        else :
            try:
                temp_elem = text_match(input_list, text)
            except:
                return
            if temp_elem == "space":
                # 做出 "提示指令为空" 的反应
                # tkinter.messagebox.showinfo("提示", "指令不能为空~")
                pass
            else:
                textinsert = inputValue +"\n"
                if i =="":
                    textBox.insert('end', textinsert)
                element = temp_elem
                xpath = element['B_xPath']
                b = driver.find_element_by_xpath(xpath)
                b.clear()
                b.send_keys(value)
                js_codeB = 'arguments[0].style.border = "2px green solid";arguments[0].style.color = "black";'
                driver.execute_script(js_codeB, b)
                xpathA = element['A_xPath']
                a = driver.find_element_by_xpath(xpathA)
                js_codeA = 'arguments[0].style.border = "2px yellow solid";'
                driver.execute_script(js_codeA, a)
                time.sleep(1)
                js_code1 = 'arguments[0].style.border = "0px white solid";'
                driver.execute_script(js_code1, a)
            
    elif    "点击" in inputValue: 
            showinfoBtn(inputValue,i)


def showinfo_play():
    showinfo("")

button = tkinter.Button(win, text="确定", width=8, command=showinfo_play)
button.place(x=340,y=50)


def showinfoBtn(inputValue,i):
    btn_Color_list = []
    i = 0
    areaCol = (re.findall(r"在(.+?)区域",inputValue))[0]
    text = (re.findall(r"点击(.+)",inputValue))[0]
    if areaCol == "粉色":
        i=0
    elif areaCol == "黄色":
        i=1
    elif areaCol == "绿色":
        i=2
    elif areaCol == "蓝色":
        i=3
    elif areaCol == "紫色":
        i=4
    elif areaCol == "天蓝色":
        i=5
    else :
        i=-1
    if areaCol !="" and i!=-1:
        for inp in btn_list:
            if inp['area']== color_list[i]:
                btn_Color_list.append(inp)
        try:
            score = text_match(btn_Color_list, text)
        except:
            return
    
        if score=='space':
            tkinter.messagebox.showinfo("提示", "无匹配按钮~")
        temp_elem = score
        if temp_elem == "space":
            # 做出 "提示指令为空" 的反应
            # tkinter.messagebox.showinfo("提示", "指令不能为空~")
            pass
        else:
            element = temp_elem
            textinsert = inputValue
            if i =="":
                textBox.insert('end', textinsert )
            xpath = element['B_xPath']
            b = driver.find_element_by_xpath(xpath)
            js_code = 'arguments[0].style.border = "2px yellow solid"'
            driver.execute_script(js_code, b)
            time.sleep(1)
            js_code1 = 'arguments[0].click();arguments[0].style.border = "2px red solid";'
            driver.execute_script(js_code1, b)
    else:
        try:
            score = text_match(btn_list, text)
        except:
            return
    
        if score=='space':
            tkinter.messagebox.showinfo("提示", "无匹配按钮~")
        temp_elem = score
        if temp_elem == "space":
            # 做出 "提示指令为空" 的反应
            # tkinter.messagebox.showinfo("提示", "指令不能为空~")
            pass
        else:
            element = temp_elem
            textinsert = inputValue
            if i =="":
                textBox.insert('end', textinsert )
            xpath = element['B_xPath']
            b = driver.find_element_by_xpath(xpath)
            js_code = 'arguments[0].style.border = "2px yellow solid"'
            driver.execute_script(js_code, b)
            time.sleep(1)
            js_code1 = 'arguments[0].click();arguments[0].style.border = "2px red solid";'
            driver.execute_script(js_code1, b)

textBox = tkinter.Text(win,width=56,height=10)
textBox.place(x=10,y=100)

# text框
# 清空
def buttonClear():
    textBox.delete("1.0","end")

buttonClear = tkinter.Button(win, text="清空", width=8, command=buttonClear)
buttonClear.place(x=10,y=240)

# 读取
def buttonRead():
    f = open("D:/data/test.txt")
    lines=f.readlines()
    for i in lines :
        textBox.insert('end', i)

buttonRead = tkinter.Button(win, text="读取", width=8, command=buttonRead)
buttonRead.place(x=115,y=240)

# 保存
def buttonSave():
    result=textBox.get("1.0","end")
    f = open("D:/data/test.txt", "w")
    s = str(result)
    f.write(s)
    f.close()

saveButton = tkinter.Button(win, text="保存", width=8, command=buttonSave)
saveButton.place(x=215,y=240)



def parseCmd():
    buttonSave()
    f = open("D:/data/test.txt")
    lines=f.readlines()
    for i in lines:
        showinfo(i)
parseCmd = tkinter.Button(win, text="执行", width=8, command=parseCmd)
parseCmd.place(x=315,y=240)
# parseCmd.grid(row=6, column=3,padx=5)
try:
    win.mainloop()
except:
    pass
