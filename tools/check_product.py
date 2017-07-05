# coding: utf-8

# 检查获取数据，判断有哪些该拿的信息没有拿到。

import argparse
import sys

sys.path.append('../')
import dks_database as dd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b',
                        '--brand',
                        help = 'Specify the brand you want to check')
    return parser.parse_args()

def write_to_file(file, lines):
    with open(file, 'w+') as f:
        for line in lines:
            if line:
                f.write(line + '\n')

if __name__ == '__main__':
    args = parse_args()
    brand = args.brand
    empty_code = []
    empty_price = []
    empty_intro = []
    empty_images = []
    jq = dd.Source.select(dd.Source.id, dd.Source.url)
    if brand:
        jq = jq.where(dd.Source.url.contains('%%' + brand))
    jq = jq.alias('jq')
    query = dd.Result.select(dd.Result, jq.c.url).join(jq, on = (jq.c.id == dd.Result.source_id))
    for r in query:
        url = r.url
        content = eval(r.content)
        if not content['code']:
            empty_code.append(url)
        if not content['price']:
            empty_price.append(url)
        if not content['intro']:
            empty_intro.append(url)
        if not content['images']:
            empty_images.append(url)
    write_to_file('code.txt', empty_code)
    write_to_file('price.txt', empty_price)
    write_to_file('intro.txt', empty_intro)
    write_to_file('images.txt', empty_images)
