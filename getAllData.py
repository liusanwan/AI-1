# encoding:utf-8

from selenium import webdriver
from time import sleep
import json
import os
from lxml import etree
import datetime
id_A = 0
id_B = 0


def getAllElements(url):
    print('start script')
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(
        executable_path=r"G:\anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
    # driver = webdriver.Chrome(r"D:\Selenium WebDriver\Chrome\chromedriver_win32\chromedriver.exe")
    driver.get(url)
    driver.maximize_window()
    sleep(1)
    label_list = []
    input_list = []
    btn_list = []
    link_list = []
    xpath_list = []
    # file_list = []

    # 获取页面所有Xpath
    pageSouce = driver.page_source
    tree = etree.HTML(pageSouce)

    # print(etree.tostring(tree))

    # print("====="+driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[1]/div/div/div/div/div[1]/form/div[1]/div/input').get_property('name'))
    # print("=====" + driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[1]/div/h2').text)

    # print("=====2" + driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/form/div[1]/div/input').get_property('name'))
    # print("=====2" + driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div/h2').text)

    # 遍历Xpath路径
    for element in tree.iter():
        xpath = element.getroottree().getpath(element)
        # print(xpath)
        if str(xpath).find('comment') < 0:
            if str(xpath).find('h2') >= 0:
                xpath_list.append(str(xpath))
            if str(xpath).find('th') >= 0:
                xpath_list.append(str(xpath))
            if str(xpath).find('label') >= 0:
                xpath_list.append(str(xpath))
            if str(xpath).find('input') >= 0:
                xpath_list.append(str(xpath))
            if str(xpath).find('span') >= 0:
                xpath_list.append(str(xpath))
            # if str(xpath).find('div') >= 0:
            #     xpath_list.append(str(xpath))

    # 查找所有label控件
    getLabel('//h2', xpath_list, label_list, driver)
    getLabel('//th', xpath_list, label_list, driver)
    getLabel('//label', xpath_list, label_list, driver)
    getLabel('//span', xpath_list, label_list, driver)
    # getLabel('//div', xpath_list, label_list, driver)

    # 查找所有Input控件
    getInput('//input', xpath_list, input_list, driver, btn_list, link_list)

    jsonInfo = {}
    jsonInfo['A'] = label_list
    jsonInfo['B'] = input_list
    jsonInfo['C'] = btn_list
    return jsonInfo

# 获取label数据


def getLabel(tagName, xpath_list, label_list, driver):
    h2Elements = driver.find_elements_by_xpath(tagName)

    for element in h2Elements:
        text = element.text
        if (text is not None and len(text) > 0):
            # 左上角X,Y坐标
            xlocation = element.location.get('x')
            ylocation = element.location.get('y')
            xwidth = element.size.get('width')
            yheight = element.size.get('height')

            # 控件的长宽
            # 左上
            xleftUp = xlocation
            yleftUp = ylocation
            # 右下
            xrightDown = xlocation + xwidth
            yrightDown = ylocation + yheight

            objClass = element.get_attribute("class")
            # objProperty = "Class:" + str(objClass) + " Text:" + str(text)
            objProperty = str(text)
            # 获取Xpath
            xpath = ''
            for i in xpath_list:
                a = driver.find_element_by_xpath(i).text
                if a == text:
                    xpath = i
                    break

            # 生成Json
            jsonInfo = {}
            data = json.loads(json.dumps(jsonInfo))
            global id_A
            id_A += 1
            data['id_A'] = str(id_A)
            position = {'left_up': (xleftUp, yleftUp),
                        'right_down': (xrightDown, yrightDown)}
            data['position'] = position

            # ancestor = {'xpath': 'xxxx'}
            # print(xpath)
            data['xpath'] = xpath

            context = {'data': objProperty}
            data['context'] = context

            #objJson = json.dumps(data, ensure_ascii=False)
            # print(objJson)
            label_list.append(data)

# 获取Input数据


def getInput(tagName, xpath_list, input_list, driver, btn_list, link_list):

    inputElements = driver.find_elements_by_xpath('//input')

    for element in inputElements:
        name = element.get_property("name")
        type = element.get_property("type")
        # 获取所有的入力框的input
        if (len(name) > 0 and (type == 'text' or type == 'password')):
            # 左上角X,Y坐标
            xlocation = element.location.get('x')
            ylocation = element.location.get('y')
            xwidth = element.size.get('width')
            yheight = element.size.get('height')

            # 控件的长宽
            xleftUp = xlocation
            yleftUp = ylocation
            xrightDown = xlocation + xwidth
            yrightDown = ylocation + yheight
            objName = element.get_property("name")
            objType = element.get_property("type")
            objId = element.get_property("id")
            objClass = element.get_attribute("class")
            objPlaceholder = element.get_attribute("placeholder")

            objProperty = str(objPlaceholder)
            realId = str(objId)

            if xwidth == 0 or yheight == 0:
                break
            if objType == 'checkbox':
                break

            # 获取Xpath
            xpath = ''
            for i in xpath_list:
                a = driver.find_element_by_xpath(i).get_property("name")
                if a == name:
                    xpath = i
                    break

            # 生成Json
            jsonInfo = {}
            data = json.loads(json.dumps(jsonInfo))

            global id_B
            id_B += 1
            data['id_B'] = str(id_B)
            position = {'left_up': (xleftUp, yleftUp),
                        'right_down': (xrightDown, yrightDown)}
            data['position'] = position

            data['xpath'] = xpath

            context = {'data': objProperty}
            data['context'] = context
            data['realId'] = str(realId)
            input_list.append(data)
        # 获取提交等按钮的list
        elif type == 'submit':
            text = element.get_attribute("value")
            type = element.get_property("type")
            xpath = ''
            if (text is not None and len(text) > 0):
                for i in xpath_list:
                    a = driver.find_element_by_xpath(i).get_property("value")
                    if a == text:
                        xpath = i
            jsonInfo = {}
            data = json.loads(json.dumps(jsonInfo))
            data['text'] = text
            data['type'] = type
            data['btn'] = "button"
            data['xpath'] = xpath
            btn_list.append(data)
