#!/usr/bin/env python
#coding:utf8

from flask import flash


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"请重新填写 %s - %s" % (
                getattr(form, field).label.text,
                error
            ))

def return_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            yield (u"请重新填写 %s - %s" % (
                getattr(form, field).label.text,
                error
            ))
