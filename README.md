FreeTaiops Version 1.0
---
```
 _____             _____     _                 
|  ___| __ ___  __|_   _|_ _(_) ___  _ __  ___ 
| |_ | '__/ _ \/ _ \| |/ _` | |/ _ \| '_ \/ __|
|  _|| | |  __/  __/| | (_| | | (_) | |_) \__ \
|_|  |_|  \___|\___||_|\__,_|_|\___/| .__/|___/
                                    |_|  
```
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) 
简介- Taiops-自由版
---
```
Tai是泰山，有稳如泰山的寓意。ops是运维安全的英文简写。但是自由版并没有带安全检测的功能，感兴趣的朋友可以自己拓展下。
自由版的主要功能：收集子域名、端口信息并保存。自建项目分类，收藏IP、域名。
采用的开发语言、框架、模块等：Python2.7、Flask以及一些拓展、Celery、Redis、MySQL
项目当中有些脚本摘自开源社区但保留了__author__，大家可在文件中看到。
```
安装环境搭建：debian-kali
---
```
安装Flask：http://docs.jinkan.org/docs/flask/installation.html
安装redis：http://redis.io/topics/quickstart
安装MySQL：http://www.cnblogs.com/xusir/p/3334217.html
安装Python 依赖包：pip install -r requirements.txt
数据库结构：taiops.sql
```
目录结构
---
```
├── app_config.xml 
├── appinfo 
│   ├── app_finger 
    |...
├── auth
│   ├── form.py
│   |...
├── common
│   ├── config.py
│   |...
├── core
│   └── __init__.py
├── __init__.py
├── main
│   ├── errors.py
│   |...
├── server.py
├── static
├── templates
└── worker
    ├── assertimport
    │   ├── asset_crawler.py
    │   |...
```
配置文件
---
```
配置文件（一)
├── common
│   ├── config.py

配置文件（二)
├── common
│   └── modles.py

配置文件（三)
└── worker
    ├── celeryconfig.py
```
启动
---
```
启动celery:celery -A tasks worker --loglevel=info
启动server: (线上环境 默认)python server.py production (调试模式）python server.py development
```
未来
---
```
能力有限，水平有限，时间有限，还有一些细节问题未来的及处理，比如：ssrf问题，缓存问题等
分享这个自由版本主要是想发出来和大家一起讨论，共同进步。
在专业版本中，将添加爬虫，和扫描的功能。可将收集到的目标导入扫描。
如果有任何bug欢迎提交issues,或者有想和我一起完成这个项目的伙伴可加我微信讨论。
```
![](http://dev.bugsrc.com/wp-content/uploads/2016/07/222.png)
