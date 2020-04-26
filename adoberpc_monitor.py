# -*- coding:utf-8 -*- 

"""
                  _       _            _____  _                       _   _____  _____   _____ 
         /\      | |     | |          |  __ \(_)                     | | |  __ \|  __ \ / ____|
        /  \   __| | ___ | |__   ___  | |  | |_ ___  ___ ___  _ __ __| | | |__) | |__) | |     
       / /\ \ / _` |/ _ \| '_ \ / _ \ | |  | | / __|/ __/ _ \| '__/ _` | |  _  /|  ___/| |     
      / ____ \ (_| | (_) | |_) |  __/ | |__| | \__ \ (_| (_) | | | (_| | | | \ \| |    | |____ 
     /_/    \_\__,_|\___/|_.__/ \___| |_____/|_|___/\___\___/|_|  \__,_| |_|  \_\_|     \_____|
 
    Ver. M1.1
    © 2017-2020 화향.
    Follow GPL-3.0
    Gtihub || https://github.com/hwahyang1/Adobe-Discord-RPC

    :: System Monitor ::
"""

if __name__ == "__main__" :
    try:
        import datetime, os, sys, time, plyer, PySimpleGUIQt, webbrowser, psutil, win32gui, win32process, platform
    except ModuleNotFoundError as e:
        if not (str(e) in 'plyer'):
            plyer.notification.notify(
                title='Adobe Discord RPC',
                message='모듈 불러오기에 실패했습니다.\n로그를 확인하세요.',
                app_name='Adobe Discord RPC',
                app_icon='monitor.ico'
            )
        log("ERROR", "%s 모듈이 존재하지 않습니다." % (str(e).replace('No module named ', '')))
        goout()

    def log(tpe, inf, datetime = None):
        if not os.path.isfile('./monitor.log'):
            open('./monitor.log', 'w').close()
        if datetime == None:
            prnt = "시간정보 없음 | %s | %s" % (tpe, inf)
        else:
            now = datetime.datetime.now()
            prnt = "%s-%02d-%02d %02d:%02d:%02d | %s | %s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, tpe, inf)
        f = open("./monitor.log", 'a', encoding='utf8')
        f.write(prnt+"\n")
        f.close()
        print(prnt)

    def goout(datetime = None):
        log("INFO", "Adobe Discord RPC 모니터 종료.", datetime)
        #exit()
        sys.exit()

    if not (sys.platform in ['Windows', 'win32', 'cygwin']):
        log("ERROR", "지원하지 않는 OS : %s" % (sys.platform))
        goout(datetime)

    if int(platform.release()) < 7:
        log("ERROR", "지원하지 않는 Windows 버전 : %s" % (platform.release()))
        goout(datetime)

    log("DEBUG", "System info : %s %s v%s (%s)" % (platform.system(), platform.release(), platform.version(), platform.processor()), datetime)

    getp = lambda process: (list(p.info for p in filter((lambda p: p.info['name'] and p.info['name'] == process),list(psutil.process_iter(['pid','name','exe','status'])))))
    returns = getp('adoberpc_monitor.exe')

    if len(returns) > 3:
        goout(datetime)

    log("DEBUG", "모니터링 시작.", datetime)

    try:
        timecount = 0
        menu_def = ['File', ['Adobe Discord RPC Monitor', '프로그램 정보', '모니터링 종료']]
        tray = PySimpleGUIQt.SystemTray(menu=menu_def, filename='monitor.ico')

        # 15초 간격 -> 60초로 한다
        while True:
            menu_item = tray.Read(timeout=0)
            if not menu_item == "__TIMEOUT__":
                if menu_item == "모니터링 종료":
                    plyer.notification.notify(
                        title='Adobe Discord RPC Monitor',
                        message='모니터링을 종료합니다.\n메인 프로그램 종료는 별도로 진행 하셔야 합니다.',
                        app_name='Adobe Discord RPC Monitor',
                        app_icon='monitor.ico'
                    )
                    goout(datetime)
                if menu_item == "프로그램 정보":
                    webbrowser.open("https://github.com/hwahyang1/Adobe-Discord-RPC/#readme")
            timecount += 0.01
            
            if timecount >= 60:
                returns = getp('adoberpc.exe')

                if len(returns) == 0:
                    log("INFO", "프로그램 미가동.. 파일 확인중", datetime)
                    if os.path.isfile('stop.req'):
                        log("INFO", "가동 중지 요청 확인됨.", datetime)
                    else:
                        log("INFO", "가동 중지 요청 미확인.. 실행 시도중", datetime)
                        os.system('start /d "%cd%" /b adoberpc.exe')
                else:
                    log("INFO", "프로그램 가동 중", datetime)
                    try:
                        os.remove('stop.req')
                    except FileNotFoundError:
                        timecount = 0

                timecount = 0
            time.sleep(0.01)
    except KeyboardInterrupt:
        log("DEBUG", "콘솔 단에서 중지함.", datetime)
        goout(datetime)
    except Exception as e:
        log("ERROR", "미정의 애러 : %s" % (e), datetime)
        goout(datetime)

# End of code.