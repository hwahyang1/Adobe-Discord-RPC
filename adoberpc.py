# -*- coding:utf-8 -*- 

"""
                  _       _            _____  _                       _   _____  _____   _____ 
         /\      | |     | |          |  __ \(_)                     | | |  __ \|  __ \ / ____|
        /  \   __| | ___ | |__   ___  | |  | |_ ___  ___ ___  _ __ __| | | |__) | |__) | |     
       / /\ \ / _` |/ _ \| '_ \ / _ \ | |  | | / __|/ __/ _ \| '__/ _` | |  _  /|  ___/| |     
      / ____ \ (_| | (_) | |_) |  __/ | |__| | \__ \ (_| (_) | | | (_| | | | \ \| |    | |____ 
     /_/    \_\__,_|\___/|_.__/ \___| |_____/|_|___/\___\___/|_|  \__,_| |_|  \_\_|     \_____|
 
    Ver. 3.2
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
        import datetime, os, requests, sys, psutil, json, win32gui, win32process, time, pandas, plyer, subprocess, re, win32ui, win32con
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
        print("A")

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

    def get_process_info():
        #for element in data:
        #    process_name = element['processName']
        #    for process in psutil.process_iter():
        #        process_info = process.as_dict(attrs=['pid', 'name'])
        #        if process_info['name'] == None: # 이거 대체 왜뜸
        #            pass
        #        elif process_info['name'].lower() in process_name:
        #            element['pid'] = process_info['pid']
        #            return element
        # 20-03-22 Tasklist를 반복해서 돌리는 것으로 대체. 반복 횟수 적어서 CPU 소모 적을듯
        # 20-03-23 CPU 소모 적기는 개뿔 똑같네 다른 방법 찾아야할듯
        for now_json in data:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            fd_popen = subprocess.Popen(["powershell.exe", "tasklist /FI 'ImageName eq %s' /v /fo List" % (now_json['processName'])], stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=si).stdout
            resp = fd_popen.read().strip()
            fd_popen.close()
            try:
                resp = resp.decode("utf-8")
            except UnicodeDecodeError:
                resp = resp.decode("ansi") # Fucking ANSI...
            
            #print(resp)
            if resp == '' or resp.startswith('INFO') or resp.startswith('정보'): # 왜 두가지야
                #time.sleep(0.1)
                pass
            else:
                pidsplit = resp.split("\n")[1]
                pid = re.findall(r'\d+', pidsplit)
                wtsplit = resp.split("\n")[8]
                wt = wtsplit.split(":")[1:]
                wt = ':'.join(wt)
                return_target = json.loads(str(now_json).replace("\'", "\""))
                return_target.update({"pid": int(pid[0]), "window_title": wt})
                return return_target
    
    def get_window_title(pid):
        # 구현하기 귀찮았음,,
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        window_title = win32gui.GetWindowText(hwnds[-1])
        return window_title


    def get_version(pinfo):
        """
            CommandLine
            "C:\Program Files\Adobe\Adobe Photoshop 2020\Photoshop.exe"
        """
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        fd_popen = subprocess.Popen(["powershell.exe", "wmic process where \"ProcessID=%s\" get CommandLine" % (pinfo['pid'])], stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=si).stdout
        path_all = fd_popen.read().strip()
        fd_popen.close()
        try:
            path_all = path_all.decode("utf-8")
        except UnicodeDecodeError:
            path_all = path_all.decode("ansi")
        path = path_all.split(pinfo['publicName'])[1]
        path = path.split('\\')[0]
        path = path.replace(" ", '')
        return path

    def isresponding(name, datetime):
        # 20-03-19 이거 응답없음이면 아무것도 반환 안하는데 글케 되면 파일안생김 그거 이용하면 될듯
        #subprocess.Popen(["powershell.exe", "Get-Process %s | Where-Object {$_.Responding -eq $true} | tee-Object -file '%s/responding.txt'" % (name, os.getcwd())])
        #time.sleep(1.5)
        #if os.path.isfile("responding.txt"):
        #    #data = open("responding.txt", 'r', encoding='utf8').read()
        #    #log("DEBUG", "파워셀 리턴 : %s" % (data), datetime)
        #    log("DEBUG", "responding.txt 파일 감지됨.", datetime)
        #    try:
        #        os.remove("responding.txt")
        #    except Exception as e:
        #        log("ERROR", "(아마도) 예상했던 오류 : %s" % (e), datetime)
        #        time.sleep(0.5)
        #        os.remove("responding.txt")
        #    return True
        #    #return False # RPC 테스트용 리턴
        #else: 
        #    log("DEBUG", "responding.txt 파일 미감지.", datetime)
        #    return False
        # 20-03-22 망할 나 왜 이런 쉬운거 두고 멀리 돌아갔냐 미치겠네 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ
        fd_popen = subprocess.Popen(["powershell.exe", "Get-Process %s | Where-Object {$_.Responding -eq $true}" % (name)], stdout=subprocess.PIPE).stdout
        data = fd_popen.read().strip()
        fd_popen.close()
        """
            running : 
            b'Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName                                                  
            -------  ------    -----      -----     ------     --  -- -----------                                                  
               4827      52   620552     570076      17.20  16176   9 rabiribi'


            not responding : 
            b''


            not running : 
            b'Get-Process : Cannot find a process with the name "rabiribi". Verify the process name and call the cmdlet again.
            At line:1 char:1
            + Get-Process rabiribi | Where-Object {$_.Responding -eq $true}
            + ~~~~~~~~~~~~~~~~~~~~
                + CategoryInfo          : ObjectNotFound: (rabiribi:String) [Get-Process], ProcessCommandException
                    + FullyQualifiedErrorId : NoProcessFoundForGivenName,Microsoft.PowerShell.Commands.GetProcessCommand'
        """
        if data == b'': # case 응답없음
            return False
        else: # 실행 안되면 여기 구문까지 올 일도 없음
            return True

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
                try:
                    pinfo = get_process_info()
                    if pinfo == None:
                        log("DEBUG", "발견된 프로세스 없음", datetime)
                        log("DEBUG", "30초 후 다시 시도..", datetime)
                        time.sleep(30)
                        continue
                    window_title = pinfo['window_title']
                    a = False # 루프 종료
                except IndexError as e:
                    log("ERROR", "정의 애러.. 10초 후 다시 시도 : %s" % (e), datetime)
                    time.sleep(10)

            RPC = Presence(pinfo['appid'])

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
            if pinfo['getver'] == -1:
                version = ''
            else:
                # 이거 버전 파일 폴더 Path로 가져오는 방식 변경 예정.
                version = get_version(pinfo)

            filename = window_title.split(pinfo['splitBy'])[pinfo['splitIndex']]
            lmt = pinfo['largeText'].replace('%Ver%', version)
            lmt = lmt.replace('%Filename%', filename)
            smt = pinfo['smallText'].replace('%Filename%', filename)
            smt = smt.replace('%Ver%', version)
            b = True

            plyer.notification.notify(
                title='Adobe Discord RPC',
                message='성공적으로 디스코드와 연결했습니다.\n%s를 플레이 하게 됩니다.' % (pinfo['publicName']),
                app_name='Adobe Discord RPC',
                app_icon='icon_alpha.ico'
            )

            while b:
                #if not isresponding(pinfo['processName'].replace('.exe', ''), datetime): # 20-03-21 2일뒤에 생각 해 보니까 이거 생각보다 위험함. 방식 바꿔야할듯
                #    pass # 나중에,,,,
                #if False:
                #    pass
                # 20-03-22 방식 바꿔서 1도 안 위험함. 가자
                if not isresponding(pinfo['processName'].replace('.exe', ''), datetime):
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
                else:
                    try:
                        rtn = RPC.update(
                            large_image='lg', large_text='프로그램 : %s' % (pinfo['publicName']),
                            small_image='sm_temp', small_text="파일명 : %s" %(filename),
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
                            window_title = get_window_title(pinfo['pid'])
                            filename = window_title.split(pinfo['splitBy'])[pinfo['splitIndex']]
                            lmt = pinfo['largeText'].replace('%Ver%', version)
                            lmt = lmt.replace('%Filename%', filename)
                            smt = pinfo['smallText'].replace('%Filename%', filename)
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
    #except Exception as e:
    #    log("ERROR", "미정의 애러 : %s" % (e), datetime)
    #    goout()

# End of Code.