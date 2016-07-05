#!/usr/bin/env python
#coding:utf8

import os
import sys
sys.path.append(os.path.abspath("./../../../"))
from datetime import datetime
from inc import main
from flask import render_template, redirect, request, flash, g as G
from flask.ext.login import current_user, login_required

from form import PojForm, DelPojForm
from app.server import db
from app.common.form import flash_errors, return_errors
from app.common.modles import ProjectModel, ProjectDomainModel, ProjectSiteModel, ProjectIpModel


@main.route('/poj', methods=['GET', 'POST'])
@login_required
def project():
    '''
    项目列表
    :return:
    '''
    form = DelPojForm()
    if request.method == "POST":

        if form.validate_on_submit():
            pid = form.pid.data
            project = ProjectModel.query.filter(ProjectModel.id==pid, ProjectModel.uid==current_user.id).first()

            if project is not None:
                db.session.delete(project)
                db.session.query(ProjectDomainModel).filter(ProjectDomainModel.pid==pid).delete()
                db.session.commit()
                flash(message="删除成功!")
            else:
                flash(message="非法操作!")

    pn = int(request.args.get("pn", 1))
    q = request.args.get("q", '')
    paginate = ProjectModel.query.filter(ProjectModel.uid == current_user.id).paginate(pn, 10, False)
    projects = paginate.items

    return render_template('project_list.html', tables=projects, pagination=paginate, q=q, form=form)

@main.route('/poj/<int:pid>')
@login_required
def project_detail(pid):
    '''
    查看项目
    项目内容异步查询
    '''
    pn = int(request.args.get("pn", 1))
    type = request.args.get("type", None) #查询的类别
    if type is None or type == "domain":
        type="domain"
        G.poj_domain_pg = ProjectDomainModel.query.filter(ProjectDomainModel.pid == pid,\
                                                          ProjectDomainModel.uid == current_user.id).paginate(pn, 10, False)
        G.poj_domains = G.poj_domain_pg.items

    elif type == "site":
        G.poj_site_pg = ProjectSiteModel.query.filter(ProjectSiteModel.pid == pid,\
                                                          ProjectSiteModel.uid == current_user.id).paginate(pn, 10, False)
        G.poj_sites = G.poj_site_pg.items

    elif type == "ip":
        G.poj_ip_pg = ProjectIpModel.query.filter(ProjectIpModel.pid == pid, \
                                                      ProjectIpModel.uid == current_user.id).paginate(pn, 10, False)
        G.poj_ips = G.poj_ip_pg.items

    return render_template("project_detail.html", G=G, pid=pid, type=type)

@main.route('/poj/add', methods=['POST', 'GET'])
@login_required
def add_project():
    '''
    添加项目
    :return:
    '''
    form = PojForm()
    if request.method=="POST":
        if form.validate_on_submit():
                uid = current_user.id
                poj = ProjectModel(name=form.name.data, rootdomain=form.rootdomain.data, note=form.note.data, uid=uid, utime = datetime.now())
                db.session.add(poj)
                db.session.commit()
                pdomain = ProjectDomainModel(domain=form.rootdomain.data, pid=poj.id, note="项目根域名", uid = uid, utime=datetime.now())
                db.session.add(pdomain)
                db.session.commit()
                flash(message="项目添加成功")
        else:
            flash_errors(form)

    return render_template("add_project.html", form=form)

@main.route('/poj/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_poj(id):
    '''
    编辑项目
    :param id:
    :return:
    '''
    form = PojForm()
    project = ProjectModel.query.filter(ProjectModel.id == id, ProjectModel.uid == current_user.id).first()
    if project is not None:
        if request.method == "POST":
            if form.validate_on_submit():
                project.name = form.name.data
                project.rootdomain = form.rootdomain.data
                project.note = form.note.data
                db.session.commit()
                flash(message="修改成功.")
            else:
                flash_errors(form)
    else:
        flash(message="项目不存在")

    return render_template("edit_project.html", form=form, data=project)

