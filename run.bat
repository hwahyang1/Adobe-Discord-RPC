@echo off
chcp 65001
:main
.\python376\python.exe adoberpc.py
if exist stop.req (
    del stop.req
    exit
)
timeout 15 > NUL
goto main