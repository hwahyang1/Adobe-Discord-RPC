# -*- coding:utf-8 -*- 

"""
                  _       _            _____  _                       _   _____  _____   _____ 
         /\      | |     | |          |  __ \(_)                     | | |  __ \|  __ \ / ____|
        /  \   __| | ___ | |__   ___  | |  | |_ ___  ___ ___  _ __ __| | | |__) | |__) | |     
       / /\ \ / _` |/ _ \| '_ \ / _ \ | |  | | / __|/ __/ _ \| '__/ _` | |  _  /|  ___/| |     
      / ____ \ (_| | (_) | |_) |  __/ | |__| | \__ \ (_| (_) | | | (_| | | | \ \| |    | |____ 
     /_/    \_\__,_|\___/|_.__/ \___| |_____/|_|___/\___\___/|_|  \__,_| |_|  \_\_|     \_____|
 
    Ver. 1.0
    © 2017-2020 화향.
    Follow GPL-3.0
    Gtihub || https://github.com/hwahyang1/Adobe-Discord-RPC

    :: Program Core ::
"""

"""
    :: flow ::
    모듈검증 -> 버전검증 -> 실행검증 -> RPC 연결 -> 연결알림 -> 30초 간격으로 실행검증
"""

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

def goout(datetime = None):
    log("INFO", "Adobe Discord RPC가 종료됩니다.", datetime)
    exit()

try:
    from pypresence import Presence
    from plyer import notification
    import datetime, os, requests, sys, psutil, json, win32gui, win32process, time, pandas
except ModuleNotFoundError as e:
    if not (str(e) in 'plyer'):
        notification.notify(
            title='Adobe Discord RPC',
            message='모듈 불러오기에 실패했습니다.\n로그를 확인하세요.',
            app_name='Adobe Discord RPC',
            app_icon='icon_alpha.ico'
        )
    log("ERROR", "%s 모듈이 존재하지 않습니다." % (str(e).replace('No module named ', '')))
    goout()

def checkver():
    nowver = 1.0
    r = requests.get("https://cdn.hwahyang.space/adoberpc_ver.json")
    r = r.text
    data = json.loads(r)
    latest = float(data["ver"]) # 바보야 int 아니라고,,
    if latest > nowver: # 만약에 최신이 더 높다면,
        log("DEBUG", "새 버전 알림 발신. || 현재 : %s || 최신 : %s" % (nowver, latest), datetime)
        notification.notify(
            title='Adobe Discord RPC',
            message='Adobe Discord RPC가 가동되었습니다.\n새 버전이 있습니다.\nV%s (현재) -> V%s (최신)' % (nowver, latest),
            app_name='Adobe Discord RPC',
            app_icon='icon_alpha.ico'
        )
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

def get_process_info():
    for element in data:
        process_name = element['processName']
        for process in psutil.process_iter():
            process_info = process.as_dict(attrs=['pid', 'name'])
            if process_info['name'] == None: # 이거 대체 왜뜸
                pass
            elif process_info['name'].lower() in process_name:
                element['pid'] = process_info['pid']
                return element

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

if not (sys.platform in ['Windows', 'win32', 'cygwin']):
    # 타 OS에서 노티 돌아간다는 보장 없어서 알림 안띄움
    # 않이 근데 왠만해선 타 OS에서 돌릴 일은 없지 않나
    log("ERROR", "지원하지 않는 OS : %s" % (sys.platform))
    goout(datetime)

checkver()

try: # 애러나면 로그는 해야죠
    while True:
        # 죽을때까지 실행 검증 루프
        a = True
        while a: # 실행 없으면 15초 쉬었다 루프 다시. --> 30초로 변경.
            pinfo = get_process_info()
            if pinfo == None:
                log("DEBUG", "발견된 프로세스 없음", datetime)
                log("DEBUG", "30초 후 다시 시도..", datetime)
                time.sleep(30)
                continue
            window_title = get_title(pinfo['pid'])
            a = False # 루프 종료

        RPC = Presence(pinfo['appid'])

        try:
            RPC.connect()
        except Exception as e:
            log("ERROR", "디스코드와 연결하지 못했습니다.", datetime)
            log("ERROR", "디스코드가 켜져 있는지 확인 해 주세요.", datetime)
            log("DEBUG", "ERRINFO :: %s" % (e), datetime)
            notification.notify(
                title='Adobe Discord RPC',
                message='디스코드와 연결하지 못하였습니다.\n디스코드가 켜져 있는지 다시 한번 확인 해 주세요.\n30초 후 연결을 다시 시도합니다.',
                app_name='Adobe Discord RPC',
                app_icon='icon_alpha.ico'
            )
            goout(datetime)
        log("INFO", "성공적으로 디스코드와 연결 하였습니다!", datetime)
        
        dt = pandas.to_datetime(datetime.datetime.now())
        if pinfo['getver'] == 0:
            version = ''
        else:
            version = window_title.split(pinfo['publicName'])[1]
            version = version.split(pinfo['splitBy'])[0]

        filename = window_title.split(pinfo['splitBy'])[pinfo['splitIndex']]
        lmt = pinfo['largeText'].replace('%Ver%', version)
        lmt = lmt.replace('%Filename%', filename)
        smt = pinfo['smallText'].replace('%Filename%', filename)
        smt = smt.replace('%Ver%', version)
        b = True

        notification.notify(
            title='Adobe Discord RPC',
            message='성공적으로 디스코드와 연결했습니다.\n%s를 플레이 하게 됩니다.' % (pinfo['publicName']),
            app_name='Adobe Discord RPC',
            app_icon='icon_alpha.ico'
        )

        while b:
            try:
                rtn = RPC.update(
                    large_image='lg', large_text='프로그램 : %s' % (pinfo['publicName']),
                    small_image='sm_temp', small_text="파일명 : %s" %(filename),
                    details=lmt, state=smt,
                    start=int(time.mktime(dt.timetuple()))
                )
            except Exception as e:
                log("ERROR", "pypresence 갱신 실패... 30초 대기 : %s" % (e), datetime)
                notification.notify(
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

                new_pinfo = get_process_info()
                if new_pinfo == None:
                    # 프로세스 변동 1000000%
                    log("DEBUG", "PID 변동 확인. : %s -> Null" % (pinfo['pid']), datetime)
                    b = False
                    pass
                else:
                    # PID로 프로세스 변동 감지. 실행 유지중이면 PID 변경 될 이유 없음.
                    if pinfo['pid'] == new_pinfo['pid']:
                        # 변동 없어도 파일 변경될 가능성 있음
                        log("DEBUG", "PID 변동 없음. : %s" % (pinfo['pid']), datetime)
                        window_title = get_title(pinfo['pid'])
                        filename = window_title.split(pinfo['splitBy'])[pinfo['splitIndex']]
                        lmt = pinfo['largeText'].replace('%Ver%', version)
                        lmt = lmt.replace('%Filename%', filename)
                        smt = pinfo['smallText'].replace('%Filename%', filename)
                        smt = smt.replace('%Ver%', version)
                        pass
                    else:
                        log("DEBUG", "PID 변동 확인. : %s -> %s" % (pinfo['pid'], new_pinfo['pid']), datetime)
                        b = False
except KeyboardInterrupt:
    log("DEBUG", "콘솔 단에서 중지함.", datetime)
    goout()
except Exception as e:
    log("ERROR", "미정의 애러 : %s" % (e), datetime)
    goout()

# End of Code.