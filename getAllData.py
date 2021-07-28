# encoding:utf-8

from selenium import webdriver
from time import sleep
import json
import os
from lxml import etree
import datetime
import time
id_A = 0
id_B = 0

def getAllElements(driver):
    print('start script')
    option = webdriver.ChromeOptions()
    #option.add_argument('headless')
    sleep(1)
    label_list = []
    input_list = []
    btn_list = []
    link_list = []
    xpath_disc = {}
    # file_list = []

    # 获取页面所有Xpath
    pageSouce = driver.page_source
    tree = etree.HTML(pageSouce)
    # 遍历Xpath路径
    for element in tree.iter():
        xpath = element.getroottree().getpath(element)
        if str(xpath).find('comment') < 0:
            if str(xpath).find('h2') >= 0:
                xpath_disc[str(xpath)] = str(xpath)
            if str(xpath).find('th') >= 0:
                xpath_disc[str(xpath)] = str(xpath)
            if str(xpath).find('label') >= 0:
                xpath_disc[str(xpath)] = str(xpath)
            if str(xpath).find('input') >= 0:
                xpath_disc[str(xpath)] = str(xpath)
            if str(xpath).find('span') >= 0:
                xpath_disc[str(xpath)] = str(xpath)
            if str(xpath).find('li') >= 0:
                xpath_disc[str(xpath)] = str(xpath)
            if str(xpath).find('td') >= 0:
                xpath_disc[str(xpath)] = str(xpath)
            # if str(xpath).find('div') >= 0:
            #     xpath_disc[str(xpath)] = str(xpath)
    timestart = time.time()
    # 查找所有label控件
    getLabel('//h2', xpath_disc, label_list, driver)
    getLabel('//th', xpath_disc, label_list, driver)
    getLabel('//label', xpath_disc, label_list, driver)
    getLabel('//span', xpath_disc, label_list, driver)
    getLabel('//li', xpath_disc, label_list, driver)
    getLabel('//td', xpath_disc, label_list, driver)
    # getLabel('//div', xpath_disc, label_list, driver)
    time2 =time.time()
    print(str(time2-timestart))
    # 查找所有Input控件
    getInput('//input', xpath_disc, input_list, driver, btn_list, link_list)
    time3 =time.time()
    print(str(time3-time2))

    jsonInfo = {}
    jsonInfo['A'] = label_list
    jsonInfo['B'] = input_list
    jsonInfo['C'] = btn_list
    return jsonInfo

# 获取label数据

def getLabel(tagName, xpath_disc, label_list, driver):
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
            objProperty = str(text)
            # if "已有账号" in objProperty:
            #     continue
            # 获取Xpath
            xpath = ''
            for i in xpath_disc.keys():
                a = driver.find_element_by_xpath(i).text
                if a == text:
                    xpath = i
                    # if tagName == "//li":
                    #     b = driver.find_element_by_xpath(xpath)
                    #     print(b)
                    #     js_code='''
                    #         var parent = arguments[0];
                    #         var child = parent.firstChild;
                    #         var ret = "";
                    #         while(child) {
                    #             if (child.nodeType === Node.TEXT_NODE)
                    #                 ret += child.textContent;
                    #             child = child.nextSibling;
                    #         }
                    #         return ret;
                    #         '''
                    #     #wd为Webdirver
                    #     output = driver.execute_script(js_code, b)
                    #     print(output)
                    break

            # 生成Json
            jsonInfo = {}
            data = json.loads(json.dumps(jsonInfo))

            position = {'left_up': (xleftUp, yleftUp),
                        'right_down': (xrightDown, yrightDown)}
            data['position'] = position
            data['xpath'] = xpath

            context = {'data': objProperty}
            data['context'] = context
            label_list.append(data)

# 获取Input数据


def getInput(tagName, xpath_disc, input_list, driver, btn_list, link_list):

    inputElements = driver.find_elements_by_xpath('//input')
    inputElementsBtn = driver.find_elements_by_xpath('//button')

    for element in inputElements:
        name = element.get_property("name")
        type = element.get_property("type")
        # 获取所有的入力框的input
        if (len(name) > 0 and (type == 'text' or type == 'password' or type == 'email')):
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
            for i in xpath_disc.keys():
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
            # yang
            # data['A_text'] = "姓名"
            data['type'] = type
            data['realId'] = str(realId)
            input_list.append(data)
        # 获取提交等按钮的list
        elif type == 'submit':
            text = element.get_attribute("value")
            type = element.get_property("type")
            xpath = ''
            if (text is not None and len(text) > 0):
                for i in xpath_disc.keys():
                    a = driver.find_element_by_xpath(i).get_property("value")
                    if a == text:
                        xpath = i
            jsonInfo = {}
            data = json.loads(json.dumps(jsonInfo))
            data['A_text'] = text
            data['type'] = type
            data['btn'] = "button"
            data['B_xPath'] = xpath
            if xpath == '':
                continue
            btn_list.append(data)

    for element in inputElementsBtn:
        name = element.get_property("name")
        type = element.get_property("type")
        # 获取提交等按钮的list
        if type == 'submit':
            objId = element.get_property("id")
            type = element.get_property("type")
            xpath = ''
            if (objId =='submit'):
                for i in xpath_disc.keys():
                    a = driver.find_element_by_xpath(i).get_property("id")
                    if a == objId:
                        xpath = i
                        text = driver.find_element_by_xpath(i).text
            jsonInfo = {}
            data = json.loads(json.dumps(jsonInfo))
            data['A_text'] = text
            data['type'] = type
            data['btn'] = "button"
            data['B_xPath'] = xpath
            if xpath == '':
                continue
            btn_list.append(data)
