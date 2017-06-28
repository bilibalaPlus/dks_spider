# coding: utf-8

import sys
sys.path.append('../')
import util

prefixes = ['www.dior.cn']

def parse(driver, url):
    products = []
    driver.get(url)
    elements = util.find_elements_by_css_selector(driver, 'div.product > div > div > a')
    if not elements: # http://www.dior.cn/beauty/zh_cn/%E9%A6%99%E6%B0%9B%E4%B8%8E%E7%BE%8E%E5%AE%B9/%E5%BD%A9%E5%A6%86/%E7%9C%BC%E9%83%A8/%E7%9C%BC%E5%BD%B1/fr-eyeshadows-%E7%9C%BC%E5%BD%B1.html
        elements = util.find_elements_by_css_selector(driver, 'div.column > div.push-pic > a')
    for element in elements:
        products.append(element.get_attribute('href').strip())
    return ';'.join(products)

if __name__ == '__main__':
    driver = util.create_chrome_driver()
    print(parse(driver, sys.argv[1]))
    driver.quit()
