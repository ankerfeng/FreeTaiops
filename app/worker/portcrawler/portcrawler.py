#!/usr/bin/env python
#coding:utf-8
#端口扫描
import nmap
import os
import sys
#print os.path.abspath("./../../../")
sys.path.append(os.path.abspath("./../../../"))
rootdir = os.path.abspath(os.path.dirname(__file__))
from datetime import datetime
from app.common.modles import IpPortModel, Session

class PortCrawler:
    def __init__(self, ip, port=None):
        self.ip = ip
        if port is None:
            self.args="--system-dns --open -Pn"
        else:
            self.args="--system-dns --open -p%s" % str(port)
        self.ports_protocol = {}
        self.data=[]
        self.save = False

    def crawler(self, ip=None):
        if ip is None:
            ip=self.ip

        nm = nmap.PortScanner()
        scaninfo = nm.scan(ip, arguments=self.args)
        if scaninfo['scan'].has_key(ip):
            self.save = True
            self.ports_protocol[ip] = {port:scaninfo['scan'][ip]['tcp'][port]['name'] for port in scaninfo['scan'][ip]['tcp']}
            #print self.ports_protocol
            #self.add_info()

    def save_msg(self):
        session = Session()

        for ip in self.ports_protocol:
            for port in self.ports_protocol[ip]:
                self.data.append({"ip":ip, "port":port, "protocol":self.ports_protocol[ip][port], "utime":datetime.now()})
        print self.data
        session.execute(
            IpPortModel.__table__.insert(),
            self.data
        )
        session.commit()
        session.close()


    def run(self):
        # self.load()
        self.crawler()
        if self.save:
            self.save_msg()

if __name__=="__main__":
    sc = PortCrawler("127.0.0.1", 80)
    sc.run()


