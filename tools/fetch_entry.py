# coding: utf-8

# 使用entry项目数据库

import argparse
import sys

sys.path.append('../')
import dks_database as dd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b',
                        '--brand',
                        help = 'Specify the brand you want to fetch')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    brand = args.brand
    rows = dd.Result.select()
    if brand:
        rows = rows.where(dd.Result.content.contains(brand))
    for row in rows:
        for product in row.content.split(';'):
            # 生成SQL语句
            query = 'insert into source(url, enabled, created_at, updated_at) values("'
            query += product + '", true, now(), now());'
            print(query)
