# coding: utf-8

import sys

sys.path.append('../')
import util

prefixes = ['www.louisvuitton.cn']
def parse(driver, url):
    products = []
    driver.get(url)
    elements = util.find_elements_by_css_selector(driver, 'a.product-item')
    if not elements: # http://www.louisvuitton.cn/zhs-cn/women/ready-to-wear/furs/_/N-f8lvb3
        elements = util.find_elements_by_css_selector(driver, 'li.listing > a.product-img')
    for element in elements:
        products.append(element.get_attribute('href').strip())
    return ';'.join(products)

if __name__ == '__main__':
    driver = util.create_chrome_driver()
    print(parse(driver, sys.argv[1]))
    driver.quit()
