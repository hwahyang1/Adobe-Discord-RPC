# -*- coding:utf-8 -*- 

"""
                  _       _            _____  _                       _   _____  _____   _____ 
         /\      | |     | |          |  __ \(_)                     | | |  __ \|  __ \ / ____|
        /  \   __| | ___ | |__   ___  | |  | |_ ___  ___ ___  _ __ __| | | |__) | |__) | |     
       / /\ \ / _` |/ _ \| '_ \ / _ \ | |  | | / __|/ __/ _ \| '__/ _` | |  _  /|  ___/| |     
      / ____ \ (_| | (_) | |_) |  __/ | |__| | \__ \ (_| (_) | | | (_| | | | \ \| |    | |____ 
     /_/    \_\__,_|\___/|_.__/ \___| |_____/|_|___/\___\___/|_|  \__,_| |_|  \_\_|     \_____|
 
    Ver. U1.2
    © 2017-2020 화향.
    Follow GPL-3.0
    Gtihub || https://github.com/hwahyang1/Adobe-Discord-RPC

    :: Program Updater ::

    Form implementation generated from reading ui file 'update_dialog.ui'

    Created by: PyQt5 UI code generator 5.14.1
"""

updater = 1.2
site = "https://cdn.adoberpc.hwahyang.space/"

