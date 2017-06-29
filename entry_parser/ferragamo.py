# coding: utf-8

import sys

sys.path.append('../')
import util

prefixes = ['www.ferragamo.cn']
def parse(driver, url):
    products = []
    driver.get(url)
    for i in range(10): # 确保页面拉到最下面，所有商品得到展示。
        driver.execute_script('window.scrollBy(0, 10000)')
        util.sleep(1)
    elements = util.find_elements_by_css_selector(driver, 'li.item > div> div.product-image-box >a')
    for element in elements:
        products.append(element.get_attribute('href').strip())
    return ';'.join(products)

if __name__ == '__main__':
    driver = util.create_chrome_driver()
    print(parse(driver, sys.argv[1]))
    driver.quit()
