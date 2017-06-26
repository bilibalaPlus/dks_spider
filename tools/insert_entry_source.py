# coding: utf-8

import sys

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                sql = "insert into source(url, enabled, created_at, updated_at) values('"
                sql += line + "', true, now(), now());"
                print(sql)
