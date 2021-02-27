# 파이썬에서 키움증권의 클래스를 사용하려면 PyQt의 QAxWidget 클래스를 사용해 인스턴스를 생성해야 합니다. 키움증권에서 제공하는 클래스는 각각 고유의 CLSID 또는 ProgID를 가지는데 해당 값을 QAxWidget 클래스의 생성자로 전달하면 인스턴스가 생성됩니다.
# 키움증권의 개발 가이드를 참조하면 CLSID는 {A1574A0D-6BFA-4BD7-9020-DED88711818D} 임을 알 수 있고, 이를 윈도우 레지스트리 편집기를 통해 검색하면 ProgID는 그림 12.30과 같이 'KHOPENAPI.KHOpenAPICtrl.1'임을 알 수 있습니다.

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

mainform_class = uic.loadUiType("C:/98_Git/KJS_Project/Trading/tradingUI.ui")[0]
# ================================================================================================
# Method 사용하는 방법 기본꼴 (SetInputValue 라는 Method를 예시로...)
# self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
# 1. 앞에 self.kiwwom.dynamicCall 불이고 ("Method 이름(arg 타입 선언)", "arg") 꼴로 사용
# 2. BSTR은 str이라고 생각하면 댐
# ================================================================================================


class MyWindow(QMainWindow, mainform_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # QAxBase::setControl: requested control KHOPENAPI.KHOpenAPICtrl.1 could not be instantiated
        # Python이 32bit 환경이 아니라서 발생
        # https://lazyquant.tistory.com/5
        # $ conda activate KJS_vir_env
        # $ set CONDA_32BIT=1
        # To deactivate an active environment, use
        # $ conda deactivate

        # designer
        self.ob_btn_login.clicked.connect(self.btn_login_clicked)
        self.ob_btn_checkstate.clicked.connect(self.btn_checkstate_clicked)
        self.ob_btn_check.clicked.connect(self.btn_check_clicked)
        self.ob_btn_code.clicked.connect(self.btn_code_clicked)
        
        self.ob_textEdit_codeinfo.setEnabled(False)
        
        self.ob_listWidget_codename.setAlternatingRowColors(True)
        self.ob_listWidget_codename.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.ob_checkBox_sort.stateChanged.connect(self.chk_checkbox)

        # openapi
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        
        # global variable PyQt에서 global처럼 쓰기위한 처리 (그냥 global쓰면 main loop돌 때 사라짐)
        self.login_rev = 0
        self.checkBox_sort_on = 0

    # push button's shorcut can set in designer
    def btn_login_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")

    def event_connect(self, err_code):
        if err_code == 0:
            show_popup(self, "LoginDiag", "Connected!")
            self.login_rev = 1
    
    def btn_checkstate_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")

    def btn_check_clicked(self):
        self.ob_textEdit_codeinfo.clear()

        if self.login_rev == 0:
            show_popup(self, "LoginDiag", "로그인 후 이용해 주세용!")
        else:
            code = self.ob_lineEdit.text()
            self.ob_textEdit_codeinfo.append("종목코드 : " + code)

            # Input from API
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
            # Output from API
            self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")
    
    def btn_code_clicked(self):
        self.ob_listWidget_codename.clear()
        if self.login_rev == 0:
            show_popup(self, "LoginDiag", "로그인 후 이용해 주세용!")
        else:    
            if self.checkBox_sort_on == 0:
                ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
                kospi_code_list = ret.split(';')
                kospi_code_name_list = []

                for x in kospi_code_list:
                    name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
                    kospi_code_name_list.append(name + " : " + x)
                
                del kospi_code_name_list[-1]
                kospi_code_name_list.sort()
                self.ob_listWidget_codename.addItems(kospi_code_name_list)
            else:
                ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
                kospi_code_list = ret.split(';')
                kospi_code_name_list = []

                for x in kospi_code_list:
                    name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
                    kospi_code_name_list.append(x + " : " + name)
                
                del kospi_code_name_list[-1]
                self.ob_listWidget_codename.addItems(kospi_code_name_list)

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":    # 이게 모냐면... KOA들어가면 TR목록에 opt번호들 있음 그거임!
            # opt10001 Output에 원하는 데이터 eg.종목명,거래량,결산월 ... 골라서 CommGetData로 받아올 수 있음! 선택 가능 마치 PER 내가 추가 한거처럼!
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            per = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "PER")
            self.ob_textEdit_codeinfo.append("종목명: " + name.strip())
            self.ob_textEdit_codeinfo.append("거래량: " + volume.strip())
            self.ob_textEdit_codeinfo.append("PER: " + per.strip())

    def chk_checkbox(self):
        if self.ob_checkBox_sort.isChecked(): self.checkBox_sort_on = 1
        else : self.checkBox_sort_on = 0

# 얘는 Main window가 아니고 다른 Window 띄우는거라 다른 MainWindow 함수 밖에 놔둬야 함!
def show_popup(self, title: str, content: str):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(content)
    msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
    result = msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()