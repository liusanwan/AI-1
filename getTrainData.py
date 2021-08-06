# encoding:utf-8

from selenium import webdriver
from time import sleep
import json
import os
from lxml import etree
from getArea import getArea
import datetime

# url = "http://www.jbyunshang.com/shop/passport/signup.html"
url = "http://www.beidaihe.com.cn/demolregist"
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()


pageSource = driver.page_source
tree = etree.HTML(pageSource)
xpath_dict_label = {}
xpath_dict_input = {}
xpath_dict_button = {}
label_list = []
input_list = []
xpath_list = []
btn_list = []

elements = []
for element in tree.iter():
    xpath = element.getroottree().getpath(element)

    if 'body' not in xpath or 'script' in xpath or 'comment' in xpath:
        continue
    if '/input' in xpath or '/button' in xpath or '/a' in xpath:
        if '/a' in xpath:
            if element.text == None or element.text.strip() == '':
                continue
        elem = driver.find_element_by_xpath(xpath)
        if elem.rect['height'] == 0:
            continue
        if not elem.is_enabled():
            continue
        if '/input' in xpath:
            if elem.get_attribute('type') in ['submit', 'button']:
                value = elem.get_attribute('value')
                xpath_dict_button[xpath] = {
                    'value': value, 'elem': elem, 'type': 'button'}
            else:
                id = elem.get_attribute('id')
                classI = elem.get_attribute('class')
                placeholder = elem.get_attribute('placeholder')
                xpath_dict_input[xpath] = {
                    'value': id, 'class': classI, 'elem': elem, 'type': "text", 'placeholder':placeholder}
        else:
            if '/a' in xpath:
                Type = 'link'
            if '/button' in xpath:
                Type = 'button'
            xpath_dict_button[xpath] = {
                'value': element.text, 'elem': elem, 'type': Type}
    else:

        if element.tail != None and element.tail.strip() != '':
            parentXpath = element.getparent().getroottree().getpath(element.getparent())
            elem = driver.find_element_by_xpath(xpath)
            elements.append(elem)
            xpath_dict_label[parentXpath] = {
                'value': element.tail, 'elem': elem, 'type': 'label'}
            xpath_list.append(parentXpath)
        if '/option' in xpath:
            continue

        if element.text == None or element.text.strip() == '' or len(element.text) == 1:
            continue
        elem = driver.find_element_by_xpath(xpath)
        if elem.rect['height'] == 0:
            continue
        if elem.text == None or elem.text.strip() == '':
            continue
        elements.append(elem)
        xpath_dict_label[xpath] = {
            'value': element.text, 'elem': elem, 'type': 'label'}
    xpath_list.append(xpath)


####补充坐标####
for xdl in xpath_dict_label:
    x = xpath_dict_label[xdl]['elem'].location.get('x')
    y = xpath_dict_label[xdl]['elem'].location.get('y')
    width = xpath_dict_label[xdl]['elem'].size.get('width')
    height = xpath_dict_label[xdl]['elem'].size.get('height')
    x_left_up = x
    y_left_up = y
    x_right_down = x + width
    y_right_down = y + height
    xpath_dict_label[xdl]['position'] = {"left_up": (
        x_left_up, y_left_up), "right_down": (x_right_down, y_right_down)}
    text = xpath_dict_label[xdl]['value']
    xpath_dict_label[xdl]['xpath'] = xdl
    if text == "* ":
        continue
    if (x_left_up == 0 and x_right_down == 0) or (y_left_up == 0 and y_right_down == 0):
        continue
    data = {}
    data['position'] = xpath_dict_label[xdl]['position']
    data['xpath'] = xdl
    data['context'] = {'data': text}
    label_list.append(data)

for xdi in xpath_dict_input:
    x = xpath_dict_input[xdi]['elem'].location.get('x')
    y = xpath_dict_input[xdi]['elem'].location.get('y')
    width = xpath_dict_input[xdi]['elem'].size.get('width')
    height = xpath_dict_input[xdi]['elem'].size.get('height')
    placeholder = xpath_dict_input[xdi]['placeholder']
    x_left_up = x
    y_left_up = y
    x_right_down = x + width
    y_right_down = y + height
    xpath_dict_input[xdi]['position'] = {"left_up": (
        x_left_up, y_left_up), "right_down": (x_right_down, y_right_down)}
    text = xpath_dict_input[xdi]['value']
    classSY = xpath_dict_input[xdi]['class']
    # if ('button' in classSY or 'btn' in classSY) and text != "* ":
    #     data = {}
    #     data['A_text'] = text
    #     data['B_xPath'] = xdi
    #     btn_list.append(data)
    #     continue
    data = {}
    data['position'] = xpath_dict_input[xdi]['position']
    data['xpath'] = xdi
    data['context'] = {'data': text}
    data['B_text'] = placeholder
    input_list.append(data)

for xdb in xpath_dict_button:
    x = xpath_dict_input[xdi]['elem'].location.get('x')
    y = xpath_dict_input[xdi]['elem'].location.get('y')
    width = xpath_dict_input[xdi]['elem'].size.get('width')
    height = xpath_dict_input[xdi]['elem'].size.get('height')
    placeholder = xpath_dict_input[xdi]['placeholder']
    x_left_up = x
    y_left_up = y
    x_right_down = x + width
    y_right_down = y + height
    xpath_dict_input[xdi]['position'] = {"left_up": (
        x_left_up, y_left_up), "right_down": (x_right_down, y_right_down)}
    text = xpath_dict_input[xdi]['value']
    classSY = xpath_dict_input[xdi]['class']
    data = {}
    data['position'] = xpath_dict_input[xdi]['position']
    data['xpath'] = xdi
    data['context'] = {'data': text}
    data['B_text'] = placeholder
    input_list.append(data)

jsonInfo = {}
jsonInfo['A'] = label_list
jsonInfo['B'] = input_list
path = 'C:\\jsonData'
dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
fileName = path + '\\jsonData' + str(dt)
with open(fileName + '.txt', 'a') as file_object:
    for i in range(len(input_list)):
        for j in range(len(label_list)):
            # 生成Json
            jsonInfo = {}
            jsonInfo['A'] = label_list[j]
            jsonInfo['B'] = input_list[i]
            jsonInfo['Result'] = "0"
            objJson = json.dumps(jsonInfo, ensure_ascii=False)
            file_object.write(str(objJson.replace(u'\xa0', u'').encode('utf-8').decode('utf-8') + "\n"))    


