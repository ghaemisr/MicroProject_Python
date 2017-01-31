import os
import sys
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from send import send
from receive import receive
import re


Form = uic.loadUiType(os.path.join(os.getcwd(), "mainwindow.ui"))[0]


class IntroWindow(QMainWindow, Form):
    def __init__(self):
        Form.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        pixmap = QtGui.QPixmap('000.jpg')
        self.Image_label.setPixmap(pixmap)
        self.Image_label.setScaledContents(True)
        self.lRoom_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.kRoom_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.bRoom_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.oRoom_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.radio_dict = {'B': False, 'E': False, 'D': False,
                           'G': True, 'H': True, 'J': True,
                           'L': False, 'M': False, 'Q': False,
                           'Z': False}
        self.port = 8000
        self.startListening_pushButton.clicked.connect(self.listen)
        self.stop_pushButton.clicked.connect(self.stop)
        self.send_pushButton.clicked.connect(self.send)
        self.thread = ReceiveThread(self.port)

    def send(self):
        message = self.send_lineEdit.text()
        self.check_status()
        control = ''
        for key, value in self.radio_dict.items():
            if value is True:
                control += key
        if control != '':
            send(7000, control)
        else:
            send(7000, message)
        self.update_LEDs()

    def listen(self):
        self.port_label.setText(str(self.port))
        self.thread = ReceiveThread(self.port)
        self.thread.update_trigger.connect(self.update_label)
        self.thread.start()

    def stop(self):
        receive(self.port, "Stop")
        self.update_label("port {} stopped".format(self.port))

    def update_label(self, x):
        self.receive_label.setText(str(x))
        # pattern = re.compile(r'b\'(\w)T = (\d\d)\n\'.*')
        # print(str(x))
        # temp = pattern.search(str(x))
        # print(temp)
        # if temp:
        #     print("pattern recienalsl: {}".format(temp.group(1)))
        #     if temp.group(1) == 'L':
        #         self.lRoomT_label.setText(temp.group(2))
        #     elif temp.group(1) == 'B':
        #         self.bRoomT_label.setText(temp.group(2))
        #     elif temp.group(1) == 'K' :
        #         self.kRoomT_label.setText(temp.group(2))
        #     elif temp.group(1) == 'O' :
        #         self.oRoomT_label.setText(temp.group(2))

        print(str(x))

    def update_LEDs(self):
        lRoom = self.lRoom_radioButton.isChecked()
        bRoom = self.bRoom_radioButton.isChecked()
        kRoom = self.kRoom_radioButton.isChecked()
        if lRoom and bRoom and kRoom:
            pixmap = QtGui.QPixmap('111.jpg')
            self.Image_label.setPixmap(pixmap)
            self.Image_label.setScaledContents(True)
        elif lRoom and bRoom:
            pixmap = QtGui.QPixmap('101.jpg')
            self.Image_label.setPixmap(pixmap)
            self.Image_label.setScaledContents(True)
        elif lRoom and kRoom:
            pixmap = QtGui.QPixmap('110.jpg')
            self.Image_label.setPixmap(pixmap)
            self.Image_label.setScaledContents(True)
        elif kRoom and bRoom:
            pixmap = QtGui.QPixmap('011.jpg')
            self.Image_label.setPixmap(pixmap)
            self.Image_label.setScaledContents(True)
        elif lRoom:
            pixmap = QtGui.QPixmap('100.jpg')
            self.Image_label.setPixmap(pixmap)
            self.Image_label.setScaledContents(True)
        elif bRoom:
            pixmap = QtGui.QPixmap('001.jpg')
            self.Image_label.setPixmap(pixmap)
            self.Image_label.setScaledContents(True)
        elif kRoom:
            pixmap = QtGui.QPixmap('010.jpg')
            self.Image_label.setPixmap(pixmap)
            self.Image_label.setScaledContents(True)
        else:
            pixmap = QtGui.QPixmap('000.jpg')
            self.Image_label.setPixmap(pixmap)
            self.Image_label.setScaledContents(True)

    def check_status(self):
        self.radio_dict['F'] = self.lRoom_radioButton.isChecked()
        self.radio_dict['D'] = self.bRoom_radioButton.isChecked()
        self.radio_dict['E'] = self.kRoom_radioButton.isChecked()
        self.radio_dict['K'] = not(self.lRoom_radioButton.isChecked())
        self.radio_dict['H'] = not(self.bRoom_radioButton.isChecked())
        self.radio_dict['J'] = not(self.kRoom_radioButton.isChecked())
        self.radio_dict['X'] = self.lRoomT_radioButton.isChecked()
        self.radio_dict['Q'] = self.bRoomT_radioButton.isChecked()
        self.radio_dict['M'] = self.kRoomT_radioButton.isChecked()
        self.radio_dict['Z'] = self.oRoomT_radioButton.isChecked()


class ReceiveThread(QtCore.QThread):
    update_trigger = QtCore.pyqtSignal(bytes)

    def __init__(self, port):
        QtCore.QThread.__init__(self)
        self.port2 = int(port)

    def run(self):
        while True:
            self.update_trigger.emit(receive(self.port2, "Receive"))
        app.processEvents()


app = QApplication(sys.argv)
app.setStyle('Plastique')
window = IntroWindow()
window.show()
sys.exit(app.exec_())