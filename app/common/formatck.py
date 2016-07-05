#!/usr/bin/env python
#coding:utf8

import re
import os
import sys


def domain_check(string):
    """
    判断域名格式
    """
    with open(os.path.dirname(os.path.realpath(__file__))+os.sep+"domain.sufix") as f:
        dsufix = f.read().strip().split(",")
        dsufix = "|".join(dsufix)
    pattern = "^([0-9a-zA-Z_-]+\.)+(%s)$" % dsufix
    regx = re.compile(pattern=pattern)
    res = regx.match(string)
    if res:
        if res.group(0) in "".join(res.groups()):
            return {"domain":True, "root":True}
        else:
            return {"domain":True, "root":False}

    return False
def ip_check(string):
    regex = re.compile(r"(?P<D>\d+\.\d+\.\d+\.\d+)|(?P<C>\d+\.\d+\.\d+)")
    mc = regex.match(string)
    if mc is not None:
        if mc.group("D") is not None:
            return "D"
        else:
            return "C"
    else:
        return False
