# coding: utf-8

from selenium import webdriver
import importlib
import os

def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options = options)
    driver.implicitly_wait(5)
    return driver

def load_parsers(folder, name = ''):
    if folder.endswith('/'):
        folder = folder[:-1]
    handlers = {}
    for f in os.listdir(folder):
        if not os.path.isfile(folder + '/' + f):
            continue
        if name and (f != (name + '.py')):
            continue
        if f.endswith('.py'):
            mod = importlib.import_module(folder + '.' + f[:-3])
            handlers[mod.prefix] = mod.parse
    return handlers
