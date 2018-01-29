@echo ddd
cd C:\gsma\pythonWorkSpace\spider_monitor
set PYTHONPATH=%PYTHONPATH%;%cd%
set PYTHONIOENCODING=utf-8
cd ./monitor/service
python Service.py
