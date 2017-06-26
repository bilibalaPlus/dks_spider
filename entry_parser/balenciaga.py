# coding: utf-8

import sys
sys.path.append('../')
import util

prefix = 'www.balenciaga.cn'

def parse(driver, url):
    products = []
    driver.get(url)
    elements = util.find_elements_by_css_selector(driver, 'item-display-image-container')
    for element in elements:
        products.append(element.get_attribute('href'))
    return ';'.join(products)
