# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

class MyApp(QWidget):

  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
      btn = QPushButton('Quit', self)
      btn.move(50, 50)
      btn.resize(btn.sizeHint())
      btn.clicked.connect(QApplication.instance().quit)

      icon = QIcon('img/logo2.png')
      self.setWindowTitle('Broadcast')
      self.setWindowIcon(icon)
      self.setGeometry(300, 300, 924, 600)
      self.show()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())