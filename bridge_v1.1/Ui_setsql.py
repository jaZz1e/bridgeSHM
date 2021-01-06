# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\jazzy\Documents\bridge_SHM\setsql.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(310, 384)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.testconn_btn = QtWidgets.QPushButton(self.centralwidget)
        self.testconn_btn.setGeometry(QtCore.QRect(20, 270, 75, 23))
        self.testconn_btn.setObjectName("testconn_btn")
        self.sqlconfirm_btn = QtWidgets.QPushButton(self.centralwidget)
        self.sqlconfirm_btn.setGeometry(QtCore.QRect(120, 270, 75, 23))
        self.sqlconfirm_btn.setObjectName("sqlconfirm_btn")
        self.sqlcans_btn = QtWidgets.QPushButton(self.centralwidget)
        self.sqlcans_btn.setGeometry(QtCore.QRect(220, 270, 75, 23))
        self.sqlcans_btn.setObjectName("sqlcans_btn")
        self.host_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.host_edit.setGeometry(QtCore.QRect(120, 20, 161, 31))
        self.host_edit.setObjectName("host_edit")
        self.port_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.port_edit.setGeometry(QtCore.QRect(120, 70, 161, 31))
        self.port_edit.setObjectName("port_edit")
        self.sqluser_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.sqluser_edit.setGeometry(QtCore.QRect(120, 120, 161, 31))
        self.sqluser_edit.setObjectName("sqluser_edit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 19, 91, 31))
        font = QtGui.QFont()
        font.setFamily("华光小标宋_CNKI")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 69, 91, 31))
        font = QtGui.QFont()
        font.setFamily("华光小标宋_CNKI")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 119, 91, 31))
        font = QtGui.QFont()
        font.setFamily("华光小标宋_CNKI")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.sqlpwd_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.sqlpwd_edit.setGeometry(QtCore.QRect(120, 170, 161, 31))
        self.sqlpwd_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sqlpwd_edit.setObjectName("sqlpwd_edit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 170, 91, 31))
        font = QtGui.QFont()
        font.setFamily("华光小标宋_CNKI")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 220, 91, 31))
        font = QtGui.QFont()
        font.setFamily("华光小标宋_CNKI")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.database_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.database_edit.setGeometry(QtCore.QRect(120, 220, 161, 31))
        self.database_edit.setObjectName("database_edit")
        self.setsqllb = QtWidgets.QLabel(self.centralwidget)
        self.setsqllb.setGeometry(QtCore.QRect(20, 310, 151, 16))
        self.setsqllb.setObjectName("setsqllb")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 310, 22))
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
        self.testconn_btn.setText(_translate("MainWindow", "测试连接"))
        self.sqlconfirm_btn.setText(_translate("MainWindow", "确认"))
        self.sqlcans_btn.setText(_translate("MainWindow", "取消"))
        self.host_edit.setText(_translate("MainWindow", "localhost"))
        self.port_edit.setText(_translate("MainWindow", "3306"))
        self.sqluser_edit.setText(_translate("MainWindow", "root"))
        self.label.setText(_translate("MainWindow", "host"))
        self.label_2.setText(_translate("MainWindow", "port"))
        self.label_3.setText(_translate("MainWindow", "user"))
        self.sqlpwd_edit.setText(_translate("MainWindow", "9qqhaoma"))
        self.label_4.setText(_translate("MainWindow", "password"))
        self.label_5.setText(_translate("MainWindow", "database"))
        self.database_edit.setText(_translate("MainWindow", "BridgeSHM"))
        self.setsqllb.setText(_translate("MainWindow", "设置后点击测试"))
