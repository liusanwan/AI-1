import tkinter
import tkinter.messagebox
# from selenium.webdriver.common.by import By
from main import loadChrome
import re
from text_match import text_match
from selenium import webdriver
import time


url = "http://wlwz.changsha.gov.cn/webapp/cs/register/register_2.htm"
# url = "http://172.27.234.198/zentao/user-login-L3plbnRhby8=.html"     #禅道登入页面
# url = "http://www.gdkjxh.com/member/reg"          #text页面
# url = "https://www.hnsrmyy.net/Register.html"  # 河南人民医院注册网页

color_list_disc = {'红色':"rgb(224 22 22 / 39%)",'灰色':"rgb(229 229 243 / 45%)",'粉色':"rgb(226 110 236 / 33%)"
    ,'绿色':"rgb(162 243 83 / 33%)",'橙色':"rgb(255 231 3 / 50%)",'橘色':"rgb(255 137 3 / 50%)",'黄色':"rgb(245 255 3 / 53%)"
    ,'蓝色':"rgb(15 224 191 / 53%)",'紫色':"rgb(157 70 228 / 26%)",'深灰色':"rgb(8 8 8 / 26%)"}
# yang
# driver = webdriver.Chrome(
#     executable_path=r"G:\anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
input_list,btn_list  = loadChrome(driver)

def reloadChrome():
    url= entry_url.get()
    driver.get(url)
    driver.maximize_window()
    global input_list
    global btn_list
    input_list,btn_list  = loadChrome(driver)
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
reloadChrome = tkinter.Button(win, text="切换", width=8,height=1, command=reloadChrome)
reloadChrome.place(x=340,y=10)

labelCmd = tkinter.Label(win, text="Cmd", fg="black",
                      font=("黑体", 10), anchor="ne")
labelCmd.place(x=10,y=50)
e = tkinter.Variable()
entry1 = tkinter.Entry(win, width=39)
entry1.place(x=50,y=50)
jsonInfo = {}
textinsert = ''

# input的样式和值得修改
def input_style(i,value,temp_elem,inputValue):
    if temp_elem == "space":
                # 做出 "提示指令为空" 的反应
                # tkinter.messagebox.showinfo("提示", "指令不能为空~")
                pass
    else:
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

# button的样式和值得修改
def button_style(i,temp_elem,inputValue):
    if temp_elem == "space":
            # 做出 "提示指令为空" 的反应
            # tkinter.messagebox.showinfo("提示", "指令不能为空~")
            pass
    else:
        element = temp_elem
        textinsert = inputValue+"\n"
        if i =="":
            textBox.insert('end', textinsert )
        xpath = element['B_xPath']
        b = driver.find_element_by_xpath(xpath)
        js_code = 'arguments[0].style.border = "2px yellow solid"'
        driver.execute_script(js_code, b)
        time.sleep(1)
        js_code1 = 'arguments[0].click();arguments[0].style.border = "2px red solid";'
        driver.execute_script(js_code1, b)

# 确定按钮执行动作
def showinfo(i):
    if i =="":
        inputValue = entry1.get()
    else:
        inputValue = i
    if "输入" in inputValue:
        input_color_list = []
        if "区域" in inputValue:
            areaCol = (re.findall(r"在(.+?)区域",inputValue))[0]
            text = (re.findall(r"的(.+?)输入",inputValue))[0]
        else :
            areaCol=""
            text = (re.findall(r"在(.+?)输入",inputValue))[0]
        value = (re.findall(r"输入(.+)",inputValue))[0]
        if areaCol !="" :
            for inp in input_list:
                if inp['area']== color_list_disc[areaCol]:
                    input_color_list.append(inp)
            try:
                temp_elem = text_match(input_color_list, text)
            except:
                return
            input_style(i,value,temp_elem,inputValue)
        else :
            try:
                temp_elem = text_match(input_list, text)
            except:
                return
            input_style(i,value,temp_elem,inputValue)
            
    elif    "点击" in inputValue: 
            showinfoBtn(inputValue,i)

# 确定按钮执行动作
def showinfo_play():
    showinfo("")
button = tkinter.Button(win, text="确定", width=8, command=showinfo_play)
button.place(x=340,y=50)

def showinfoBtn(inputValue,i):
    btn_Color_list = []
    i = 0
    if "区域" in inputValue:
            areaCol = (re.findall(r"在(.+?)区域",inputValue))[0]
    else :
            areaCol=""
    text = (re.findall(r"点击(.+)",inputValue))[0]
    if areaCol !="":
        for inp in btn_list:
            if inp['area']== color_list_disc[areaCol]:
                btn_Color_list.append(inp)
        try:
            score = text_match(btn_Color_list, text)
        except:
            return
        if score=='space':
            tkinter.messagebox.showinfo("提示", "无匹配按钮~")
        temp_elem = score
        button_style(i,temp_elem,inputValue)
    else:
        try:
            score = text_match(btn_list, text)
        except:
            return
        if score=='space':
            tkinter.messagebox.showinfo("提示", "无匹配按钮~")
        temp_elem = score
        button_style(i,temp_elem,inputValue)

textBox = tkinter.Text(win,width=56,height=10)
textBox.place(x=10,y=100)

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

# 执行
def parseCmd():
    buttonSave()
    f = open("D:/data/test.txt")
    lines=f.readlines()
    for i in lines:
        showinfo(i)
parseCmd = tkinter.Button(win, text="执行", width=8, command=parseCmd)
parseCmd.place(x=315,y=240)
try:
    win.mainloop()
except:
    pass