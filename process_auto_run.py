# -*- coding: utf-8 -*-
import json
import os
import platform
import datetime
import psutil
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def save_log(log, is_important=False):
    log = log.encode(u'utf8')
    if log == u'\n':
        time_str = u''
    else:
        time_str = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S') + u'： '
    log = time_str + log
    file_path = os.path.dirname(os.path.realpath(__file__)) + u'/log'
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    if is_important:
        file_name_path = file_path + u'/auto_run_execute_log.txt'
    else:
        file_name_path = file_path + u'/auto_run_flow_log.txt'
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


params = sys.argv
if params and len(params) > 1:
    # 说明有参数
    conf_path = params[1]
    loadF = None
    save_log(u'conf_path: %s\n' % conf_path)
    try:
        if os.path.exists(conf_path):
            # 不存在，则需要下载
            with open(conf_path, u'r') as loadF:
                # 根据系统来
                system_str = platform.system()
                program_obj = json.load(loadF)
                program_list = program_obj.get(system_str, [])
                executed_commands = []  # 用于启动去重
                for index, program in enumerate(program_list):
                    name = program.get(u'name', u'no exist')
                    cwd = program.get(u'cwd', u'no exist')
                    exe = program.get(u'exe', u'no exist')
                    info = program.get(u'info', u'no exist')
                    commands = program.get(u'commands', u'')
                    if not commands:
                        save_log(u'no command\n')
                        save_log(u'info=%s, name=%s, exe=%s, cwd=%s\n' % (info, name, exe, cwd))
                        continue
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
                        # if u"python" in p_name:
                        #     print p_name, p_cwd, p_exe
                        if name in p_name and exe in p_exe and cwd in p_cwd:
                            # 说明就是这个线程在运行
                            is_running = True
                    if not is_running:
                        # 说明需要启动
                        # 调用启动的代码
                        commands = u''.join(commands)
                        save_log(u'%s========================================\n' % index, is_important=True)
                        save_log(u'info=%s, name=%s, exe=%s, cwd=%s\n' % (info, name, exe, cwd), is_important=True)
                        save_log(u'no running\n', is_important=True)
                        save_log(u'execute command %s\n' % commands, is_important=True)
                        # 记录当前新启动的，防止重复启动
                        if commands in executed_commands:
                            continue
                        executed_commands.append(commands)
                        os.popen(commands)
                        save_log(u'execute command complete\n\n', is_important=True)
                    else:
                        save_log(u'info=%s, name=%s, exe=%s, cwd=%s\n' % (info, name, exe, cwd))
                        save_log(u'program is running\n')
        else:
            save_log(u'no config file\n')
    finally:
        if loadF:
            loadF.close()
