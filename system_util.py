# -*- coding: utf-8 -*-
import json
import os
import platform
import sys

import datetime
import psutil


def save_log(log):
    if log == u'\n':
        time_str = u''
    else:
        time_str = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S') + u'：'
    print time_str, log
    log = log.encode(u'utf8')

    fsize = os.path.getsize(u'log_monitor.txt')
    fsize /= float(1024 * 1024)
    fsize = round(fsize, 2)
    need_clear = False
    if fsize > 100:
        need_clear = True
    with open(u'log_monitor.txt', u'a') as loadF:
        if need_clear:
            save_log(u'log文件过大，需要删除（%s）' % fsize)
            loadF.truncate()
        loadF.write(log)
        loadF.close()

params = sys.argv
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
                for index, program in enumerate(program_list):
                    save_log(u'%s========================================\n' % index)
                    name = program.get(u'name', u'no exist')
                    cwd = program.get(u'cwd', u'no exist')
                    exe = program.get(u'exe', u'no exist')
                    commands = program.get(u'commands', u'')
                    if not commands:
                        save_log(u'不存在命令\n')
                        save_log(u'name=%s, exe=%s, cwd=%s\n' % (name, exe, cwd))
                        continue
                    is_running = False
                    pids = psutil.pids()
                    for pid in pids:
                        p = psutil.Process(pid).as_dict(attrs=[u'pid', u'name', u'exe', u'cwd'])
                        p_name = p.get(u'name', '')
                        p_cwd = p.get(u'cwd', '')
                        p_exe = p.get(u'exe', '')
                        # if u"python" in p_name:
                        #     print p_name, p_cwd, p_exe
                        if name in p_name and exe in p_exe and cwd in p_cwd:
                            # 说明就是这个线程在运行
                            is_running = True
                    if not is_running:
                        # 说明需要启动
                        # 调用启动的代码
                        save_log(u'未运行--------------------------\n')
                        save_log(u'name=%s, exe=%s, cwd=%s\n' % (name, exe, cwd))
                        save_log(u'执行命令%s\n' % u''.join(commands))
                        # 记录当前新启动的，防止重复启动
                        os.popen(u''.join(commands))
                        save_log(u'执行命令完毕\n\n')
                    else:
                        save_log(u'正在运行\n')
                        save_log(u'name=%s, exe=%s, cwd=%s\n' % (name, exe, cwd))
        else:
            save_log(u'无配置文件\n')
    finally:
        if loadF:
            loadF.close()