if __name__ == "__main__" :
    def perform_log(tpe, inf, datetime = None):
        if not os.path.isfile('./updater.log'):
            open('./updater.log', 'w').close()
        if datetime == None:
            prnt = "시간정보 없음 | %s | %s" % (tpe, inf)
        else:
            now = datetime.datetime.now()
            prnt = "%s-%02d-%02d %02d:%02d:%02d | %s | %s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, tpe, inf)
        f = open("./updater.log", 'a', encoding='utf8')
        f.write(prnt+"\n")
        f.close()
        print(prnt)

    try:
        from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
        import zipfile, hashlib, datetime, os, requests, sys, win32ui, json, time, urllib.request, shutil, webbrowser, psutil
    except ModuleNotFoundError as e:
        perform_log("ERROR", "%s 모듈이 존재하지 않습니다." % (str(e).replace('No module named ', '')))
        goout()

    def goout(datetime = None):
        try:
            os.remove('stop.req')
        except FileNotFoundError:
            asdf = 0
        perform_log("INFO", "Adobe Discord RPC 업데이터 종료.", datetime)
        #exit()
        sys.exit()

    def increase_percent(ui, current, end):
        nowv = current
        a = True
        while a:
            nowv += 1
            ui.progressBar.setValue(nowv)
            if nowv == end:
                a = False
            else:
                time.sleep(0.05)
            pass

    def change_logs(ui, log, target):
        _translate = QtCore.QCoreApplication.translate
        log = log + target + "\n"
        ui.textBrowser.setText(_translate("Dialog", log))
        ui.textBrowser.verticalScrollBar().setSliderPosition(200)
        perform_log("INFO", target, datetime)
        return log

    class Ui_Dialog(object):
        def setupUi(self, Dialog):
            Dialog.setObjectName("Adobe Discord RPC Updater Dialog")
            Dialog.resize(561, 229)
            Dialog.setMinimumSize(QtCore.QSize(561, 229))
            Dialog.setMaximumSize(QtCore.QSize(561, 229))
            Dialog.setStyleSheet("alternate-background-color: rgb(255, 255, 255);")
            Dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
            Dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
            self.progressBar = QtWidgets.QProgressBar(Dialog)
            self.progressBar.setGeometry(QtCore.QRect(20, 40, 531, 23))
            self.progressBar.setProperty("value", 0)
            self.progressBar.setObjectName("progressBar")
            self.label = QtWidgets.QLabel(Dialog)
            self.label.setGeometry(QtCore.QRect(80, 10, 391, 20))
            font = QtGui.QFont()
            font.setPointSize(15)
            self.label.setFont(font)
            self.label.setObjectName("label")
            self.textBrowser = QtWidgets.QTextBrowser(Dialog)
            self.textBrowser.setGeometry(QtCore.QRect(20, 80, 521, 131))
            self.textBrowser.setObjectName("textBrowser")

            self.retranslateUi(Dialog)
            QtCore.QMetaObject.connectSlotsByName(Dialog)

        def retranslateUi(self, Dialog):
            _translate = QtCore.QCoreApplication.translate
            Dialog.setWindowTitle(_translate("Adobe Discord RPC Updater", "Adobe Discord RPC Updater"))
            Dialog.setWindowIcon(QtGui.QIcon('update.ico'))
            self.progressBar.setFormat(_translate("Dialog", "%p%"))
            self.label.setText(_translate("Dialog", "                업데이트 준비중..."))

        def runScript(self):
            log = change_logs(ui, "", "Adobe Discord RPC Updater Ver. U%s\nDevelop By. 화향\nUpdater Icon Design By. 화향, Tilto\n" % (updater))

            if not os.path.isdir('./temp'):
                os.makedirs('./temp')
            with open('programver.json', encoding='utf8') as f:
                data = json.load(f)
            nowver = data['ver']

            # 파베 리밋 터졌는지 확인
            # 파베 -> 개인서버 순으로 시도함.
            r = requests.get(site)
            if r.status_code != 404: # index 안해놔서 404가 맞음!
                usest = "https://cdn.hwahyang.space/"
            else:
                usest = site

            # 업데이터 확인
            r = requests.get("%slatest/installer.json" % (usest))
            if r.status_code != 200:
                self.label.setText("                 업데이트 취소됨.")
                ui.progressBar.setValue(100)
                log = change_logs(ui, log, "예기치 못한 문제가 발생했습니다.\n동일한 문제가 지속적으로 발생되면, update.log 파일과 함께 개발자에게 알려주세요.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다.")
                perform_log("ERROR", "lookin' as server down! : %s" % (r.status_code), datetime)
                QtTest.QTest.qWait(10000)
                goout(datetime)
            r = r.text
            data = json.loads(r)
            latest = float(data["latest"])
            if latest > updater:
                perform_log("DEBUG", "업데이터 버전 변동 있음. || 현재 : %s || 최신 : %s" % (updater, latest), datetime)
                self.label.setText("                 업데이트 취소됨.")
                log = change_logs(ui, log, "업데이터의 업데이트를 진행합니다.\n\n업데이트 완료 후에는 자동으로 메인 프로그램 업데이트를 진행합니다.")
                QtTest.QTest.qWait(2000)

                perform_log("DEBUG", "다운로드 시작 : %slatest/%s" % (usest, data['file']['name']), datetime)

                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)
                try:
                    urllib.request.urlretrieve("%slatest/%s" % (usest, data['file']['name']), "./temp/adoberpc_updater.exe")
                except urllib.error.HTTPError as e:
                    log = change_logs(ui, log, "예기치 못한 문제가 발생했습니다.\n동일한 문제가 지속적으로 발생되면, update.log 파일과 함께 개발자에게 알려주세요.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다.")
                    perform_log("ERROR", "lookin' as server down! : %s" % (e), datetime)
                    QtTest.QTest.qWait(10000)
                    goout(datetime)

                perform_log("DEBUG", "다운로드 완료", datetime)
                perform_log("DEBUG", "파일의 무결성을 검사중", datetime)

                with open('./temp/adoberpc_updater.exe', 'rb') as f:
                    zipall = f.read()
                
                if hashlib.md5(zipall).hexdigest().lower() != data['file']['hash'].lower():
                    log = change_logs(ui, log, "예기치 못한 문제가 발생했습니다.\n동일한 문제가 지속적으로 발생되면, update.log 파일과 함께 개발자에게 알려주세요.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다.")
                    perform_log("ERROR", "WTF? : MD5 -> %s :vs: %s" % (hashlib.md5(zipall).hexdigest().lower(), data['file']['hash'].lower()), datetime)
                    QtTest.QTest.qWait(10000)
                    goout(datetime)

                perform_log("DEBUG", "파일의 무결성 확인됨.", datetime)

                QtTest.QTest.qWait(2000)
                log = change_logs(ui, log, "\n\n\n배치 파일로 업데이트를 이어서 진행합니다.\n관리자 권한을 묻는 창이 나오면 '예'를 눌러주세요.")
                QtTest.QTest.qWait(2000)
                os.system("start moveeeeeeeeee.lnk")
                QtTest.QTest.qWait(3000)
                goout(datetime)
            else:
                perform_log("DEBUG", "업데이터 버전 변동 없음. || 현재 : %s || 최신 : %s" % (nowver, latest), datetime)
                log = change_logs(ui, log, "업데이터가 최신 버전(U%s)입니다." % (updater))

            # 코어 확인
            r = requests.get("%slatest/info.json" % (usest))
            if r.status_code != 200:
                self.label.setText("                 업데이트 취소됨.")
                ui.progressBar.setValue(100)
                log = change_logs(ui, log, "예기치 못한 문제가 발생했습니다.\n동일한 문제가 지속적으로 발생되면, update.log 파일과 함께 개발자에게 알려주세요.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다.")
                perform_log("ERROR", "lookin' as server down! : %s" % (r.status_code), datetime)
                QtTest.QTest.qWait(10000)
                goout(datetime)
            r = r.text
            data = json.loads(r)
            latest = float(data["nowver"])
            if latest > nowver:
                perform_log("DEBUG", "코어 버전 변동 있음. || 현재 : %s || 최신 : %s" % (nowver, latest), datetime)
            else:
                perform_log("DEBUG", "코어 버전 변동 없음. || 현재 : %s || 최신 : %s" % (nowver, latest), datetime)
                self.label.setText("                 업데이트 취소됨.")
                ui.progressBar.setValue(100)
                log = change_logs(ui, log, "이미 최신버전(V%s)을 사용 중입니다.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다." % (latest))
                QtTest.QTest.qWait(10000)
                goout(datetime)

            log = change_logs(ui, log, "현재 버전 : V%s\n최신 버전 : V%s" % (nowver, latest))

            if data['installer'] == False or float(data['minver']) == nowver:
                log = change_logs(ui, log, "현재 버전은 직접 설치 파일을 다운 받아서 실행하셔야 합니다.\nGithub 페이지를 자동으로 실행합니다.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다.")
                webbrowser.open("https://github.com/hwahyang1/Adobe-Discord-RPC/releases")
                QtTest.QTest.qWait(10000)
                goout(datetime)

            QtTest.QTest.qWait(1000)
            log = change_logs(ui, log, "메인 프로그램 실행 여부를 체크합니다.. 잠시만 기다려 주세요")
            QtTest.QTest.qWait(2000)

            getp = lambda process: (list(p.info for p in filter((lambda p: p.info['name'] and p.info['name'] == process),list(psutil.process_iter(['pid','name','exe','status'])))))
            returns01 = getp('adoberpc_monitor.exe')
            returns02 = getp('adoberpc.exe')

            QtTest.QTest.qWait(800)

            if len(returns01) == 0 and len(returns02) == 0:
                log = change_logs(ui, log, "프로그램이 실행되지 않고 있습니다.\n프로그램 종료 절차 없이 다운로드를 시작합니다.")
            else:
                log = change_logs(ui, log, "프로그램이 실행 중입니다.\n프로그램 종료를 시도합니다.")
                QtTest.QTest.qWait(800)
                log = change_logs(ui, log, "관리자 권한을 묻는 메시지가 나오면 '예'를 눌러주세요.")
                QtTest.QTest.qWait(1000)
                os.system('exit.lnk')
                log = change_logs(ui, log, "종료 딜레이를 감안하여 10초 대기...")
                QtTest.QTest.qWait(8000)

            QtTest.QTest.qWait(2000)

            log = change_logs(ui, log, "정보 읽는 중..")
            increase_percent(ui, 0, 8)
            r = requests.get("%slatest/info.json" % (usest))
            r = r.text
            data = json.loads(r)
            QtTest.QTest.qWait(1500)
            if data['ver'] == latest:
                ui.label.setText("               업데이트 다운로드 중...")
                log = change_logs(ui, log, "V%s 버전 다운로드를 시작합니다." % (latest))
                perform_log("DEBUG", "다운로드 시작 : %s%s" % (usest, data['down']), datetime)
                increase_percent(ui, 8, 20)

                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)
                try:
                    urllib.request.urlretrieve("%s%s" % (usest, data['down']), "./temp/Adoberpc_latest.tmp")
                except urllib.error.HTTPError as e:
                    self.label.setText("                 업데이트 취소됨.")
                    ui.progressBar.setValue(100)
                    log = change_logs(ui, log, "예기치 못한 문제가 발생했습니다.\n동일한 문제가 지속적으로 발생되면, update.log 파일과 함께 개발자에게 알려주세요.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다.")
                    perform_log("ERROR", "lookin' as server down! : %s" % (e), datetime)
                    QtTest.QTest.qWait(10000)
                    goout(datetime)

                ui.label.setText("                업데이트 다운로드 완료")
                log = change_logs(ui, log, "다운로드가 완료되었습니다.")
                increase_percent(ui, 20, 45)
                QtTest.QTest.qWait(1500)
                ui.label.setText("               업데이트 파일 확인중...")
                log = change_logs(ui, log, "파일의 무결성을 검사합니다.")

                with open('./temp/Adoberpc_latest.tmp', 'rb') as f:
                    zipall = f.read()
                
                if hashlib.md5(zipall).hexdigest().lower() != data['hash']['mainhash'].lower() or hashlib.sha1(zipall).hexdigest().lower() != data['hash']['subhash'].lower():
                    self.label.setText("                 업데이트 취소됨.")
                    ui.progressBar.setValue(100)
                    log = change_logs(ui, log, "예기치 못한 문제가 발생했습니다.\n동일한 문제가 지속적으로 발생되면, update.log 파일과 함께 개발자에게 알려주세요.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다.")
                    perform_log("ERROR", "WTF? : MD5 -> %s :vs: %s || SHA-1 %s :vs: %s" % (hashlib.md5(zipall).hexdigest().lower(), data['hash']['mainhash'].lower(), hashlib.sha1(zipall).hexdigest().lower(), data['hash']['subhash'].lower()), datetime)
                    QtTest.QTest.qWait(10000)
                    goout(datetime)

                QtTest.QTest.qWait(2000)
                ui.label.setText("              업데이트 파일 확인 완료")
                log = change_logs(ui, log, "파일의 무결성을 확인하였습니다.")
                increase_percent(ui, 45, 50)
                QtTest.QTest.qWait(1500)

                ui.label.setText("                  업데이트 적용 중...")
                log = change_logs(ui, log, "임시 폴더에 압축 풀기를 시작합니다.")

                target_zip = zipfile.ZipFile('./temp/Adoberpc_latest.tmp')
                target_zip.extractall('./temp/')
                target_zip.close()

                QtTest.QTest.qWait(1000)
                log = change_logs(ui, log, "임시 폴더에 압축 풀기를 완료했습니다.")
                increase_percent(ui, 50, 68)
                
                QtTest.QTest.qWait(2000)
                log = change_logs(ui, log, "파일을 프로그램 폴더로 이동하고 있습니다.")

                for nowfilename in target_zip.namelist():
                    shutil.move('./temp/%s' % (nowfilename), './%s'% (nowfilename))

                QtTest.QTest.qWait(2000)
                ui.label.setText("                  업데이트 적용 완료")
                log = change_logs(ui, log, "파일을 성공적으로 이동했습니다.")
                increase_percent(ui, 68, 100)

                log = change_logs(ui, log, "임시 폴더 삭제 중...")
                QtTest.QTest.qWait(2000)

                try:
                    os.remove('./stop.req')
                except FileNotFoundError:
                    pass
                shutil.rmtree('./temp')

                QtTest.QTest.qWait(1800)
                ui.label.setText("     프로그램이 곧 자동으로 실행됩니다.")
                log = change_logs(ui, log, "Adobe Discord RPC를 실행하고 있습니다.\n\n해당 업데이터는 10초 뒤 자동으로 종료됩니다.")
                os.system('startup.bat') # 아 start.bat 짜피 죽어서 이케해놨구나
                QtTest.QTest.qWait(10000)
                goout(datetime)
            else:
                self.label.setText("                 업데이트 취소됨.")
                ui.progressBar.setValue(100)
                log = change_logs(ui, log, "예기치 못한 문제가 발생했습니다.\n동일한 문제가 지속적으로 발생되면, update.log 파일과 함께 개발자에게 알려주세요.\n\n해당 프로그램은 10초 뒤 자동으로 종료됩니다.")
                perform_log("ERROR", "WTF? : data on public : %s || data on latest : %s" % (latest, data['ver']), datetime)
                QtTest.QTest.qWait(10000)
                goout(datetime)

    try:
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        ui.runScript()
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        perform_log("DEBUG", "콘솔 단에서 중지함.", datetime)
        goout(datetime)
    except Exception as e:
        perform_log("ERROR", "미정의 애러 : %s" % (e), datetime)
        goout(datetime)

# End of Code.