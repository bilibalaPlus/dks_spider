# coding: utf-8

import sys

sys.path.append('.')
import config

js_new = config.job_status['new']
js_finished = config.job_status['finished']
js_failed = config.job_status['failed']

def parse(jobs): # DKS: 爬虫具体实现部分
    result = []
    i = 0
    for job in jobs:
        result.append({'id':job['id'], 
                       'source_id':job['source_id'],
                       'content':'test_%02d' % i,
                       'status':js_finished,
                       'message':'Good'})
        i += 1
    return result
