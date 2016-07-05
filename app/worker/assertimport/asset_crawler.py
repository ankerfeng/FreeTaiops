#!/usr/bin/env python
#coding:utf8
#   原创：lijiejie.com (http://www.lijiejie.com)

import os
import sys
#print os.path.abspath("./../../../")
sys.path.append(os.path.abspath("./../../../"))
rootdir = os.path.abspath(os.path.dirname(__file__))

import Queue
import threading
import time
import optparse
import dns.resolver
from lib.consle_width import getTerminalSize
from lib.netSub import load_net_suffix
from datetime import datetime

from app.common.modles import DnsModel, Session


class assetCrawler:

    def __init__(self, target, names_file=rootdir+'./dict/subnames.txt', threads_num=30):

        self.target=target
        self.names_file = names_file
        self.threads_num = threads_num
        self.lock = threading.Lock()
        self.console_width = getTerminalSize()[0]
        self.console_width -= 2    # Cal width when starts up
        self.resolvers = [dns.resolver.Resolver() for _ in range(threads_num)]
        self.domains = Queue.Queue()
        self.ips = set()


    def load(self, target):
        '''
        加载
        :param target:
        :return:None
        '''
        self.target = target.strip()
        self.thread_count = self.threads_num
        self.scan_count = self.found_count = 0
        self.net_sub = load_net_suffix(self.target)
        self.load_dns_servers()
        self.load_sub_names()
        self.load_next_sub()
        outfile = rootdir+os.sep+os.path.join('data',target.replace('.', '_'))
        self.outfile = open(outfile, 'w')
        self.ip_dict = {}


    def load_dns_servers(self):
        '''
        加载dns服务
        :return:None
        '''
        dns_servers = []
        with open(rootdir+os.sep+os.path.join('dict', 'dns_servers.txt')) as f:
            for line in f:
                server = line.strip()
                if server.count('.') == 3 and server not in dns_servers:
                    dns_servers.append(server)
        self.dns_servers = dns_servers
        self.dns_count = len(dns_servers)

    def load_sub_names(self):
        '''
        加载子域名字典
        :return:None
        '''
        self.queue = Queue.Queue()
        _tmp = set(self.net_sub)
        with open(self.names_file) as f:
            for line in f:
                sub = line.strip()
                if sub: _tmp.add(sub)
        for _ in _tmp:
            self.queue.put(_)

    def load_next_sub(self):
        '''
        加载多级子域名字典
        :return:None
        '''
        tmp = set(self.net_sub)
        with open(rootdir+os.sep+os.path.join('dict', 'next_sub.txt')) as f:
            for line in f:
                sub = line.strip()
                tmp.add(sub)
        self.next_subs = list(tmp)

    def update_scan_count(self):
        '''
        更新任务总数
        :return:None
        '''
        self.lock.acquire()
        self.scan_count += 1
        self.lock.release()

    def print_progress(self, error=None):

        self.lock.acquire()
        if error is not None:
            sys.stdout.write('\r' + ' ' * (self.console_width - len(error)) + error)
        else:
            msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
                self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
            sys.stdout.write('\r' + ' ' * (self.console_width -len(msg)) + msg)
        sys.stdout.flush()
        self.lock.release()

    def add_host(self, answers):

        #将结果保存至数据库

        session = Session()
        try:
            #是不是cname
            if answers.qname == answers.canonical_name:
                dns_info = DnsModel(host=answers.qname, nstype="A", cname="", ip=', '\
                                    .join([answer.address for answer in answers]), udate=datetime.now())
            else:
                dns_info = DnsModel(host=answers.qname, nstype="CNAME", cname=answers.canonical_name, ip=', '\
                                    .join([answer.address for answer in answers]), udate=datetime.now())

            session.add(dns_info)
            try:
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()

            from app.worker.tasks import site_crawler
            site_crawler.delay(str(answers.qname)) #网站首页爬行

            from app.worker.tasks import port_crawler
            for answer in answers:
                if answer.address not in self.ips:
                    port_crawler.delay(answer.address) #ip服务扫描
                    self.ips.add(answer.address)

        except BaseException, e:
            print e.message

    def brute(self):
        '''
        枚举子域名
        :return:
        '''
        thread_id = int( threading.currentThread().getName())
        self.resolvers[thread_id].nameservers = [self.dns_servers[thread_id % self.dns_count]]
        self.resolvers[thread_id].lifetime = self.resolvers[thread_id].timeout = 1.0
        while self.queue.qsize() > 0 and self.found_count < 3000:
            sub = self.queue.get(timeout=1.0)
            try:
                cur_sub_domain = sub + '.' + self.target
                answers = self.resolvers[thread_id].query(cur_sub_domain)
                is_wildcard_record = False
                if answers:
                    for answer in answers:
                        self.lock.acquire()
                        if answer.address not in self.ip_dict:
                            self.ip_dict[answer.address] = 1
                        else:
                            self.ip_dict[answer.address] += 1
                            if self.ip_dict[answer.address] > 10:
                                is_wildcard_record = True
                        self.lock.release()
                    if is_wildcard_record:
                        self.update_scan_count()
                        self.print_progress()
                        continue

                    self.lock.acquire()
                    self.found_count += 1
                    ips = ', '.join([answer.address for answer in answers])
                    msg = cur_sub_domain.ljust(30) + ips
                    sys.stdout.write('\r' + msg + ' ' * (self.console_width- len(msg)) + '\n\r')
                    sys.stdout.flush()
                    self.add_host(answers=answers)
                    self.outfile.write(cur_sub_domain.ljust(30) + '\t' + ips + '\n')
                    self.lock.release()
                    for i in self.next_subs:
                        self.queue.put(i + '.' + sub)
            except Exception, e:
                self.print_progress(error=e.message)
                pass
            self.update_scan_count()
            self.print_progress()
        self.print_progress()
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    def run(self):

        #启动子域名爆破
        self.load(self.target)
        self.start_time = time.time()

        for i in range(self.threads_num):
            t = threading.Thread(target=self.brute, name=str(i))
            t.setDaemon(True)
            t.start()
        while self.thread_count > 0:
            time.sleep(0.01)
            #print self.thread_count
        return True

if __name__ == '__main__':
    d = assetCrawler("usth.org")
    d.run()


