# coding: utf-8

import sys
sys.path.append('../')
import util

prefix = 'www.balenciaga.cn'

def parse(driver, url):
    products = []
    driver.get(url)
    elements = util.find_elements_by_css_selector(driver, 'a.item-display-image-container')
    for element in elements:
        products.append(element.get_attribute('href').strip())
    return ';'.join(products)

if __name__ == '__main__':
    print(parse(util.create_chrome_driver(), sys.argv[1])
