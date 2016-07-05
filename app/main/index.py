#!/use/bin/env python
#coding:utf8

import os
import sys
sys.path.append(os.path.abspath("./../../../"))
from datetime import datetime
from flask import render_template, redirect, request, flash
from flask.ext.login import current_user, login_required
from form import AssetForm, SiteForm, IpForm, IPPortForm
from app.server import db
from app.common.form import flash_errors
from app.worker.tasks import asset_import, site_crawler, port_crawler
from app.common.modles import AssertAddLogModel
from inc import main


@main.route('/', methods=["POST", "GET"])
@login_required
def index():
    '''
    home page route
    :return:index.html
    '''

    form_groups = {'assert':AssetForm(), 'site':SiteForm(), 'ip':IpForm(), 'ip_port':IPPortForm()}
    pn = int(request.args.get("pn", 1))
    q = request.args.get("q", '')
    add_type = request.args.get("type", None)
    paginate = AssertAddLogModel.query.filter(AssertAddLogModel.uid == current_user.id).paginate(pn, 10, False)
    logs = paginate.items

    if request.method == "POST":
        if form_groups['assert'].validate_on_submit():

            value = form_groups['assert'].domain.data
            asset_import.delay(value, current_user.id)
            model = AssertAddLogModel(uid = current_user.id, value = value,\
                                      addtime = datetime.now(), type = 'assert',\
                                      note = form_groups['assert'].note.data)
            db.session.add(model)
            db.session.commit()
            flash(message="资产导入成功")

        elif form_groups['site'].validate_on_submit():
            value = form_groups['site'].url.data
            site_crawler.delay(value, current_user.id)
            model = AssertAddLogModel(uid = current_user.id, value = value,\
                                      addtime = datetime.now(), type = 'site',\
                                      note = form_groups['site'].note.data)
            db.session.add(model)
            db.session.commit()
            flash(message='网站添加成功')

        elif form_groups['ip'].validate_on_submit():
            value = form_groups['ip'].ip.data
            port_crawler.delay(value)
            model = AssertAddLogModel(uid=current_user.id, value=value, \
                                      addtime=datetime.now(), type='IP', \
                                      note=form_groups['ip'].note.data)
            db.session.add(model)
            db.session.commit()
            flash(message='IP添加成功')

        elif form_groups['ip_port'].validate_on_submit():
            value = form_groups['ip_port'].target.data + ":" + str(form_groups['ip_port'].port.data)
            # port_crawler.delay(form_groups['ip_port'].ip.data, [form_groups['ip_port'].port])
            model = AssertAddLogModel(uid=current_user.id, value=value, \
                                      addtime=datetime.now(), type='IP-Port', \
                                      note=form_groups['ip_port'].note.data)
            db.session.add(model)
            db.session.commit()
            flash(message="IP端口添加成功")

        elif add_type is not None:

            flash_errors(form_groups[add_type])

    return render_template('index.html', form_groups = form_groups, tables = logs, pagination = paginate, q = q, pn = pn)