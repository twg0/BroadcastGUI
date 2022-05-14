import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import multiprocessing

form_class = uic.loadUiType("broadcast.ui")[0]
name = ""
phone = "01093701524"
broadcastContents = []


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.mainFrame.raise_()

        self.emergency_btn.pressed.connect(self.emergency_btn_pressed)
        self.emergency_btn.released.connect(self.emergency_btn_released)
        self.emergency_btn.clicked.connect(self.emergency_btn_clicked)
        self.emer_cancel.clicked.connect(self.back_to_main)

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

    def emergency_btn_pressed(self):
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
        self.mainFrame.setEnabled(False)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()