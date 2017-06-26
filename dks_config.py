# coding: utf-8

db = {'host':'localhost',
      'user':'root',
      'passwd':'1234',
      'database':'dks',
      'charset':'utf8'}
      
redis = {'host':'localhost',
         'port':'6379',
         'prefix':'dks'}

task_status = {'new':'new',
               'inprogress':'inprogress',
               'finished':'finished'}

job_status = {'new':'new',
              'finished':'finished',
              'failed':'failed'}

worker = {'name':'worker',
          'port':'15001',
          'tasks':10,
          'hb_interval':30}
