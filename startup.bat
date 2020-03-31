@echo off
chcp 65001
title Adobe Windows RPC 실행 :: Develop By. 화향
pushd "%~dp0"
echo 잠시만 기다리세요.. 곧 프로그램이 실행됩니다.
start /d "%cd%" /b adoberpc_monitor.exe
exit