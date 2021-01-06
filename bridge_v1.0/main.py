#jazzy 2020.8.19 inital version

import Ui_MainWin,Ui_lalinhe_bridge
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel,QThread,QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QGraphicsPixmapItem,QGraphicsScene
import sys
import pyqtgraph as pg
import MySQLdb
import queue
import time
import numpy as np
import cv2

#主窗口
class MyWindow(QtWidgets.QMainWindow,Ui_MainWin.Ui_MainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Client QtGUI")

#拉林河大桥
class MyWindow2(QtWidgets.QMainWindow,Ui_lalinhe_bridge.Ui_MainWindow):
    def __init__(self):
        super(MyWindow2,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Window2")
        self.eventbind()
        self.weight_init()
    
    def weight_init(self):
        self.main_page1_init()
    
    def main_page1_init(self):
        # self.page1_graphicsView.setStyleSheet("background:transparent;")    #page1-图片控件背景透明
        # img1_path = './images/1.png'
        # img1 = cv2.imread(img1_path)  # 读取图像
        # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)  # 转换图像通道
        # x = img1.shape[1]  # 获取图像大小
        # y = img1.shape[0]
        # self.zoomscale = 1  # 图片放缩尺度
        # frame = QImage(img1, x, y, QImage.Format_RGB888)
        # pix = QPixmap.fromImage(frame)
        # self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        # self.scene = QGraphicsScene()  # 创建场景
        # self.scene.addItem(self.item)
        # self.page1_graphicsView.setScene(self.scene)
        # self.page1_graphicsView.show()
        
        pix_1 = QPixmap('./images/1.png')
        self.page1_piclabel.setPixmap(pix_1)
        self.page1_piclabel.setScaledContents(True)   #自适应QLabel大小

        pix_arrowleft = QPixmap('./images/left_arrow.png')
        pix_arrowright = QPixmap('./images/right_arrow.png')
        pix_arrowup = QPixmap('./images/up_arrow.png')

        self.page1_la.setPixmap(pix_arrowleft)
        self.page1_ra.setPixmap(pix_arrowright)
        self.page1_ua.setPixmap(pix_arrowup)

        self.page1_la.setScaledContents(True) 
        self.page1_ra.setScaledContents(True) 
        self.page1_ua.setScaledContents(True) 

    def eventbind(self):                                                    #事件绑定
        self.MainMenu_miBtn.clicked.connect(self.MainMenu_miBtn_clicked)    #主界面按钮绑定
        self.MainMenu_rtdBtn.clicked.connect(self.MainMenu_rtdBtn_clicked)  
        self.MainMenu_dnBtn.clicked.connect(self.MainMenu_dnBtn_clicked)
    
    def MainMenu_miBtn_clicked(self):
        self.Main_stackedWidget.setCurrentIndex(0)

    def MainMenu_rtdBtn_clicked(self):
        self.Main_stackedWidget.setCurrentIndex(1)

    def MainMenu_dnBtn_clicked(self):
        self.Main_stackedWidget.setCurrentIndex(2)

class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow2 = MyWindow2()
    myshow.btn1.clicked.connect(myshow2.show)

    styleFile = './winstyle.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    myshow.setStyleSheet(qssStyle)

    myshow.show()
    sys.exit(app.exec())