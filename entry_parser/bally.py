# coding: utf-8

import sys

sys.path.append('.')
import util

prefix = 'www.bally.cn'

def parse(drive, url):
    products = []
    driver.execute_script('window.scrollBy(0,50000)')
    utils.sleep(3)
    elements = util.find_elements_by_css_selector(driver, 'js-producttile_link')
    for element in elements:
        products.append(element.get_attribute('href')
    return ';'.join(products)
