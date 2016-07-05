#!/usr/bin/env python
#coding:utf8
#资产查询模块、主要为dns、ipport、site查询
#

import os
import sys
sys.path.append(os.path.abspath("./../../../"))
from inc import main
from flask import render_template, redirect, request, flash
from flask.ext.login import current_user, login_required

from app.common.modles import IpPortModel, DnsModel, SiteModel
from app.common.formatck import ip_check
from app.server import db

@main.route('/query/ipport', methods=["GET"])
@login_required
def q_ip_port():

    #ip端口查询
    db.session.commit() #对 我就是不行 有本事你把这个问题解决了 http://www.v2ex.com/t/198981
    q = request.args.get("q", None)
    pn = int(request.args.get("pn", 1))
    if q is None:
        return render_template('qipport.html')

    ilike = "%%%s%%" % q
    paginate = IpPortModel.query.filter(IpPortModel.ip.ilike(ilike)).paginate(pn, 20, False)
    ports = paginate.items

    return render_template('qipport.html', tables=ports, q=q, pagination=paginate)

@main.route('/query/dns', methods=["GET"])
@login_required
def q_dns():

    #dns记录查询
    db.session.commit() #对 我就是不行 有本事你把这个问题解决了 http://www.v2ex.com/t/198981
    tables = list()
    q = request.args.get("q", None)
    pn = int(request.args.get("pn", 1))
    if q is None:
        return render_template("qdns.html", tables=tables)

    if ip_check(q):
        ilike = "%%%s%%" % q
        paginate = DnsModel.query.filter(DnsModel.ip.ilike(ilike)).paginate(pn, 20, False)
    else:
        ilike = "%%%s%%" % q
        paginate = DnsModel.query.filter(DnsModel.host.ilike(ilike)).paginate(pn, 20, False)
    dns = paginate.items

    return render_template("qdns.html",tables=dns, q=q, pagination=paginate)

@main.route('/query/site', methods=["GET"])
def q_site():

    #网站信息查询
    db.session.commit()  # 对 我就是不行 有本事你把这个问题解决了 http://www.v2ex.com/t/198981
    q = request.args.get("q", None)
    pn = int(request.args.get("pn", 1))
    if q is None:
        return render_template('qsite.html')

    ilike = "%%%s%%" % q
    paginate = SiteModel.query.filter((SiteModel.host.ilike(ilike))).paginate(pn, 20, False)
    sites = paginate.items

    return render_template('qsite.html', tables=sites, q=q, pagination=paginate)