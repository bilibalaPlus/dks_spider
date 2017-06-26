# coding: utf-8

import argparse
import datetime as dt
import importlib
import multiprocessing
import socket
import sys
import threading
import time

sys.path.append('.')
import dks_config as dc
import dks_database as dd
import dks_queue as dq

ts_new = dc.task_status['new']
ts_inprogress = dc.task_status['inprogress']
ts_finished = dc.task_status['finished']
js_new = dc.job_status['new']
js_finished = dc.job_status['finished']
js_failed = dc.job_status['failed']

def parse_args():
    parser = argparse.ArgumentParser()
    ########## DKS ##########
    # 1. -s --spider: 指定爬虫实现模块
    # 2. -t --tn: 线程数量
    #########################
    parser.add_argument('-s',
                        '--spider',
                        help = 'Specify which spider to use. For example, use spider for spider.py.',
                        default = 'dks_spider_sample')
    parser.add_argument('-t',
                        '--tn',
                        help = 'How many threads to use',
                        type = int,
                        default = 0)
    return parser.parse_args()
    
def hear_beat():
    address = socket.gethostbyname(socket.gethostname())
    address += ':%s' % dc.worker['port']
    rs = dd.Worker.select().where(dd.Worker.address == address)
    if rs:
        row = rs.get()
    else:
        row = dd.Worker(name = dc.worker['name'], address = address)
    while True:
        row.updated_at = dt.datetime.now()
        row.save()
        time.sleep(dc.worker['hb_interval'])

def working_thread(spider):
    while True:
        try:
            tasks = dd.Task.select().where(dd.Task.status == ts_inprogress)
            for task in tasks:
                task_id = task.id
                print('task: %d' % task_id)
                job_queue = dq.Queue(str(task_id))
                while True:
                    jobs = job_queue.get_k(dc.worker['tasks'])
                    if jobs:
                        ########## DKS ##########
                        # 用户自己实现spider模块以及要求的parse函数
                        # 1. _jobs是一个list，每个元素是一个dict。
                        # 2. 每个元素包含以下key：id, source_id和url
                        # 3. result是一个list，每个元素是一个dict，对应每个job的处理结果。
                        #    1. id: job.id
                        #    2. source_id: job.source_id
                        #    3. status
                        #    4. message
                        #    5. content
                        #########################
                        _jobs = []
                        for job in jobs:
                            _jobs.append(eval(job)) # DKS: 反序列化为dict
                        result = spider.parse(_jobs)
                        for r in result:
                            _job = dd.Job.select().where(dd.Job.id == r['id']).get()
                            _job.status = r['status']
                            _job.message = r['message']
                            _job.updated_at = dt.datetime.now()
                            _job.save() # DKS: 更新job状态
                            # DKS: 记录去重判断
                            _r = dd.Result.select().where(dd.Result.source_id == r['source_id'])
                            if _r:
                                _r = _r.get()
                                _r.updated_at = dt.datetime.now()
                            else:
                                _r = dd.Result()
                                _r.source_id = r['source_id']
                            _r.content = r['content']
                            _r.save() # DKS: 保存结果
                    else:
                        break
            time.sleep(dc.worker['hb_interval'])
        except Exception as e:
            print(e)

if __name__ == '__main__':
    args = parse_args()
    spider = importlib.import_module(args.spider) # DKS: 动态加载爬虫实现模块
    threads = []
    for i in range(multiprocessing.cpu_count() if args.tn <= 0 else args.tn):
        threads.append(threading.Thread(target = working_thread, args=(spider,)))
    threads.append(threading.Thread(target = hear_beat))
    for t in threads:
        t.daemon = True
        t.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit()
