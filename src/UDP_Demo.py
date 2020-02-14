#!/usr/bin/python
# coding=utf-8

import numpy as np
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFont
from maya_widget import MayaviQWidget, myAction, IndexedQSlider
import utils, socket, threading

win = None

stringArray = ["weight", "height", "neck", "chest", "belly button waist",
                 "gluteal hip", "neck shoulder elbow wrist",
                 "crotch knee floor", "across back shoulder neck",
                 "neck to gluteal hip", "natural waist", "max.hip",
                 "natural waist rise", "shoulder to midhand", "upper arm",
                 "wrist", "outer natural waist to floor",
                 "knee", "max.thigh"]
# usage: GUI for showing all models
class HumanShapeAnalysisDemo(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.statusBar().showMessage("Hello there")
    self.mainBox = QtGui.QHBoxLayout()

    container = QtGui.QWidget()
    container.setWindowTitle("신체 정보 기반 3D")
    layout = QtGui.QGridLayout(container)
    self.viewer3D = MayaviQWidget(container)
    layout.addWidget(self.viewer3D, 1, 1)
    container.show()

    self.mainBox.addWidget(container)
    self.setWindowTitle("3D Human Body Reshaping with Anthropometric Modeling")

    parentWidget = QtGui.QWidget()
    self.box = QtGui.QVBoxLayout()
    self.set_menu()
    self.set_radio()
    self.set_button()
    self.set_slider()

    self.mainBox.addLayout(self.box)
    self.mainBox.addWidget(self.viewer3D)
    self.set_dialog()
    self.resize(650, 650)

    self.viewer3D.setSizePolicy(
      QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    parentWidget.setLayout(self.mainBox)
    self.setCentralWidget(parentWidget)

  def set_menu(self):
    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')

    exit = QtGui.QAction("Exit", self)
    exit.setShortcut("Ctrl+Q")
    exit.setStatusTip('Exit application')
    self.connect(exit, QtCore.SIGNAL(
      'triggered()'), QtCore.SLOT('close()'))
    fileMenu.addAction(exit)

    save = QtGui.QAction("Save", self)
    save.setShortcut("Ctrl+S")
    save.setStatusTip('save obj file')
    self.connect(save, QtCore.SIGNAL('triggered()'), self.viewer3D.save)
    fileMenu.addAction(save)

    self.flag_ = 0
    self.label_ = "female"
    self.mode = {0:"global_mapping", 1:"local_with_mask", 2:"local_with_rfemat"}
    for i in range(0, len(self.mode)):
      mode = myAction(i, self.mode[i], self)
      self.connect(mode, QtCore.SIGNAL('myact(int)'), self.select_mode)
      fileMenu.addAction(mode)
    self.setToolTip('This is a window, or <b>something</b>')

  def set_radio(self):
    self.radio1 = QtGui.QRadioButton('female')
    self.radio2 = QtGui.QRadioButton('male')
    self.radio1.setFont(QFont("Arial", 11))
    self.radio2.setFont(QFont("Arial", 11))
    self.radio1.setChecked(True)
    self.radio1.toggled.connect(self.radio_act)
    self.radio2.toggled.connect(self.radio_act)

    radio_box = QtGui.QHBoxLayout()
    radio_box.addWidget(self.radio1)
    radio_box.addWidget(self.radio2)
    self.box.addLayout(radio_box)

  def radio_act(self):
    if self.radio1.isChecked():
      self.label_ = 'female'
    else:
      self.label_ = 'male'
    self.viewer3D.select_mode(label=self.label_, flag=self.flag_)

  def set_button(self):
    self.button_box = QtGui.QHBoxLayout()

    self.reset_button = QtGui.QPushButton("RESET")
    self.reset_button.setStatusTip('reset input to mean value')
    self.reset_button.setFont(QFont("Arial", 11))
    self.connect(self.reset_button, QtCore.SIGNAL(
      'clicked()'), self.reset)
    self.button_box.addWidget(self.reset_button)

    self.pre_button = QtGui.QPushButton("PREDICT")
    self.pre_button.setToolTip('model your own shape')
    self.pre_button.setFont(QFont("Arial", 11))
    self.connect(self.pre_button, QtCore.SIGNAL(
      'clicked()'), self.show_dialog)
    self.button_box.addWidget(self.pre_button)
    self.box.addLayout(self.button_box)

  def set_slider(self):
    self.slider = []
    self.spin = []
    self.label = []
    for i in range(0, utils.M_NUM):
      hbox = QtGui.QHBoxLayout()
      slider = IndexedQSlider(i, QtCore.Qt.Horizontal, self)
      slider.setStatusTip('%d. %s' % (i, utils.M_STR[i]))
      slider.setRange(-30, 30)
      #slider.valueChangeForwarded.connect(
      #    self.viewer3D.sliderForwardedValueChangeHandler)
      slider.setFixedWidth(60)
      self.slider.append(slider)
      spinBox = QtGui.QSpinBox()
      spinBox.setRange(-30, 30)
      #spinBox.valueChanged.connect(slider.setValue)
      #slider.valueChanged.connect(spinBox.setValue)
      self.spin.append(spinBox)
      label = QtGui.QLabel()
      label.setText(utils.M_STR[i])
      # label.setFont(QFont("Arial", 11, QFont.Bold))
      label.setFont(QFont("Arial", 12))
      label.setFixedWidth(190)
      self.label.append(label)
      hbox.addWidget(label)
      hbox.addWidget(slider)
      hbox.addWidget(spinBox)
      self.box.addLayout(hbox)

  def set_dialog(self):
    self.pre_dialog = QtGui.QDialog()
    self.dialogBox = QtGui.QVBoxLayout()
    self.pre_dialog.setWindowTitle("Input")
    self.editList = []
    for i in range(0, utils.M_NUM):
      edit = QtGui.QLineEdit()
      self.editList.append(edit)
      label = QtGui.QLabel()
      label.setText(utils.M_STR[i])
      # label.setFont(QFont("Arial", 11, QFont.Bold))
      label.setFont(QFont("Arial", 12))
      label.setFixedHeight(20)
      label.setFixedWidth(190)
      box = QtGui.QHBoxLayout()
      box.addWidget(label)
      box.addWidget(edit)
      self.dialogBox.addLayout(box)
    dialogOK = QtGui.QPushButton("OK")
    clearButton = QtGui.QPushButton("CLEAR")
    dialogOK.setFont(QFont("Arial", 11, QFont.Bold))
    clearButton.setFont(QFont("Arial", 11, QFont.Bold))
    self.connect(dialogOK, QtCore.SIGNAL('clicked()'), self.predict)
    self.connect(clearButton, QtCore.SIGNAL('clicked()'), self.clear)
    box = QtGui.QHBoxLayout()
    box.addWidget(dialogOK)
    box.addWidget(clearButton)
    self.dialogBox.addLayout(box)
    self.pre_dialog.setLayout(self.dialogBox)

  def predict(self):
    try:
      w = float(self.editList[0].text())
      h = float(self.editList[1].text())
      data = []
      data.append(w ** (1.0 / 3.0) * 1000)
      data.append(h * 10)
      for i in range(2, len(self.editList)):
        try:
          tmp = float(self.editList[i].text())
          data.append(tmp * 10)
        except ValueError:
          data.append(0)
      data = np.array(data).reshape(utils.M_NUM, 1)
      [t_data, value] = self.viewer3D.predict(data)
      for i in range(2, len(self.editList)):
        self.editList[i].setText("%f" % (value[i, 0] / 10))
      for i in range(0, len(self.slider)):
        self.slider[i].valueChangeForwarded.disconnect(
          self.viewer3D.sliderForwardedValueChangeHandler)
        self.slider[i].setValue(t_data[i] / 3.0 * 100.0)
        self.slider[i].valueChangeForwarded.connect(
          self.viewer3D.sliderForwardedValueChangeHandler)
    except ValueError:
      self.editList[0].setText("Please input.")
      self.editList[1].setText("Please input.")

  def UDP_predict(self, decode_data):
    try:
      if decode_data[19] == 'male':
        win.radio2.setChecked(True)
      elif decode_data[19] == 'female':
        win.radio1.setChecked(True)

      container = QtGui.QWidget()
      container.setWindowTitle("신체 정보 기반 3D")
      win.viewer3D = MayaviQWidget(container)
      w = float(decode_data[0])
      h = float(decode_data[1])
      data = []
      data.append(w ** (1.0 / 3.0) * 1000)
      data.append(h * 10)
      for i in range(2, len(win.editList)):
        try:
          tmp = float(decode_data[i])
          data.append(tmp * 10)
        except ValueError:
          data.append(0)
      data = np.array(data).reshape(utils.M_NUM, 1)
      [t_data, value] = win.viewer3D.predict(data)
      print(stringArray[0], " = ", w)
      print(stringArray[1], " = ", h)
      for i in range(2, len(win.editList)):
        print(stringArray[i], " = ", (value[i, 0] / 10))

    except (ValueError, TypeError):
      print("Please Check your weight or height value.")
    win.viewer3D = None

  def closeEvent(self, event):
    self.pre_dialog.close()
    event.accept()

  def reset(self):
    for i in range(0, utils.M_NUM):
      self.slider[i].setValue(0)

  def clear(self):
    for i in range(0, len(self.editList)):
      self.editList[i].clear()

  def show_dialog(self):
    self.pre_dialog.show()

  def select_mode(self, id):
    self.flag_ = id
    self.setWindowTitle(self.mode[id])
    self.viewer3D.select_mode(label=self.label_, flag=self.flag_)

def show_app():
  global win
  app = QtGui.QApplication(sys.argv)
  win=HumanShapeAnalysisDemo()
  win.viewer3D = None
  win.show()
  udp_socket = threading.Thread(target = UDP_listening, args= ())
  udp_socket.start()
  #win.viewer3D.save()
  sys.exit(app.exec_())

def UDP_listening():
  global win
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind( ('localhost', 5566) )
  print('UDP socket port = ', 5566)

  while True:
    udp_data, addr = sock.recvfrom(5577)
    print("Received 3D modeling request message from unity.")
    decode_data = udp_data.decode().split('/')

    print('length = ', len(decode_data))
    print(decode_data)

    if len(decode_data) == 20:
      win.UDP_predict(decode_data)
    else:
      print("But... Data parsing error\n", udp_data.decode())

if __name__ == "__main__":
    show_app()