#!/bin/bash
cd /home/gsma/test/
export PYTHONPATH=$PYTHONPATH:$PWD
export PYTHONIOENCODING=utf-8
cd project1
nohup python2.7 monitor.py> output 2>&1&