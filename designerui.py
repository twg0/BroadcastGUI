import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtWidgets, QtCore
import paho.mqtt.client as mqtt
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

        self.radioClose_btn.pressed.connect(self.radioClose_btn_pressed)
        self.radioClose_btn.released.connect(self.radioClose_btn_released)
        self.radioClose_btn.clicked.connect(self.radioClose_btn_clicked)
        # 방송 리스트
        self.broadcast_list()

        # MQTT
        self.client = MqttClient(self)
        self.client.stateChanged.connect(self.on_stateChanged)
        self.client.messageSignal.connect(self.on_messageSignal)

        self.client.hostname = "58.124.114.104:1883"
        self.client.connectToHost()


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
        self.freqInput_btn.setStyleSheet("""background-color: #adadc8;
        font: 16pt "휴먼엑스포";""")

    def freqInput_released(self):
        self.freqInput_btn.setStyleSheet("""background-color: rgb(220, 220, 255);
        font: 16pt "휴먼엑스포";""")

    def freqInput_clicked(self):
        pass

    def radioClose_btn_pressed(self): #9b9bb4
        self.radioClose_btn.setStyleSheet("""background-color: #9b9bb4;
        font: 16pt "휴먼엑스포";""")

    def radioClose_btn_released(self):
        self.radioClose_btn.setStyleSheet("""background-color: rgb(220, 220, 255);
        font: 16pt "휴먼엑스포";""")

    def radioClose_btn_clicked(self):
        pass

    # 방송 리스트
    def broadcast_list(self):
        # Create QListWidget
        for index, name in [
            ('22년 5월 16일', '마을 방송입니다~~~'),
            ('22년 5월 15일', '마을 방송입니다~~~'),
            ('22년 5월 14일', '마을 방송입니다~~~'),
            ('22년 5월 13일', '마을 방송입니다~~~'),
            ('22년 5월 12일', '마을 방송입니다~~~'),
            ('22년 5월 11일', '마을 방송입니다~~~'),
            ('22년 5월 10일', '마을 방송입니다~~~'),
            ('22년 5월 9일', '마을 방송입니다~~~'),
            ('22년 5월 8일', '마을 방송입니다~~~')]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            # Create QListWidgetItem
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.listWidget)  # QtWidgets
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.listWidget.addItem(myQListWidgetItem)
            self.listWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

#MQTT
    @QtCore.pyqtSlot(int)
    def on_stateChanged(self, state):
        if state == MqttClient.Connected:
            print(state)
            self.client.subscribe("shok2")

    @QtCore.pyqtSlot(str)
    def on_messageSignal(self, msg):
        try:
            val = float(msg)
            self.lcd_number.display(val)
        except ValueError:
            print("error: Not is number")

# 방송 리스트
class QCustomQWidget (QtWidgets.QWidget):                       # QtWidgets
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()          # QtWidgets
        self.textUpQLabel    = QtWidgets.QLabel()               # QtWidgets
        self.textDownQLabel  = QtWidgets.QLabel()               # QtWidgets
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QtWidgets.QHBoxLayout()          # QtWidgets
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 0);
            border: 0px;
            font : 75 20pt "맑은 고딕";
            background: transparent;
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(0, 0, 0);
            border: 0px;
            font : 20px "맑은 고딕";
            background: transparent;
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

# MQTT
class MqttClient(QtCore.QObject):
    Disconnected = 0
    Connecting = 1
    Connected = 2

    MQTT_3_1 = mqtt.MQTTv31
    MQTT_3_1_1 = mqtt.MQTTv311

    connected = QtCore.pyqtSignal()
    disconnected = QtCore.pyqtSignal()

    stateChanged = QtCore.pyqtSignal(int)
    hostnameChanged = QtCore.pyqtSignal(str)
    portChanged = QtCore.pyqtSignal(int)
    keepAliveChanged = QtCore.pyqtSignal(int)
    cleanSessionChanged = QtCore.pyqtSignal(bool)
    protocolVersionChanged = QtCore.pyqtSignal(int)

    messageSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(MqttClient, self).__init__(parent)

        self.m_hostname = ""
        self.m_port = 1883
        self.m_keepAlive = 60
        self.m_cleanSession = True
        self.m_protocolVersion = MqttClient.MQTT_3_1

        self.m_state = MqttClient.Disconnected

        self.m_client =  mqtt.Client(clean_session=self.m_cleanSession, protocol=self.protocolVersion)

        self.m_client.on_connect = self.on_connect
        self.m_client.on_message = self.on_message
        self.m_client.on_disconnect = self.on_disconnect


    @QtCore.pyqtProperty(int, notify=stateChanged)
    def state(self):
        return self.m_state

    @state.setter
    def state(self, state):
        if self.m_state == state: return
        self.m_state = state
        self.stateChanged.emit(state)

    @QtCore.pyqtProperty(str, notify=hostnameChanged)
    def hostname(self):
        return self.m_hostname

    @hostname.setter
    def hostname(self, hostname):
        if self.m_hostname == hostname: return
        self.m_hostname = hostname
        self.hostnameChanged.emit(hostname)

    @QtCore.pyqtProperty(int, notify=portChanged)
    def port(self):
        return self.m_port

    @port.setter
    def port(self, port):
        if self.m_port == port: return
        self.m_port = port
        self.portChanged.emit(port)

    @QtCore.pyqtProperty(int, notify=keepAliveChanged)
    def keepAlive(self):
        return self.m_keepAlive

    @keepAlive.setter
    def keepAlive(self, keepAlive):
        if self.m_keepAlive == keepAlive: return
        self.m_keepAlive = keepAlive
        self.keepAliveChanged.emit(keepAlive)

    @QtCore.pyqtProperty(bool, notify=cleanSessionChanged)
    def cleanSession(self):
        return self.m_cleanSession

    @cleanSession.setter
    def cleanSession(self, cleanSession):
        if self.m_cleanSession == cleanSession: return
        self.m_cleanSession = cleanSession
        self.cleanSessionChanged.emit(cleanSession)

    @QtCore.pyqtProperty(int, notify=protocolVersionChanged)
    def protocolVersion(self):
        return self.m_protocolVersion

    @protocolVersion.setter
    def protocolVersion(self, protocolVersion):
        if self.m_protocolVersion == protocolVersion: return
        if protocolVersion in (MqttClient.MQTT_3_1, self.MQTT_3_1_1):
            self.m_protocolVersion = protocolVersion
            self.protocolVersionChanged.emit(protocolVersion)

    #################################################################
    @QtCore.pyqtSlot()
    def connectToHost(self):
        if self.m_hostname:
            self.m_client.connect(self.m_hostname,
                port=self.port,
                keepalive=self.keepAlive)

            self.state = MqttClient.Connecting
            self.m_client.loop_start()

    @QtCore.pyqtSlot()
    def disconnectFromHost(self):
        self.m_client.disconnect()

    def subscribe(self, path):
        if self.state == MqttClient.Connected:
            self.m_client.subscribe(path)

    #################################################################
    # callbacks
    def on_message(self, mqttc, obj, msg):
        mstr = msg.payload.decode("ascii")
        # print("on_message", mstr, obj, mqttc)
        self.messageSignal.emit(mstr)

    def on_connect(self, *args):
        # print("on_connect", args)
        self.state = MqttClient.Connected
        self.connected.emit()

    def on_disconnect(self, *args):
        # print("on_disconnect", args)
        self.state = MqttClient.Disconnected
        self.disconnected.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
