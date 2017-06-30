# coding: utf-8

import sys
sys.path.append('../')
import util

brand = 'balenciaga'
prefixes = ['www.balenciaga.cn']

def get_title(driver):
    title = ''
    element = util.find_element_by_css_selector(driver, 'div.item-main.top-content > div > span.modelName')
    if not element:
        raise Exception('Title not found for %s' % driver.current_url)
    else:
        title = element.text.strip()
        element = util.find_element_by_css_selector(driver, 'div.EditorialDescription > span.value')
        if element:
            title += ' - ' + element.text.strip()
    
def get_code(driver):
    return ''
    
def get_price(driver):
    price = 0
    # 先找折扣价
    element = util.find_element_by_css_selector(driver, 'div.model-price > div > span.discounted.price > span.value')
    if not element: # 没有折扣就查看原价
        element = util.find_element_by_css_selector(driver, 'div.item-main > div > span.price > span.value')
    if element:
        text = element.text.strip()
        price = float(text.replace(',', '')) if text else 0
    return price
    
def get_intro(driver):
    pass
    
def get_images(driver):
    pass

def parse(driver, url):
    driver.get(url)
    good = {'brand':brand'}
    good['title'] = get_title(driver)
    good['code'] = get_code(driver)
    good['price'] = get_price(driver)
    good['intro'] = get_intro(driver)
    good['images'] = get_images(driver)

if __name__ == '__main__':
    driver = util.create_chrome_driver()
    print(parse(driver, sys.argv[1]))
    driver.quit()
