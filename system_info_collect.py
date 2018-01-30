# -*- coding: utf-8 -*-
import json
import os
import platform
import datetime
import psutil
import sys
import socket
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


def save_log(log):
    log = log.encode(u'utf8')
    if log == u'\n':
        time_str = u''
    else:
        time_str = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S') + u'： '
    log = time_str + log
    file_path = os.path.dirname(os.path.realpath(__file__)) + u'/log'
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    file_name_path = file_path + u'/info_collect_flow_log.txt'
    fsize = 0
    if os.path.exists(file_name_path):
        fsize = os.path.getsize(file_name_path)
        fsize /= float(1024 * 1024)
        fsize = round(fsize, 2)
    with open(file_name_path, u'a') as loadF:
        if fsize > 100:
            loadF.truncate()
        loadF.write(log)
        loadF.close()


def get_system_info():
    # cpu使用率
    cpu_use = (str)(psutil.cpu_percent(1)) + '%'
    # 内存总共.total
    memory_total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0), 2)) + 'M'
    # 剩余内存.free
    memory_free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0), 2)) + 'M'
    # 当前项目所在磁盘剩余
    disk_free = str(psutil.disk_usage("/")[2] / (1024.0 * 1024 * 1024))
    save_log(u"cpu使用率=%s, 总内存=%s, 内存剩余=%s, 项目所在磁盘剩余=%s" % (cpu_use, memory_total, memory_free, disk_free))
    return [
        {
            u'name': u'cpu使用率',
            u'code': u'cpu_use',
            u'value': cpu_use,
        },
        {
            u'name': u'总内存',
            u'code': u'memory_total',
            u'value': memory_total,
        },
        {
            u'name': u'内存剩余',
            u'code': u'memory_free',
            u'value': memory_free,
        },
        {
            u'name': u'项目所在磁盘剩余',
            u'code': u'disk_free',
            u'value': disk_free,
        },
    ]


def send_sys_info(sys_info_str):
    try:
        url = u"http://localhost:10012/send/sys_info"
        result = requests.post(url, data={u'system_info': sys_info_str})
        save_log(str(result.status_code) + '\n')
        save_log(str(result.content) + '\n')
    except Exception, e:
        save_log(str(e.message) + '\n')


params = sys.argv
if params and len(params) > 1:
    # 说明有参数
    conf_path = params[1]
    loadF = None
    process_status = []
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
                    info = program.get(u'info', u'no exist')
                    is_running = False
                    pids = psutil.pids()
                    for pid in pids:
                        try:
                            p = psutil.Process(pid).as_dict(attrs=[u'pid', u'name', u'exe', u'cwd'])
                        except:
                            continue
                        p_name = p.get(u'name', '')
                        p_cwd = p.get(u'cwd', '')
                        p_exe = p.get(u'exe', '')
                        if name in p_name and exe in p_exe and cwd in p_cwd:
                            # 说明就是这个线程在运行
                            is_running = True
                    if not is_running:
                        # 说明需要启动
                        # 调用启动的代码
                        save_log(u'--------------------------\n')
                        save_log(u'name=%s, exe=%s, cwd=%s\n' % (name, exe, cwd))
                        save_log(u'no running\n')
                        is_running = 0
                    else:
                        save_log(u'name=%s, exe=%s, cwd=%s\n' % (name, exe, cwd))
                        save_log(u'program is running\n')
                        is_running = 1
                    process_status.append({
                        u"info": info,
                        u"exe": exe,
                        u"name": name,
                        u"cwd": cwd,
                        u"is_running": is_running
                    })
                hostname = socket.gethostname()
                ipList = socket.gethostbyname_ex(hostname)
                if len(ipList) == 3:
                    ipList = ipList[2]
                system_info = {
                    u"hostname": hostname,
                    u"ip": ipList,
                    u"sys_info": get_system_info(),
                    u"process_status": process_status
                }
                system_info_str = json.dumps(system_info)
                send_sys_info(system_info_str)

        else:
            save_log(u'no config file\n')
    finally:
        if loadF:
            loadF.close()

