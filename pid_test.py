#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import psutil

pids = psutil.pids()
for pid in pids:
    p = psutil.Process(pid).as_dict(attrs=['pid', 'name', 'username', 'exe', 'cwd', 'create_time'])
    name = p["name"]
    if 'python' not in name:
        continue
    for keys in p.keys():
        tempText = keys + ':' + str(p[keys]) + '\n'
        print tempText
