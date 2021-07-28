# encoding:utf-8

from selenium import webdriver
from time import sleep
import json
import os
from lxml import etree
import datetime
import time

def getAllElements(driver):
    pageSource = driver.page_source
    tree = etree.HTML(pageSource)
    xpath_dict_label = {}
    xpath_dict_input = {}
    xpath_dict_button = {}
    label_list = []
    input_list = []
    btn_list = []
    xpath_list = []

    elements = []
    for element in tree.iter():
        xpath = element.getroottree().getpath(element)
        xpath_list.append(xpath)
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
                if elem.get_attribute('type') in ['submit','button']:
                    value = elem.get_attribute('value')
                    xpath_dict_button[xpath] = {'value': value, 'elem': elem,'type':'button'}
                else:
                    id = elem.get_attribute('id')
                    classI = elem.get_attribute('class')
                    xpath_dict_input[xpath] = {'value': id,'class':classI,'elem': elem,'type': "text"}
            else:
                if '/a' in xpath:
                    Type = 'link'
                if '/button' in xpath:
                    Type = 'button'
                xpath_dict_button[xpath] = {'value':element.text,'elem': elem,'type': Type}
        else:
            if '/option' in xpath:
                continue
            if element.text == None or element.text.strip() == '':
                continue
            elem = driver.find_element_by_xpath(xpath)
            if elem.rect['height'] == 0:
                continue
            if elem.text == None or elem.text.strip() == '':
                continue
            elements.append(elem)
            xpath_dict_label[xpath] = {'value':element.text,'elem':elem,'type':'label'}



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
        xpath_dict_label[xdl]['position'] = {"left_up":(x_left_up,y_left_up),"right_down":(x_right_down,y_right_down)}
        text = xpath_dict_label[xdl]['value']
        xpath_dict_label[xdl]['xpath'] = xdl
        if text =="* ":
            continue
        data = {}
        data['position'] = xpath_dict_label[xdl]['position']
        data['xpath'] = xdl
        data['context'] = {'data':text}
        label_list.append(data)
        

    for xdi in xpath_dict_input:
        x = xpath_dict_input[xdi]['elem'].location.get('x')
        y = xpath_dict_input[xdi]['elem'].location.get('y')
        width = xpath_dict_input[xdi]['elem'].size.get('width')
        height = xpath_dict_input[xdi]['elem'].size.get('height')
        x_left_up = x
        y_left_up = y
        x_right_down = x + width
        y_right_down = y + height
        xpath_dict_input[xdi]['position']={"left_up":(x_left_up,y_left_up),"right_down":(x_right_down,y_right_down)}
        text = xpath_dict_input[xdi]['value']
        classSY = xpath_dict_input[xdi]['class']
        if ('button' in classSY or 'btn' in classSY) and text !="* " :
            data = {}
            data['A_text'] = text
            data['B_xPath'] = xdi
            btn_list.append(data)
            continue
        data = {}
        data['position'] = xpath_dict_input[xdi]['position']
        data['xpath'] = xdi
        data['context'] = {'data':text}
        input_list.append(data)

    for xdb in xpath_dict_button:
        text = xpath_dict_button[xdb]['value']
        data = {}
        data['A_text'] = text
        data['B_xPath'] = xdb
        btn_list.append(data)

    jsonInfo = {}
    jsonInfo['A'] = label_list
    jsonInfo['B'] = input_list
    jsonInfo['C'] = btn_list
    return jsonInfo
