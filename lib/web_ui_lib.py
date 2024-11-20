#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from lib.varpool_lib import varpool
from lib.logger_lib import create_logger, create_rotating_file_handler, logger_add_handler

# about driver
from selenium import webdriver
from webdriver_helper import get_webdriver

# driver options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# driver service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.ie.service import Service as IEService

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

# mouse and keyboard
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


# browser operations ------------------------------------------------------------------------------------------
def open_url(url: str, browser_type="chrome", driver_type="smart",webhub_url="", driver_path=""):
    if driver_type not in ["smart", "local", "remote"]:
        raise ValueError(f"Unsupported driver type: {driver_type}")
    if browser_type not in ["chrome", "firefox", "edge", "ie"]:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    if driver_type == "smart":
        driver = __open_online_browser(browser_type)
    elif driver_type == "local":
        driver = __open_local_browser(browser_type, driver_path)
    elif driver_type == "remote":
        driver = __open_remote_browser(webhub_url, browser_type)
    else:
        raise ValueError(f"Unsupported driver type: {driver_type}")
    driver.get(url)
    return driver

def close_browser(driver):
    driver.quit()

def get_current_url(driver):
    return driver.current_url

def get_title(driver):
    return driver.title

def get_page_source(driver):
    return driver.page_source



def __open_local_browser(browser_type, driver_path):
    """
    打开指定类型的浏览器并设置选项
    :param browser_type: 浏览器类型，支持 'chrome', 'firefox', 'edge', 'ie'
    :param driver_path: 浏览器驱动文件路径
    """
    if browser_type.lower() == 'chrome':
        options = ChromeOptions()
        options.add_argument('--ignore-certificate-errors')  # 忽略不安全的SSL
        options.add_argument('--start-maximized')  # 最大化窗口
        service = ChromeService(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_type.lower() == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        service = FirefoxService(driver_path)
        driver = webdriver.Firefox(service=service, options=options)
    elif browser_type.lower() == 'edge':
        options = EdgeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        service = EdgeService(driver_path)
        driver = webdriver.Edge(service=service, options=options)
    elif browser_type.lower() == 'ie':
        options = IeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        service = IEService(driver_path)
        driver = webdriver.Ie(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    return driver


def __open_online_browser(browser_type="chrome"):
    if browser_type.lower() == 'chrome':
        options = ChromeOptions()
        options.add_argument('--ignore-certificate-errors')  # 忽略不安全的SSL
        options.add_argument('--start-maximized')  # 最大化窗口
        driver = get_webdriver(browser_type, options=options)
    elif browser_type.lower() == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        driver = get_webdriver(browser_type, options=options)
    elif browser_type.lower() == 'edge':
        options = EdgeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        driver = get_webdriver(browser_type, options=options)
    elif browser_type.lower() == 'ie':
        options = IeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        driver = get_webdriver(browser_type, options=options)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    return driver


def __open_remote_browser(webhub_url: str, browser_type="chrome"):
    # check browser type
    # set capabilities
    capabilities = None
    if browser_type == "chrome":
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities["browserName"] = "chrome"
        capabilities["version"] = ""
        capabilities["platform"] = "ANY"
        capabilities["javascriptEnabled"] = True
        capabilities["acceptInsecureCerts"] = True
    elif browser_type == "firefox":
        capabilities = {
            "browserName": "firefox",
            "version": "",
            "platform": "ANY",
            "javascriptEnabled": True,
            "acceptInsecureCerts": True
        }
    elif browser_type == "edge":
        capabilities = {
            "browserName": "edge",
            "version": "",
            "platform": "ANY",
            "javascriptEnabled": True
        }
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    # set headless mode
    driver = webdriver.Remote(command_executor=webhub_url, desired_capabilities=capabilities)
    return driver


# element operations ------------------------------------------------------------------------------------------
def locate_element(driver, locator_type: str, locator_value: str, timeout=10):
    if locator_type == "id":
        return WebDriverWait(driver, timeout,0.5).until(EC.presence_of_element_located((By.ID, locator_value)))
    elif locator_type == "name":
        return WebDriverWait(driver, timeout,0.5).until(EC.presence_of_element_located((By.NAME, locator_value)))
    elif locator_type == "xpath":
        return WebDriverWait(driver, timeout,0.5).until(EC.presence_of_element_located((By.XPATH, locator_value)))
    elif locator_type == "link_text":
        return WebDriverWait(driver, timeout,0.5).until(EC.presence_of_element_located((By.LINK_TEXT, locator_value)))
    elif locator_type == "partial_link_text":
        return WebDriverWait(driver, timeout,0.5).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, locator_value)))
    elif locator_type == "tag_name":
        return WebDriverWait(driver, timeout,0.5).until(EC.presence_of_element_located((By.TAG_NAME, locator_value)))
    elif locator_type == "class_name":
        return WebDriverWait(driver, timeout,0.5).until(EC.presence_of_element_located((By.CLASS_NAME, locator_value)))
    elif locator_type == "css_selector":
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, locator_value)))
    else:
        raise ValueError("Unsupported locator type: {}".format(locator_type))


def click_element(element):
    element.click()


def input_text(element, text: str):
    element.clear()
    element.send_keys(text)

# mouse and keyboard operations -------------------------------------------------------------------------------
