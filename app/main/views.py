#!/usr/bin/env python
#coding:utf8

import sys
import os
sys.path.append(os.path.abspath("./../../"))
from flask import render_template, redirect, url_for, abort, \
    flash, request,current_app, make_response, jsonify, g as G
from flask.ext.login import current_user, login_required

from datetime import datetime

from app.server import db
from app.common.modles import TaskModel
from app.worker.hashid import hashid

from inc import main


@main.route('/tasklist', methods=["GET"])
@login_required
def qtasklist():

    #任务记录查询
    db.session.commit()  # 对 我就是不行 有本事你把这个问题解决了 http://www.v2ex.com/t/198981
    pn = int(request.args.get("pn", 1))
    tables = list()
    paginate = TaskModel.query.filter(TaskModel.uid==current_user.id).order_by(TaskModel.status).paginate(pn, 15, False)
    sites = paginate.items
    for site in sites:
        tables.append(site)

    return render_template('task_list.html', tables=tables, pagination=paginate)


@main.route('/hashinfo', methods=["GET", "post"])
def hash_id():

    #加密识别
    s = request.args.get("s", None)
    if s is not None:
        hashids = hashid.identify_hashes(s.strip())
        return render_template("hashinfo.html", hashids = hashids, s=s)
    else:return render_template("hashinfo.html")