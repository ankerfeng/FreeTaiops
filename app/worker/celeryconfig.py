#!/usr/bin/env python
#coding:utf8

#celery配置文件


BROKER_URL = 'redis://taiops@127.0.0.1:6379/9'
CELERY_RESULT_BACKEND = 'redis://taiops@127.0.0.1:6379/10'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ENABLE_UTC = True

CELERY_ANNOTATIONS = {
    'app.worker.tasks.asset_import': {'rate_limit': '1/m'},
    'app.worker.tasks.site_crawler':{'rate_limit':'4/m'},
    'app.worker.tasks.port_crawler':{'rate_limit':'1/m'},
}

CELERY_IMPORTS = ("app.worker.tasks")