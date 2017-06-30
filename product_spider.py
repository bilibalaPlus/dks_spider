# coding: utf-8

# 根据入口页面链接找到相关的产品链接

import sys
import time
import traceback

sys.path.append('.')
import dks_config as dc
import util

js_new = dc.job_status['new']
js_finished = dc.job_status['finished']
js_failed = dc.job_status['failed']
parsers = util.load_parsers('product_parser')

def parse(jobs):
    result = []
    driver = util.create_chrome_driver()
    for job in jobs:
        result.append({'id':job['id'], 'source_id':job['source_id'], 'message':''})
        try:
            url = job['url']
            prefix = url.split('//')[1].split('/')[0]
            if prefix in parsers:
                content = parsers[prefix](driver, url)
                result[-1]['status'] = js_finished
                result[-1]['content'] = content
            else:
                raise Exception('Parser not found for %s' % url)
        except Exception as e:
            result[-1]['status'] = js_failed
            result[-1]['message'] = '%s\n%s' % (e, traceback.format_exc())
    driver.quit()
    return result
