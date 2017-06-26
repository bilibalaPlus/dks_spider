# coding: utf-8

import argparse
import datetime as dt
import sys

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
    # -a --action参数说明
    # 1. create: 创建新任务
    # 2. list: 显示活跃工作节点
    # 3. view: 查看任务状态
    # 4. retry: 任务重试
    #########################
    parser.add_argument('-a',
                        '--action',
                        help = 'Create task, list worker, view task status. If action is view, use -t to assign task id.',
                        default = 'create')
    # DKS: -t, --tid: 任务id
    parser.add_argument('-t', '--tid',
                        help = 'tid',
                        default = 0,
                        type = int)
    return parser.parse_args()

def list_worker():
    rs = dd.Worker.select().where(dd.Worker.updated_at >= (dt.datetime.now() - dt.timedelta(seconds = 900)))
    print('%d workers' % rs.count())
    for row in rs:
        print('\t %s: %s' % (row.name, row.address))
    

def create_task():
    task = dd.Task(status = ts_new)
    task.save()
    task_id = task.id
    rq = dq.Queue(task_id)
    sources = dd.Source.select().where(dd.Source.enabled == True)
    for source in sources:
        job = dd.Job(task_id = task_id, source_id = source.id, status = js_new)
        job.save()
        rq.put({'id':job.id, 'source_id':source.id, 'url':source.url})
    task.status = ts_inprogress
    task.tasks = len(sources)
    task.save()
    print('Task %d is scheduled with %d jobs' % (task_id, task.tasks))

def view_task(task_id):
    rs = dd.Task.select().where(dd.Task.id == task_id)
    task = rs.get() if rs else None
    if task:
        if task.status == ts_finished:
            print('Task %d finished: %d total, %d finished, %d failed.' % (task_id, task.tasks, task.finished, task.failed))
        elif task.status == ts_inprogress:
            jobs = dd.Job.select().where(dd.Job.task_id == task_id)
            total_jobs = jobs.count()
            new_jobs = 0
            finished_jobs = 0
            failed_jobs = 0
            for job in jobs:
                if job.status == js_new:
                    new_jobs += 1
                elif job.status == js_finished:
                    finished_jobs += 1
                elif job.status == js_failed:
                    failed_jobs += 1
                else:
                    raise Exception('Job %d is in unknown status %s, please check it.' % (job.id, job.status))
            task.unfinished = new_jobs
            task.finished = finished_jobs
            task.failed = failed_jobs
            if (finished_jobs + failed_jobs) == total_jobs:
                task.status = ts_finished
            task.save()
            print('Task %d in progress: %d total, %d new, %d finished, %d failed.' % (task_id, total_jobs, new_jobs, finished_jobs, failed_jobs))
        elif task.status == ts_new:
            print('Task %d not started yet' % task_id)
        else:
            raise Exception('Unknown status %s for task %d' % (r.status, task_id))
    else:
        raise Exception('Task %d not found' % task_id)

def retry_task(task_id):
    if dd.Task.select().where((dd.Task.id == task_id) and (dd.Task.status == ts_inprogress)):
        rq = dq.Queue(task_id)
        jobs = dd.Job.select().where(dd.Job.status != js_finished)
        for job in jobs:
            source = dd.Source.select().where(dd.Source.id == job.source_id).get()
            rq.put({'id':job.id, 'source_id':source.id, 'url':source.url})
        print('Task %d rescheduled %d jobs' % (task_id, len(jobs)))
    else:
        raise Exception('Task %d not found' % task_id)
    
if __name__ == '__main__':
    args = parse_args()
    action = args.action
    if action == 'list':
        list_worker()
    elif action == 'create':
        create_task()
    elif action == 'view':
        view_task(args.tid)
    elif action == 'retry':
        retry_task(args.tid)
