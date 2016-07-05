#coding:utf8
from flask import Blueprint
appinfo = Blueprint('httpinfo', __name__)
import views
from flask import render_template, redirect, request, url_for, flash
from Whatweb import Whatweb
import time


@appinfo.route("/appinfo")
def info():
    t = time.time()
    s = request.args.get("s", None)
    if s is not None:
        app = Whatweb(s).result_info
        return render_template("appinfo.html", app=app, s=s, t=(time.time()-t))
    else:return render_template("appinfo.html")
