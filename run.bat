@echo off
chcp 65001
:main
adoberpc.exe
if exist stop.req (
    del stop.req
    exit
)
timeout 15 > NUL
goto main