# coding: utf-8

import sys

sys.path.append('../')
import util

prefixes = ['www.gucci.com'] # 打开浏览器后会自动跳转到.cn

def parse(driver, url):
    products = []
    driver.get(url)
    elements = util.find_elements_by_css_selector(driver, 'div > a.spice-item-grid')
    for element in elements:
        products.append(element.get_attribute('href').strip())
    return ';'.join(products)

if __name__ == '__main__':
    driver = util.create_chrome_driver()
    print(parse(driver, sys.argv[1]))
    driver.quit()
