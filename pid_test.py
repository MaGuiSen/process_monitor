#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psutil
import sys

params = sys.argv
keyword = ''
if params and len(params) > 1:
    # 说明有参数
    keyword = params[1]

pids = psutil.pids()
for pid in pids:
    try:
        p = psutil.Process(pid).as_dict(attrs=['pid', 'name', 'username', 'exe', 'cwd', 'create_time'])
        name = p["name"] or ''
        exe = p["exe"] or ''
        cwd = p["cwd"] or ''
        if keyword not in name and keyword not in exe and keyword not in cwd:
            continue
        print 'name: ', name
        print 'exe: ', exe
        print 'cwd: ', cwd
    except Exception, e:
        continue
