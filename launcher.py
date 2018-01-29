# -*- coding: utf-8 -*-
import os
# subprocess.Popen("cmd.exe", shell=True)
ss = os.popen("START %cd%/cmd/window/ccmdc.bat")
ss = os.popen("@echo ddlla")
ss = os.popen("START %cd%/cmd/window/ccmdb.bat")