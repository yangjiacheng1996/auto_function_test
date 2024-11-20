#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import time
import platform

from lib.varpool_lib import varpool
from lib import web_api_lib
from lib import web_ui_lib
from lib import cmd_lib


def add(**kwargs):
    a = int(kwargs["a"])
    b = int(kwargs["b"])
    logging.info("%d + %d = %d" % (a, b, a + b))
    return a + b


def douban(**kwargs):
    url = kwargs["url"]
    headers = kwargs.get("headers", {})
    response = web_api_lib.get_api_data(url, headers)
    logging.info(response)
    return response

def search_baidu(**kwargs):
    url = kwargs["url"]
    baidu_search_box = kwargs["baidu_search_box"]
    baidu_search_button = kwargs["baidu_search_button"]
    search_text = kwargs["text"]
    driver = web_ui_lib.open_url(url)
    time.sleep(2)
    element_baidu_search_box = web_ui_lib.locate_element(driver, baidu_search_box[0],baidu_search_box[1])
    web_ui_lib.input_text(element_baidu_search_box, search_text)
    element_baidu_search_button = web_ui_lib.locate_element(driver, baidu_search_button[0],baidu_search_button[1])
    web_ui_lib.click_element(element_baidu_search_button)
    time.sleep(5)
    return True

def run_cmd(**kwargs):
    cmd = kwargs["cmd"]
    system = platform.system()
    if system == 'Windows' and cmd == "ipconfig":
        return cmd_lib.command(cmd)
    elif system == 'Linux' and cmd == "ip a":
        return cmd_lib.command(cmd)
    elif system == 'Darwin' and cmd == "ifconfig":  # macOS
        return cmd_lib.command(cmd)
    else:
        return True



