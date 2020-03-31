@echo off
chcp 65001
title Adobe Windows RPC Updater 업데이트 || Develop By. 화향
pushd "%~dp0"
echo 잠시만 기다리세요.. 업데이터의 종료를 기다리는 중 입니다.
timeout 8 > NUL
echo 업데이트를 마무리 하는 중 입니다. 잠시만 기다리세요..
echo 업데이트 완료 후 자동으로 코어 프로그램의 업데이트를 진행합니다.
del "%cd%\adoberpc_updater.exe"
move "%cd%\temp\adoberpc_updater.exe" "%cd%\adoberpc_updater.exe"
timeout 2 > NUL
echo 업데이터를 실행하는 중 입니다. 잠시만 기다리세요...
start /d "%cd%" /b adoberpc_updater.exe
echo 해당 배치 파일은 잠시 후 자동으로 종료됩니다.
timeout 2 > NUL
exit