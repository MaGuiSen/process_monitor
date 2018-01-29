#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import json

import psutil,os,time
# https://www.jianshu.com/p/535a6b111038 参考文档
# http://www.aichengxu.com/python/9934044.htm 监控demo
# window定时任务1、写命令批量处理文件bat 2、启动定时任务 参考：http://blog.csdn.net/Gpwner/article/details/77882131
# if __name__ == '__main__':
#     pass
# pids = psutil.pids()
# for pid in pids:
#     p = psutil.Process(pid).as_dict(attrs=['pid', 'name', 'username', 'exe', 'cwd', 'create_time'])
#     for keys in p.keys():
#         tempText = keys + ':' + str(p[keys]) + '\n'
#         print tempText

# from subprocess import PIPE
# p1=psutil.Popen(["python","-c","print('hello')"],stdout=PIPE).as_dict(attrs=['pid', 'name', 'username', 'exe', 'cwd', 'create_time'])
# for keys in p1.keys():
#             tempText = keys + ':' + str(p1[keys]) + '\n'
#             print tempText
#
#
# import subprocess
# subprocess.Popen("scrapy crawl News")

# conf_obj = [
#     {
#         u'name': u'python.exe',
#         u'exe': u'C:\Python27\python.exe',
#         u'cwd': u'spider_monitor\util'
#     },
# ]

# 这是linux
"""
username:gsma

exe:/usr/bin/python2.7

name:python2.7

pid:6283

create_time:1516937723.22

cwd:/home/gsma/test/project1
"""
# 这是window  /home/gsma/monitor/cmd/linux
"""
username:DESKTOP-ESM6QSD\1ping

exe:C:\Python27\python.exe

name:python.exe

pid:6796

create_time:1516867149.0

cwd:C:\gsma\pythonWorkSpace\spider_monitor\util
"""
# 得到传入的参数
import sys
import platform
import os
params = sys.argv
# params = ['./util/SystemUtil.py', './conf_file.json']
if params and len(params)>1:
    # 说明有参数
    conf_path = params[1]
    loadF = None
    try:
        if os.path.exists(conf_path):
            # 不存在，则需要下载
            with open(conf_path, u'r') as loadF:
                # 根据系统来
                system_str = platform.system()
                program_obj = json.load(loadF)
                program_list = program_obj.get(system_str, [])
                for program in program_list:
                    name = program.get(u'name', u'no exist')
                    cwd = program.get(u'cwd', u'no exist')
                    exe = program.get(u'exe', u'no exist')
                    command = program.get(u'command', u'')
                    print name, exe, cwd
                    if not command:
                        continue
                    is_running = False
                    pids = psutil.pids()
                    for pid in pids:
                        p = psutil.Process(pid).as_dict(attrs=[u'pid', u'name', u'exe', u'cwd'])
                        p_name = p.get(u'name', '')
                        p_cwd = p.get(u'cwd', '')
                        p_exe = p.get(u'exe', '')
                        if u"python" in p_name:
                            print p_name, p_cwd, p_exe
                        if name in p_name and exe in p_exe and cwd in p_cwd:
                            pass
                            # 说明就是这个线程在运行
                            is_running = True
                    if not is_running:
                        # 说明需要启动
                        pass
                        # 调用启动的代码
                        print u'未运行,执行命令'
                        # 记录当前新启动的，防止重复启动
                        os.popen(command)
                    else:
                        print u'正在运行'
    finally:
        if loadF:
            loadF.close()