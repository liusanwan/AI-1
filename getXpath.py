# encoding:utf-8

from selenium import webdriver
from time import sleep
import json
import execjs
from lxml import etree


def getXpath():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(r"D:\Selenium WebDriver\Chrome\chromedriver_win32\chromedriver.exe",
                              chrome_options=option)
    driver.get("https://www.sf-express.com/cn/sc/dynamic_function/more/payment/")
    driver.maximize_window()
    sleep(1)

    res = driver.execute_script('return document.title')
    print(res)

    element = driver.find_element_by_xpath('//*[@id="carryId"]')
    id = element.get_property('id')
    domObj = "document.getElementById('{}')".format(id)

    js = """
    function getPathTo(element) {
        var ix= 0;
        return element.parentNode
        var siblings= element.parentNode.childNodes;
        for (var i= 0; i<siblings.length; i++) {
            var sibling= siblings[i];
            if (sibling===element)
                return getPathTo(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
            if (sibling.nodeType===1 && sibling.tagName===element.tagName)
                ix++;
        }
    }
    """

    # js1 = "var s = '';" + "var o = getComputedStyle(arguments[0]);" + "for(var i = 0; i < o.length; i++){" + "s+=o[i] + ':' + o.getPropertyValue(o[i])+';';}" + "return s;"
    # res = driver.execute_script(js1, element)
    # js = "var q=document.getElementById(\"carryId\").parentNode;"
    # res = driver.execute_script('document.title')
    # print(res)

    CTX = execjs.compile(js)
    print(CTX.call('getPathTo', domObj))

    driver.close()


def getParents():
    print("get parents")

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(r"D:\Selenium WebDriver\Chrome\chromedriver_win32\chromedriver.exe",
                              chrome_options=option)
    # driver = webdriver.Chrome(r"D:\Selenium WebDriver\Chrome\chromedriver_win32\chromedriver.exe")
    driver.get("http://172.27.234.198/zentao/user-login-L3plbnRhby8=.html")

    element = driver.find_element_by_xpath(
        '//input[@id="account"]/../../..').tag_name
    print(element)

    id = "account"
    js_blog = 'return document.getElementById("%s").tagName;' % id
    print(js_blog)
    blog = driver.execute_script(js_blog)
    print(blog)


def uselxml():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(r"D:\Selenium WebDriver\Chrome\chromedriver_win32\chromedriver.exe",
                              chrome_options=option)
    driver.get("https://www.sf-express.com/cn/sc/dynamic_function/more/payment/")
    sleep(1)

    pageSouce = driver.page_source

    tree = etree.HTML(pageSouce)
    # print(etree.tostring(tree))

    # root = etree.fromstring(etree.tostring(tree))
    for element in tree.iter():
        txt = element.getroottree().getpath(element)
        print(txt)
        if str(txt).find('comment') < 0:
            # print(xpath)
            a = driver.find_element_by_xpath(txt).text
            # print(a)
            if a == '运单号*':
                print(txt)
                print(a)
                break
