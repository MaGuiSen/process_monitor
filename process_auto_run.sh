#!/bin/sh
date "+%Y-%m-%d %H:%M:%S"
echo start check process
echo $PYTHONPATH
python2.7 /home/gsma/monitor/process_auto_run.py /home/gsma/monitor/conf_file.json