# coding: utf-8

import redis
import sys

sys.path.append('.')
import dks_config as dc

host = dc.redis['host']
port = dc.redis['port']
prefix = dc.redis['prefix']

class Queue:
    def __init__(self, name):
        self._db = redis.Redis(host = host, port = port)
        self.key = '%s:%s' % (prefix, name)

    def qsize(self):
        return self._db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, item):
        self._db.rpush(self.key, item)

    def get(self, block = True, timeout = None):
        if block:
            item = self._db.blpop(self.key, timeout = timeout)
        else:
            item = self._db.lpop(self.key)
        if item:
            item = item[1]
        return item
        
    def get_k(self, k):
        i = 0
        items = []
        while i < k:
            item = self.get(True, 1) # DKS: 分布式环境使用阻塞调用
            if item:
                items.append(item)
                i += 1
            else:
                break
        return items
