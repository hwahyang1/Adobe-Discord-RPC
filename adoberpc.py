# -*- coding:utf-8 -*- 

"""
                  _       _            _____  _                       _   _____  _____   _____ 
         /\      | |     | |          |  __ \(_)                     | | |  __ \|  __ \ / ____|
        /  \   __| | ___ | |__   ___  | |  | |_ ___  ___ ___  _ __ __| | | |__) | |__) | |     
       / /\ \ / _` |/ _ \| '_ \ / _ \ | |  | | / __|/ __/ _ \| '__/ _` | |  _  /|  ___/| |     
      / ____ \ (_| | (_) | |_) |  __/ | |__| | \__ \ (_| (_) | | | (_| | | | \ \| |    | |____ 
     /_/    \_\__,_|\___/|_.__/ \___| |_____/|_|___/\___\___/|_|  \__,_| |_|  \_\_|     \_____|
 
    Ver. 3.4
    © 2017-2020 화향.
    Follow GPL-3.0
    Gtihub || https://github.com/hwahyang1/Adobe-Discord-RPC

    :: Program Core ::
"""

if __name__ == "__main__" :
    def log(tpe, inf, datetime = None):
        if not os.path.isfile('./log.log'):
            open('./log.log', 'w').close()
        if datetime == None:
            prnt = "시간정보 없음 | %s | %s" % (tpe, inf)
        else:
            now = datetime.datetime.now()
            prnt = "%s-%02d-%02d %02d:%02d:%02d | %s | %s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, tpe, inf)
        f = open("./log.log", 'a', encoding='utf8')
        f.write(prnt+"\n")
        f.close()
        print(prnt)
    try:
        from pypresence import Presence
        import datetime, os, requests, sys, psutil, json, win32gui, win32process, time, pandas, plyer, re, win32ui, win32con, platform
    except ModuleNotFoundError as e:
        if not (str(e) in 'plyer'):
            plyer.notification.notify(
                title='Adobe Discord RPC',
                message='모듈 불러오기에 실패했습니다.\n로그를 확인하세요.',
                app_name='Adobe Discord RPC',
                app_icon='icon_alpha.ico'
            )
        log("ERROR", "%s 모듈이 존재하지 않습니다." % (str(e).replace('No module named ', '')))
        goout()

        
    try:
        os.remove('./stop.req')
    except FileNotFoundError:
        pass

    def goout(datetime = None):
        log("INFO", "Adobe Discord RPC가 종료됩니다.", datetime)
        #time.sleep(30)
        #os.system('adoberpc.exe')
        #exit()
        sys.exit()

    def checkver():
        # 20-03-23 방식 변경
        #          새 버전 알림 -> 새 버전 알림 후 업데이트 수락하면 업데이터 가동
        with open('programver.json', encoding='utf8') as f:
            data = json.load(f)
        nowver = data['ver']
        r = requests.get("https://cdn.adoberpc.hwahyang.space/adoberpc_ver.json")
        if r.status_code != 200:
            r = requests.get("https://cdn.hwahyang.space/adoberpc_ver.json")
        r = r.text
        data = json.loads(r)
        latest = float(data["ver"]) # 바보야 int 아니라고,,
        if latest > nowver: # 만약에 최신이 더 높다면,
            log("DEBUG", "새 버전 알림 발신. || 현재 : %s || 최신 : %s" % (nowver, latest), datetime)
            plyer.notification.notify(
                title='Adobe Discord RPC',
                message='Adobe Discord RPC가 가동되었습니다.\n새 버전이 있습니다.\nV%s (현재) -> V%s (최신)' % (nowver, latest),
                app_name='Adobe Discord RPC',
                app_icon='icon_alpha.ico'
            )
            res = win32ui.MessageBox("새 버전이 있습니다.\nV%s (현재) -> V%s (최신)\n업데이트를 진행할까요?" % (nowver, latest), "Adobe Discord RPC", win32con.MB_YESNO)
            if res == win32con.IDYES:
                os.system('start adoberpc_updater.exe')
                open("stop.req", 'w').close()
                goout()
        else:
            log("DEBUG", "버전 변동 없음. || 현재 : %s || 최신 : %s" % (nowver, latest), datetime)
            #notification.notify(
            #    title='Adobe Discord RPC',
            #    message='Adobe Discord RPC가 가동되었습니다.\n새 버전이 존재하지 않습니다.',
            #    app_name='Adobe Discord RPC',
            #    app_icon='icon_alpha.ico'
            #)

    with open('pinfo.json', encoding='utf8') as f:
        data = json.load(f)

    def get_title(pid):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        window_title = win32gui.GetWindowText(hwnds[-1])
        return window_title

    def get_info(programname):
        getp = lambda process: (list(p.info for p in filter((lambda p: p.info['name'] and p.info['name'] == process),list(psutil.process_iter(['pid','name','exe','status'])))))
        returns = getp(programname)

        if not returns: # 미친 이거 왜됨
            return [False]
        
        returns = returns[0]

        try:
            windowname = get_title(returns['pid'])
        except Exception as e:
            print(e)
            return [False]

        return [True, returns['name'], returns['pid'], windowname, returns['status'], returns['exe']]

    def get_process_info():
        for now_json in data:
            def_returned = get_info(now_json['processName'])
            if def_returned[0]:
                return def_returned + [now_json]
            else:
                continue

        return [False]

    def get_window_title(pid):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        window_title = win32gui.GetWindowText(hwnds[-1])
        return window_title

    if not (sys.platform in ['Windows', 'win32', 'cygwin']):
        # 않이 근데 왠만해선 타 OS에서 돌릴 일은 없지 않나
        log("ERROR", "지원하지 않는 OS : %s" % (sys.platform))
        goout(datetime)

    if int(platform.release()) < 7:
        log("ERROR", "지원하지 않는 Windows 버전 : %s" % (platform.release()))
        goout(datetime)

    checkver()

    try: # 애러나면 로그는 해야죠
        while True:
            # 죽을때까지 실행 검증 루프
            a = True
            while a: # 실행 없으면 15초 쉬었다 루프 다시. --> 30초로 변경.
                try:
                    pinfo = get_process_info()
                    if not pinfo[0]:
                        log("DEBUG", "발견된 프로세스 없음", datetime)
                        log("DEBUG", "30초 후 다시 시도..", datetime)
                        time.sleep(30)
                        continue
                    window_title = pinfo[3]
                    a = False # 루프 종료
                except IndexError as e:
                    log("ERROR", "정의 애러.. 10초 후 다시 시도 : %s" % (e), datetime)
                    time.sleep(10)

            RPC = Presence(pinfo[len(pinfo)-1]['appid'])

            try:
                RPC.connect()
            except Exception as e:
                log("ERROR", "디스코드와 연결하지 못했습니다.", datetime)
                log("ERROR", "디스코드가 켜져 있는지 확인 해 주세요.", datetime)
                log("DEBUG", "ERRINFO :: %s" % (e), datetime)
                plyer.notification.notify(
                    title='Adobe Discord RPC',
                    message='디스코드와 연결하지 못하였습니다.\n디스코드가 켜져 있는지 다시 한번 확인 해 주세요.\n30초 후 연결을 다시 시도합니다.',
                    app_name='Adobe Discord RPC',
                    app_icon='icon_alpha.ico'
                )
                goout(datetime)
            log("INFO", "성공적으로 디스코드와 연결 하였습니다!", datetime)
            
            dt = pandas.to_datetime(datetime.datetime.now())
            # -1은 미사용
            # 그 이상은 splitindex 용도로 사용함
            if pinfo[len(pinfo)-1]['getver'] == -1:
                version = ''
            else:
                path = pinfo[5].split(pinfo[len(pinfo)-1]['publicName'])[1]
                path = path.split('\\')[pinfo[len(pinfo)-1]['getver']]
                version = path.replace(" ", '')
                
            filename = window_title.split(pinfo[len(pinfo)-1]['splitBy'])[pinfo[len(pinfo)-1]['splitIndex']]
            lmt = pinfo[len(pinfo)-1]['largeText'].replace('%Ver%', version)
            lmt = lmt.replace('%Filename%', filename)
            smt = pinfo[len(pinfo)-1]['smallText'].replace('%Filename%', filename)
            smt = smt.replace('%Ver%', version)
            b = True

            plyer.notification.notify(
                title='Adobe Discord RPC',
                message='성공적으로 디스코드와 연결했습니다.\n%s를 플레이 하게 됩니다.' % (pinfo[len(pinfo)-1]['publicName']),
                app_name='Adobe Discord RPC',
                app_icon='icon_alpha.ico'
            )

            while b:
                # 20-04-25 코드 구조 대량으로 변경되어서 응답없음 여부 사용 안함
                """if not isresponding(pinfo['processName'].replace('.exe', ''), datetime):
                    # 응답없음은 10초 간격으로 체크해서 응답없음 풀리면 c = False 로 만듬
                    c = True
                    while c:
                        try:
                            rtn = RPC.update(
                                large_image='lg', large_text='프로그램 : %s' % (pinfo['publicName']),
                                small_image='sm_temp', small_text="파일명 : %s" %(filename),
                                details="응답없음", state="응답없음",
                                start=int(time.mktime(dt.timetuple()))
                            )
                        except Exception as e:
                            log("ERROR", "pypresence 갱신 실패... 10초 대기 : %s" % (e), datetime)
                            plyer.notification.notify(
                                title='Adobe Discord RPC',
                                message='RPC 갱신에 실패하였습니다.\n10초 후 다시 시도합니다.',
                                app_name='Adobe Discord RPC',
                                app_icon='icon_alpha.ico'
                            )
                            b = False
                            time.sleep(10)
                        else:
                            log("DEBUG", "pypresence 리턴 : %s" % (rtn), datetime)
                            time.sleep(10)

                            if not isresponding(pinfo['processName'].replace('.exe', ''), datetime):
                                pass
                            else:
                                # 정상실행 경우
                                # RPC.clear(pid=os.getpid())
                                c = False
                                pass
                else:"""
                try:
                    rtn = RPC.update(
                        large_image='lg', large_text='프로그램 : %s' % (pinfo[len(pinfo)-1]['publicName']),
                        small_image='sm_temp', small_text="Adobe Discord RPC",
                        details=lmt, state=smt,
                        start=int(time.mktime(dt.timetuple()))
                    )
                except Exception as e:
                    log("ERROR", "pypresence 갱신 실패... 30초 대기 : %s" % (e), datetime)
                    plyer.notification.notify(
                        title='Adobe Discord RPC',
                        message='RPC 갱신에 실패하였습니다.\n30초 후 다시 시도합니다.',
                        app_name='Adobe Discord RPC',
                        app_icon='icon_alpha.ico'
                    )
                    b = False
                    time.sleep(30)
                else:
                    log("DEBUG", "pypresence 리턴 : %s" % (rtn), datetime)
                    time.sleep(30)
                    #time.sleep(5) # 테스트용인데 왜 주석 안하고 배포한거야

                    try:
                        window_title = get_window_title(pinfo[2])
                        filename = window_title.split(pinfo[len(pinfo)-1]['splitBy'])[pinfo[len(pinfo)-1]['splitIndex']]
                        lmt = pinfo[len(pinfo)-1]['largeText'].replace('%Ver%', version)
                        lmt = lmt.replace('%Filename%', filename)
                        smt = pinfo[len(pinfo)-1]['smallText'].replace('%Filename%', filename)
                        smt = smt.replace('%Ver%', version)
                        pass
                    except IndexError as e:
                        # PID 변경 OR 프로그램 종료. 같은 PID 금방 다시 할당할 일 없음.
                        log("DEBUG", "PID 변동 OR 프로세스 종료. : %s -> %s" % (pinfo['pid'], e), datetime)
                        RPC.clear(pid=os.getpid())
                        b = False
    except KeyboardInterrupt:
        log("DEBUG", "콘솔 단에서 중지함.", datetime)
        goout()
    except Exception as e:
        log("ERROR", "미정의 애러 : %s" % (e), datetime)
        goout()

# End of Code.