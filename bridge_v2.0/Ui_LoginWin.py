# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\jazzy\Documents\BridgeSHM1127\LoginWin.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1122, 831)
        MainWindow.setMouseTracking(False)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(600, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout_2.addItem(spacerItem2, 1, 2, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.loginWidget = QtWidgets.QWidget(self.centralwidget)
        self.loginWidget.setObjectName("loginWidget")
        self.label_3 = QtWidgets.QLabel(self.loginWidget)
        self.label_3.setGeometry(QtCore.QRect(100, 120, 121, 41))
        font = QtGui.QFont()
        font.setFamily("华光大标宋_CNKI")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAutoFillBackground(True)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.loginWidget)
        self.label_2.setGeometry(QtCore.QRect(100, 190, 121, 41))
        font = QtGui.QFont()
        font.setFamily("华光大标宋_CNKI")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.userInputBox = QtWidgets.QLineEdit(self.loginWidget)
        self.userInputBox.setGeometry(QtCore.QRect(260, 120, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.userInputBox.setFont(font)
        self.userInputBox.setAlignment(QtCore.Qt.AlignCenter)
        self.userInputBox.setObjectName("userInputBox")
        self.pwdInputBox = QtWidgets.QLineEdit(self.loginWidget)
        self.pwdInputBox.setGeometry(QtCore.QRect(260, 190, 241, 41))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(10)
        self.pwdInputBox.setFont(font)
        self.pwdInputBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwdInputBox.setAlignment(QtCore.Qt.AlignCenter)
        self.pwdInputBox.setObjectName("pwdInputBox")
        self.loginBtn = QtWidgets.QPushButton(self.loginWidget)
        self.loginBtn.setGeometry(QtCore.QRect(130, 280, 141, 51))
        font = QtGui.QFont()
        font.setFamily("华光大标宋_CNKI")
        font.setPointSize(12)
        self.loginBtn.setFont(font)
        self.loginBtn.setObjectName("loginBtn")
        self.label_4 = QtWidgets.QLabel(self.loginWidget)
        self.label_4.setGeometry(QtCore.QRect(0, 70, 591, 41))
        font = QtGui.QFont()
        font.setFamily("华光大标宋_CNKI")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAutoFillBackground(True)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.conSQLBtn = QtWidgets.QPushButton(self.loginWidget)
        self.conSQLBtn.setGeometry(QtCore.QRect(360, 280, 141, 51))
        font = QtGui.QFont()
        font.setFamily("华光大标宋_CNKI")
        font.setPointSize(12)
        self.conSQLBtn.setFont(font)
        self.conSQLBtn.setObjectName("conSQLBtn")
        self.gridLayout.addWidget(self.loginWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 400, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem4, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 4, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 3, 0, 1, 1)
        self.bannerlabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("华光标题宋_CNKI")
        font.setPointSize(36)
        self.bannerlabel.setFont(font)
        self.bannerlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.bannerlabel.setObjectName("bannerlabel")
        self.gridLayout_3.addWidget(self.bannerlabel, 1, 0, 1, 3)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem7, 3, 2, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem8, 2, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1122, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "用户名"))
        self.label_2.setText(_translate("MainWindow", "密  码"))
        self.loginBtn.setText(_translate("MainWindow", "登  录"))
        self.label_4.setText(_translate("MainWindow", "欢迎登录"))
        self.conSQLBtn.setText(_translate("MainWindow", "连  接"))
        self.bannerlabel.setText(_translate("MainWindow", "黑龙江省公路综合管理系统——桥梁健康监测子系统"))
