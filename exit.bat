@echo off
chcp 65001
title Adobe Windows RPC 종료 :: Develop By. 화향
echo 잠시만 기다리세요.. 곧 프로그램이 종료됩니다.
echo stop.req > stop.req
timeout 1 > NUL
taskkill /F /IM adoberpc.exe
taskkill /F /IM adoberpc_monitor.exe
timeout 1 > NUL
taskkill /F /IM adoberpc.exe
taskkill /F /IM adoberpc_monitor.exe
timeout 1 > NUL
taskkill /F /IM adoberpc.exe
taskkill /F /IM adoberpc_monitor.exe
taskkill /F /IM adoberpc.exe
taskkill /F /IM adoberpc_monitor.exe
taskkill /F /IM adoberpc.exe
taskkill /F /IM adoberpc_monitor.exe