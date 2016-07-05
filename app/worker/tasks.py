#!/usr/bin/env python
#coding:utf8

'''
 windows:celery -A tasks worker --loglevel=info -P threads
 linux:celery -A tasks worker --loglevel=info
'''

import os
import sys
import time
sys.path.append(os.path.abspath("./../../"))
from datetime import datetime
from app.worker import celeryconfig
from celery import Celery
from assertimport.asset_crawler import assetCrawler
from sitecrawler.sitecrawler import SiteCrawler
from portcrawler.portcrawler import PortCrawler
from app.common.modles import TaskModel, Session


app = Celery('tasks')
app.config_from_object(celeryconfig)


def start_save(task_name, args, uid):
    #开始时间
    session = Session()
    infotask = TaskModel(uid=uid, taskname=task_name, args=",".join(args), status=0, starttime=datetime.now())
    session.add(infotask)
    session.commit()
    id = infotask.id
    session.close()
    return id

def end_save(id):
    #结束时间

    session = Session()
    infotask = session.query(TaskModel).filter(TaskModel.id==id).with_lockmode("update").first()
    infotask.status=1
    infotask.endtime = datetime.now()
    session.add(infotask)
    session.commit()
    session.close()

@app.task
def asset_import(domain, uid=1000):
    #资产导入

    tid = start_save(task_name="资产导入", args=[str(domain), ], uid=uid)
    crawler = assetCrawler(domain)
    crawler.run()
    end_save(tid)

@app.task
def site_crawler(host, uid=1000):
    #首页爬行

    tid = start_save(task_name="网站分析", args=[str(host), ], uid=uid)
    crawler = SiteCrawler(host=host)
    crawler.run()
    end_save(tid)

@app.task
def port_crawler(ip, port=None, uid=1000):
    #端口扫描

    tid = start_save(task_name="端口探测", args=[str(ip),], uid=uid)
    crawler = PortCrawler(ip)
    crawler.run()
    end_save(tid)


