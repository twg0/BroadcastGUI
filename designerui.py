import sys
import time
from PyQt5.QtCore import *
import asyncio

from PyQt5.QtWidgets import *
from PyQt5 import uic
import multiprocessing

form_class = uic.loadUiType("broadcast.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        self.ti_count = 5

        self.setupUi(self)

        self.mainFrame.raise_()
        self.loginFrame.raise_()

        self.name = ""
        self.phone = "01093701524"
        self.broadcastContents = []

        # 로그인 페이지
        self.warn_msg.setVisible(False)
        self.login_btn.pressed.connect(self.login_btn_pressed)
        self.login_btn.released.connect(self.login_btn_released)
        self.login_btn.clicked.connect(self.login_btn_clicked)

        # 메인 페이지
        self.emergency_btn.pressed.connect(self.emergency_btn_pressed)
        self.emergency_btn.released.connect(self.emergency_btn_released)
        self.emergency_btn.clicked.connect(self.emergency_btn_clicked)
        self.emer_cancel.clicked.connect(self.emer_cancel_btn_clicked)

        self.broadcastPlay_btn.pressed.connect(self.broadcastPlay_btn_pressed)
        self.broadcastPlay_btn.released.connect(self.broadcastPlay_btn_released)
        self.broadcastPlay_btn.clicked.connect(self.broadcastPlay_btn_clicked)
        self.play_cancel.clicked.connect(self.back_to_main)

        self.radio_btn.pressed.connect(self.radio_btn_pressed)
        self.radio_btn.released.connect(self.radio_btn_released)
        self.radio_btn.clicked.connect(self.radio_btn_clicked)
        self.radioClose_btn.clicked.connect(self.back_to_main)

        self.broadcastList_btn.pressed.connect(self.broadcastList_btn_pressed)
        self.broadcastList_btn.released.connect(self.broadcastList_btn_released)
        self.broadcastList_btn.clicked.connect(self.broadcastList_btn_clicked)
        self.listClose_btn.clicked.connect(self.back_to_main)

        # 긴급 호출 타이머
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)

        # 라디오
        self.Inc1.pressed.connect(self.Inc1_btn_pressed)
        self.Inc1.released.connect(self.Inc1_btn_released)
        self.Inc1.clicked.connect(self.Inc1_btn_clicked)

        self.inc_1.pressed.connect(self.inc_1_btn_pressed)
        self.inc_1.released.connect(self.inc_1_btn_released)
        self.inc_1.clicked.connect(self.inc_1_btn_clicked)

        self.dec1.pressed.connect(self.dec1_btn_pressed)
        self.dec1.released.connect(self.dec1_btn_released)
        self.dec1.clicked.connect(self.dec1_btn_clicked)

        self.dec_1.pressed.connect(self.dec_1_btn_pressed)
        self.dec_1.released.connect(self.dec_1_btn_released)
        self.dec_1.clicked.connect(self.dec_1_btn_clicked)

        self.freqInput_btn.pressed.connect(self.freqInput_pressed)
        self.freqInput_btn.released.connect(self.freqInput_released)
        self.freqInput_btn.clicked.connect(self.freqInput_clicked)

    # 메인 페이지
    def emergency_btn_pressed(self):
        self.emerFrame.raise_()
        self.emergency_btn.setStyleSheet("""background-color: #962321;
    border-style: outset;
    border-width: 2px;
    border-radius: 20px;
    border-color: beige;
    font: bold 20px;
	image:url(:/newPrefix/call.png);
	padding: 70px""")

    def emergency_btn_released(self):
        self.emergency_btn.setStyleSheet("""background-color: rgb(225, 49, 45);
	selection-background-color: rgb(255, 131, 131);
    border-style: outset;
    border-width: 2px;
    border-radius: 20px;
    border-color: beige;
    font: bold 20px;
	image:url(:/newPrefix/call.png);
	padding: 70px""")

    def emergency_btn_clicked(self):
        self.ti_count = 5
        self.mainFrame.setEnabled(False)
        self.countdown.setText(str(self.ti_count))
        self.timer.start()

    def emer_cancel_btn_clicked(self):
        self.timer.stop()
        self.mainFrame.raise_()
        self.ti_count = 5
        self.countdown.setText(str(self.ti_count))
        self.mainFrame.setEnabled(True)

    def broadcastPlay_btn_pressed(self):
        self.broadcastPlay_btn.setStyleSheet("""background-color: #963a1b;
    border-style: outset;
    border-width: 2px;
    border-radius: 20px;
    border-color: beige;
    font: bold 20px;
    min-width: 10em;
    padding: 5px;""")

    def broadcastPlay_btn_released(self):
        self.broadcastPlay_btn.setStyleSheet("""background-color: rgb(226, 90, 41);
    border-style: outset;
    border-width: 2px;
    border-radius: 20px;
    border-color: beige;
    font: bold 20px;
    min-width: 10em;
    padding: 5px;""")

    def broadcastPlay_btn_clicked(self):
        self.mainFrame.setEnabled(False)

    def radio_btn_pressed(self):
        self.radio_btn.setStyleSheet("""background-color: #163218;
	selection-background-color: rgb(255, 131, 131);
    border-style: outset;
    border-width: 2px;
    border-radius: 20px;
    border-color: beige;
    font: bold 20px;
	image: url(:/newPrefix/radio.png) 0 0 0 0 stretch stretch;
    min-width: 10em;
    padding: 40px;""")

    def radio_btn_released(self):
        self.radio_btn.setStyleSheet("""background-color: rgb(55, 125, 61);
	selection-background-color: rgb(255, 131, 131);
    border-style: outset;
    border-width: 2px;
    border-radius: 20px;
    border-color: beige;
    font: bold 20px;
	image: url(:/newPrefix/radio.png) 0 0 0 0 stretch stretch;
    min-width: 10em;
    padding: 40px;""")

    def radio_btn_clicked(self):
        self.mainFrame.setEnabled(False)

    def broadcastList_btn_pressed(self):
        self.broadcastList_btn.setStyleSheet("""background-color: #2f1632;
	border-style: outset;
    border-width: 2px;
    border-radius: 20px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 5px;""")

    def broadcastList_btn_released(self):
        self.broadcastList_btn.setStyleSheet("""background-color: rgb(101, 48, 106);
	border-style: outset;
    border-width: 2px;
    border-radius: 20px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 5px;""")

    def broadcastList_btn_clicked(self):
        self.mainFrame.setEnabled(False)

    def back_to_main(self):
        self.mainFrame.raise_()
        self.mainFrame.setEnabled(True)

    # 로그인
    def login_btn_clicked(self):
        phone_num = self.lineEdit_2.text()
        if phone_num.isnumeric():
            if self.phone == phone_num:
                self.mainFrame.raise_()
                self.warn_msg.setVisible(False)
            else:
                self.warn_msg.setVisible(True)
                self.warn_msg.setText("번호가 존재하지 않습니다")
        else :
            self.warn_msg.setVisible(True)
            self.warn_msg.setText("형식이 올바르지 않습니다")

    def login_btn_pressed(self):
        self.login_btn.setStyleSheet("""background-color: #6d8db4;
font: 18pt "휴먼둥근헤드라인";
border-radius: 20px""")

    def login_btn_released(self):
        self.login_btn.setStyleSheet("""background-color: rgb(155, 200, 255);
font: 18pt "휴먼둥근헤드라인";
border-radius: 20px""")

    # 타이머
    def timeout(self):
        i = self.time_count()
        if i == 0:
            self.timer.stop()
            self.mainFrame.raise_()
            self.ti_count = 5
            self.countdown.setText(str(self.ti_count))

    def time_count(self):
        self.ti_count -= 1
        self.countdown.setText(str(self.ti_count))
        return self.ti_count

    # 라디오
    def Inc1_btn_pressed(self):
        self.Inc1.setStyleSheet("""background-color: #b4ae95;""")

    def Inc1_btn_released(self):
        self.Inc1.setStyleSheet("""background-color: rgb(255, 247, 211);""")

    def inc_1_btn_pressed(self):
        self.inc_1.setStyleSheet("""background-color: #b4ae95;""")

    def inc_1_btn_released(self):
        self.inc_1.setStyleSheet("""background-color: rgb(255, 247, 211);""")

    def dec1_btn_pressed(self):
        self.dec1.setStyleSheet("""background-color: #b4ae95;""")

    def dec1_btn_released(self):
        self.dec1.setStyleSheet("""background-color: rgb(255, 247, 211);""")

    def dec_1_btn_pressed(self):
        self.dec_1.setStyleSheet("""background-color: #b4ae95;""")

    def dec_1_btn_released(self):
        self.dec_1.setStyleSheet("""background-color: rgb(255, 247, 211);""")

    def Inc1_btn_clicked(self):
        # 라디오 1주파수 증가
        pass

    def inc_1_btn_clicked(self):
        # 라디오 0.1주파수 증가
        pass

    def dec1_btn_clicked(self):
        # 라디오 1주파수 감소
        pass

    def dec_1_btn_clicked(self):
        # 라디오 0.1주파수 감소
        pass

    def freqInput_pressed(self):
        self.freqInput_btn.setStyleSheet("""background-color: #adadc8;""")

    def freqInput_released(self):
        self.freqInput_btn.setStyleSheet("""background-color: rgb(220, 220, 255);""")

    def freqInput_clicked(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
