# coding: utf-8

import sys

sys.path.append('../')
import util

prefixes = ['www.bally.cn']

def parse(driver, url):
    products = []
    driver.get(url)
    driver.execute_script('window.scrollBy(0,50000)')
    util.sleep(3)
    elements = util.find_elements_by_css_selector(driver, 'a.js-producttile_link')
    for element in elements:
        products.append(element.get_attribute('href').strip())
    return ';'.join(products)

if __name__ == '__main__':
    driver = util.create_chrome_driver()
    print(parse(driver, sys.argv[1]))
    driver.quit()
