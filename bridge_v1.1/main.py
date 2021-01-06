#jazzy 2020.8.19 inital version

import Ui_MainWin,Ui_lalinhe_bridge,Ui_setsql
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel,QThread,QTimer,QDateTime, QDate, QTime, Qt, QEvent
from PyQt5.QtGui import QPixmap, QImage, QMovie, QMouseEvent
from PyQt5.QtWidgets import QGraphicsPixmapItem,QGraphicsScene,QMessageBox,QTreeWidgetItem
import sys
import pyqtgraph as pg
import MySQLdb
import queue
import time
import numpy as np
# import cv2
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget
# import qdarkstyle
# import display3d

qthread_pool = []

admin_dic = {}
admin_dic.update({'admin':'123456'})
 #默认选择
bridge_dic = {}
bridge_dic.update({1:'拉林河大桥'})
bridge_dic.update({2:'通河大桥'})

conn_glb = None

host_glb = None
port_glb = None
user_glb = None
pwd_glb = None
database_glb = None

def get_conn(host_i,port_i,user_i,passwd_i,db_i):
    con = MySQLdb.connect(
        host=host_i,
        port=port_i,
        user=user_i,
        passwd=passwd_i,
        db=db_i,
        charset='utf8'
    )
    return con

class Sensor:
    def __init__(self,dtype='strain',globalnum=1,index='1_L_01'):
        self.state = 0 #0:正常 1:关闭 2:报警
        self.type = dtype
        self.globalnum = globalnum
        self.index = index

class Sqlwindow(QtWidgets.QMainWindow,Ui_setsql.Ui_MainWindow):
    def __init__(self):
        super(Sqlwindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("数据库设置")
        self.btnbind()
    
    def btnbind(self):
        self.testconn_btn.clicked.connect(self.testconn)
        self.sqlconfirm_btn.clicked.connect(self.sqlconfirm)
        self.sqlcans_btn.clicked.connect(self.sqlcans)

    def sqlconfirm(self):

        self.host = self.host_edit.text()
        port = self.port_edit.text()
        try:
            self.port = int(port)
        except:
            QMessageBox.about(self,"警告",'输入错误：port')
            return
        self.user = self.sqluser_edit.text()
        self.pwd = self.sqlpwd_edit.text()
        self.database = self.database_edit.text()

        global host_glb,port_glb,user_glb,pwd_glb,database_glb

        host_glb = self.host
        port_glb = self.port
        user_glb = self.user
        pwd_glb = self.pwd
        database_glb = self.database

        try:
            global conn_glb
            conn_glb = get_conn(self.host,self.port,self.user,self.pwd,self.database)
            # self.cursor = self.con.cursor()
            QMessageBox.about(self,"提示",'连接成功')
            conn_glb.close()
            

            self.close()
        
        except:
            QMessageBox.about(self,"提示",'连接失败')
            conn_glb = None
            return
    
    def sqlcans(self):
        self.close()

    
    def testconn(self):
        host = self.host_edit.text()
        port = self.port_edit.text()
        try:
            port = int(port)
        except:
            QMessageBox.about(self,"警告",'输入错误：port')
            return
        user = self.sqluser_edit.text()
        pwd = self.sqlpwd_edit.text()
        database = self.database_edit.text()


        try:
            self.con = get_conn(host,port,user,pwd,database)
            cursor = self.con.cursor()
            self.setsqllb.setText('测试成功')
            self.con.close()
        
        except:
            self.setsqllb.setText('测试失败')
            return

#主窗口
class MyWindow(QtWidgets.QMainWindow,Ui_MainWin.Ui_MainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Client QtGUI")
        self.widget_init()
        self.eventbind()
        self.parainit()

    def parainit(self):
        self.select_id = 1
    
    def widget_init(self):
        pix_1 = QPixmap('./images/hlj_map_1.png')
        self.Mainwin_maplb.setPixmap(pix_1)
        self.Mainwin_maplb.setScaledContents(True)
        pix_2 = QPixmap('./images/mainlogo.png')
        self.mainlogo.setPixmap(pix_2)
        self.mainlogo.setScaledContents(True)

        

    def eventbind(self):                                                    #事件绑定
        self.llh_selectbtn.clicked.connect(self.llh_selected)
        self.th_selectbtn.clicked.connect(self.th_selected)
        self.mainwin_loginbtn.clicked.connect(self.userlogin)
    
    def userlogin(self):
        urn = self.mainwin_username.text()
        pwd = self.mainwin_pwdedit.text()
        if urn == '':
            QMessageBox.about(self,"警告",'用户名为空！')
            return
        if pwd == '':
            QMessageBox.about(self,"警告",'密码为空！')
            return
        rtnpwd = admin_dic.get(urn,'unknown')
        if rtnpwd == pwd:
            self.login_suc()
            
        else:
            QMessageBox.about(self,"提示",'密码错误或用户名不存在')

    def login_suc(self):
        # print(select_id)
        if self.select_id == 1:
            QMessageBox.about(self,"提示",'登录成功')
            self.myshow2 = MyWindow2()
            self.myshow2.show()
            self.myshow2.setStyleSheet(qssStyle2)
            self.close()
        else:
            QMessageBox.about(self,"提示",'该大桥未载入数据')

    def llh_selected(self):
        self.select_id = 1
        self.mainwin_dipselecttext.setText('当前选择：'+bridge_dic[self.select_id])

    def th_selected(self):
        self.select_id = 2
        
        self.mainwin_dipselecttext.setText('当前选择：'+bridge_dic[self.select_id])

#拉林河大桥
class MyWindow2(QtWidgets.QMainWindow,Ui_lalinhe_bridge.Ui_MainWindow):
    def __init__(self):
        super(MyWindow2,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Window2")
        self.eventbind()
        self.sensor_init()
        self.widget_init()
        self.sql_init()

    def sql_init(self):
        pass

    def add_sensor(self, type, bdpos, pos, lcnum):
        index = str(bdpos) + pos + str(lcnum)
        sensor = Sensor(type, self.num_cnt, index)
        self.sensor_dict.update({index: sensor})
        self.sensor_index.update({self.num_cnt: sensor})
        self.num_cnt += 1

    def sensor_init(self):
        self.sensor_dict = {}
        self.sensor_index = {}

        self.num_cnt = 1
        #strain sensor init
        #1-1
        for num in range(11):
            self.add_sensor('strain', num + 1, '_C_', 1)
            self.add_sensor('strain', num + 1, '_C_', 2)
            self.add_sensor('strain', num + 1, '_C_', 3)
            self.add_sensor('strain', num + 1, '_C_', 4)

        #2-2
        self.add_sensor('strain', 6, '_L_', 1)
        self.add_sensor('strain', 6, '_L_', 2)
        self.add_sensor('strain', 6, '_L_', 7)
        self.add_sensor('strain', 6, '_L_', 8)
        self.add_sensor('strain', 6, '_R_', 1)
        self.add_sensor('strain', 6, '_R_', 2)
        self.add_sensor('strain', 6, '_R_', 7)
        self.add_sensor('strain', 6, '_R_', 8)

        #3-3
        self.add_sensor('strain', 11, '_R_', 2)
        self.add_sensor('strain', 11, '_R_', 5)
        self.add_sensor('strain', 11, '_R_', 6)

    
    def widget_init(self):
        self.main_page1_init()
        self.main_page2_init()
        self.showtime_init()
        self.actionlink_DB.triggered.connect(self.linkDBwindow)
    
    def main_page1_init(self):
        self.init_3d()
        self.init_tab()
        self.init_main_pg()
        self.select_blocknum = 0
        self.select_localsensornum = 0
    
    def main_page2_init(self):
        self.treeWidgetinit()
        self.calinit()
        self.pg2disinit()
        self.page2_displaybtn.clicked.connect(self.pg2display)

    def pg2disinit(self):
        pg.setConfigOption('background', '#31363b')
        self.main_pw2 = pg.GraphicsLayoutWidget()
        # self.main_pw = pg.GraphicsWindow()
        
        # self.main_p3 = pg.ViewBox()
        ax1 = pg.AxisItem(orientation='bottom')
        ax2 = pg.AxisItem(orientation='top')
        ax3 = pg.AxisItem(orientation='left')
        ax4 = pg.AxisItem(orientation='right')
        ax4.setTicks([''])
        ax2.setTicks([''])
        self.main_p2 = self.main_pw2.addPlot(axisItems={'bottom':ax1,'top':ax2,'left':ax3,'right':ax4})
        self.main_p2.setLabel('bottom', "时间")
        self.main_p2.setLabel('left', "幅值")
        self.main_p2.setLabel('right', " ")
        self.main_p2.setLabel('top', " ")

        self.main_curve2 = self.main_p2.plot()

        self.page2_vl_graph.addWidget(self.main_pw2)

    def calinit(self):
        self.selectdate = time.strftime('%Y%m%d',time.localtime())
        self.calendarWidget.selectionChanged.connect(self.changeDate)
    
    def changeDate(self):
        self.selectdate = self.calendarWidget.selectedDate().toString("yyyyMMdd")
        
        # print(self.selectdate.toString("yyyyMMdd"))

    def pg2display(self):
        if host_glb == None:
            QMessageBox.about(self,"警告",'未连接数据库')
            return

        con = get_conn(host_glb,port_glb,user_glb,pwd_glb,database_glb)
        cursor = con.cursor()
        tbname = 'llh%03d%s' % (self.selectsensor,self.selectdate)
        cmd = "SELECT table_name FROM information_schema.TABLES WHERE table_name ='%s';" % (tbname)
        cursor.execute(cmd)
        if not len(cursor.fetchall()):
            QMessageBox.about(self,"警告",'当日无数据')
            con.close()
            return
        cmd = "SELECT val FROM %s;" % (tbname)
        cursor.execute(cmd)
        fetch_inf = cursor.fetchall()
        # print(fetch_inf)
        self.display2 = [float(x[0]) for x in fetch_inf]
        self.main_curve2.setData(self.display2)
        con.close()

    def treeWidgetinit(self):
        self.selectsensor = None

        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['传感器','描述'])
        self.treeWidget.setColumnWidth(0,500)

        self.root_sensor = QTreeWidgetItem(self.treeWidget)
        self.root_sensor.setText(0,'拉林河大桥')

        secondlist = ['应变','裂缝','加速度']
        self.gen_branch(self.root_sensor,secondlist)

        thirdlist = ['第1跨','第2跨','第3跨','第4跨','第5跨','第6跨','第7跨','第8跨','第9跨','第10跨','第11跨']
        # print(thirdlist)
        self.gen_branch(self.root_sensor.child(0), thirdlist)
        self.gen_branch(self.root_sensor.child(1), thirdlist)
        self.gen_branch(self.root_sensor.child(2), thirdlist)

        forthlist = ['跨中','跨北','跨南']
        for i in range(11):
            self.gen_branch(self.root_sensor.child(0).child(i), forthlist)
            self.gen_branch(self.root_sensor.child(1).child(i), forthlist)
            self.gen_branch(self.root_sensor.child(2).child(i), forthlist)
        
        for sensor in self.sensor_dict.values():
            if sensor.type == 'strain':
                self.typenum = 0
            elif sensor.type == 'rent':
                self.typenum = 1
            elif sensor.type == 'acc':
                self.typenum = 2
            
            bdnum,bdpos,_ = sensor.index.split('_')
            if bdpos == 'C':
                self.bdposnum = 0
            if bdpos == 'L':
                self.bdposnum = 1
            if bdpos == 'R':
                self.bdposnum = 2

            self.glbnum = sensor.globalnum

            item = QTreeWidgetItem()
            item.setText(0,str(self.glbnum))
            item.setText(1,str(self.glbnum))
            self.root_sensor.child(self.typenum).child(int(bdnum)-1).child(self.bdposnum).addChild(item)

        self.treeWidget.clicked.connect(self.treeonClicked)
        self.treeWidget.expandAll()
    
    def treeonClicked(self):
        item = self.treeWidget.currentItem()
        try:
            self.selectsensor = int(item.text(1))
        except:
            pass
        
        # print('Key=%s,value=%s'%(item.text(0),item.text(1)))
        # print(item.text(1))
        


    @staticmethod
    def gen_branch(node: QTreeWidgetItem, texts: list):
        """ 给定某个节点和列表 在该节点生成列表内分支"""
        for text in texts:
            item = QTreeWidgetItem()
            item.setText(0, text)
            # item.setCheckState(0, Qt.Unchecked)
            node.addChild(item)



    def init_main_pg(self):
        self.dislist = []
        pg.setConfigOption('background', '#31363b')
        self.winwidth = 100
        self.main_pw = pg.GraphicsLayoutWidget()
        # self.main_pw = pg.GraphicsWindow()
        
        # self.main_p3 = pg.ViewBox()
        ax1 = pg.AxisItem(orientation='bottom')
        ax2 = pg.AxisItem(orientation='top')
        ax3 = pg.AxisItem(orientation='left')
        ax4 = pg.AxisItem(orientation='right')
        ax4.setTicks([''])
        ax2.setTicks([''])
        self.main_p1 = self.main_pw.addPlot(axisItems={'bottom':ax1,'top':ax2,'left':ax3,'right':ax4})
        self.main_p1.setLabel('bottom', "时间")
        self.main_p1.setLabel('left', "幅值")
        self.main_p1.setLabel('right', " ")
        self.main_p1.setLabel('top', " ")
        # self.main_p1.setYRange(0,100)
        self.main_p1.setXRange(0,self.winwidth)

        self.main_curve = self.main_p1.plot()

        self.page1_vl_graph.addWidget(self.main_pw)
        
        self.main_gif = QMovie('./images/ld5.gif')
        self.main_giflb.setMovie(self.main_gif)
        self.main_gif.start()
        self.main_giflb.setScaledContents(True)
        

    def eventbind(self):                                                    #事件绑定
        self.MainMenu_miBtn.clicked.connect(self.MainMenu_miBtn_clicked)    #主界面按钮绑定
        self.MainMenu_rtdBtn.clicked.connect(self.MainMenu_rtdBtn_clicked)  
        self.MainMenu_dnBtn.clicked.connect(self.MainMenu_dnBtn_clicked)
    
    def showtime_init(self):
        st_timer = QTimer(self)
        st_timer.timeout.connect(self.showtime)
        st_timer.start(1000)

    def eventFilter(self, watched, event):
        if watched == self.kz_strain_dc:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 1
                    self.sensorclicked_zh()
        if watched == self.kz_strain_pc:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 2
                    self.sensorclicked_zh()
        if watched == self.kz_strain_pl:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 3
                    self.sensorclicked_zh()
        if watched == self.kz_strain_pr:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 4
                    self.sensorclicked_zh()

        if watched == self.kr_strain_dcl:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 5
                    self.sensorclicked_r()
        if watched == self.kr_strain_dcr:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 6
                    self.sensorclicked_r()
        if watched == self.kr_strain_pc:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 2
                    self.sensorclicked_r()

        if watched == self.kr_strain_dc:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 1
                    self.sensorclicked_r()

        if watched == self.kr_strain_dl:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 7
                    self.sensorclicked_r()

        if watched == self.kr_strain_dr:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 8
                    self.sensorclicked_r()

        if watched == self.kl_strain_dc:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 1
                    self.sensorclicked_l()
        if watched == self.kl_strain_pc:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 2
                    self.sensorclicked_l()
        if watched == self.kl_strain_dl:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 7
                    self.sensorclicked_l()
        if watched == self.kl_strain_dr:
            if event.type() == QEvent.MouseButtonPress:
                mouseEvent = QMouseEvent(event)
                if mouseEvent.buttons() == Qt.LeftButton:
                    self.select_localsensornum = 8
                    self.sensorclicked_l()
        return QtWidgets.QMainWindow.eventFilter(self, watched, event)

    def cleartab(self):
        self.kz_strain_dc.hide()
        self.kz_strain_pc.hide()
        self.kz_strain_pl.hide()
        self.kz_strain_pr.hide()

        self.kr_strain_dcl.hide()
        self.kr_strain_dcr.hide()
        self.kr_strain_pc.hide()
        self.kr_strain_dr.hide()
        self.kr_strain_dl.hide()
        self.kr_strain_dc.hide()

        self.kl_strain_dc.hide()
        self.kl_strain_pc.hide()
        self.kl_strain_dl.hide()
        self.kl_strain_dr.hide()


    def init_tab(self):

        self.cleartab()
        #Tab 1
        pix_1 = QPixmap('./images/zl_cross1.png')
        self.pg1_tab_zhdm_lb.setPixmap(pix_1)
        self.pg1_tab_zhdm_lb.setScaledContents(True)

        pix = QPixmap('./images/strain_sensor.png')
        self.strain_lb.setPixmap(pix)
        self.strain_lb.setScaledContents(True)

        pix = QPixmap('./images/strain_sensor.png')
        self.kz_strain_dc.setPixmap(pix)
        self.kz_strain_dc.setScaledContents(True)
        self.kz_strain_dc.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kz_strain_pc.setPixmap(pix)
        self.kz_strain_pc.setScaledContents(True)
        self.kz_strain_pc.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kz_strain_pl.setPixmap(pix)
        self.kz_strain_pl.setScaledContents(True)
        self.kz_strain_pl.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kz_strain_pr.setPixmap(pix)
        self.kz_strain_pr.setScaledContents(True)
        self.kz_strain_pr.installEventFilter(self)

        # Tab 2
        pix_1 = QPixmap('./images/zl_cross1.png')
        self.pg1_tab_zdm_lb.setPixmap(pix_1)
        self.pg1_tab_zdm_lb.setScaledContents(True)

        pix = QPixmap('./images/strain_sensor.png')
        self.kr_strain_dcl.setPixmap(pix)
        self.kr_strain_dcl.setScaledContents(True)
        self.kr_strain_dcl.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kr_strain_dcr.setPixmap(pix)
        self.kr_strain_dcr.setScaledContents(True)
        self.kr_strain_dcr.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kr_strain_pc.setPixmap(pix)
        self.kr_strain_pc.setScaledContents(True)
        self.kr_strain_pc.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kr_strain_dc.setPixmap(pix)
        self.kr_strain_dc.setScaledContents(True)
        self.kr_strain_dc.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kr_strain_dcl.setPixmap(pix)
        self.kr_strain_dcl.setScaledContents(True)
        self.kr_strain_dcl.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kr_strain_dcr.setPixmap(pix)
        self.kr_strain_dcr.setScaledContents(True)
        self.kr_strain_dcr.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kr_strain_dl.setPixmap(pix)
        self.kr_strain_dl.setScaledContents(True)
        self.kr_strain_dl.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kr_strain_dr.setPixmap(pix)
        self.kr_strain_dr.setScaledContents(True)
        self.kr_strain_dr.installEventFilter(self)

        # Tab 3
        pix_1 = QPixmap('./images/zl_cross1.png')
        self.pg1_tab_ydm_lb.setPixmap(pix_1)
        self.pg1_tab_ydm_lb.setScaledContents(True)

        pix = QPixmap('./images/strain_sensor.png')
        self.kl_strain_dl.setPixmap(pix)
        self.kl_strain_dl.setScaledContents(True)
        self.kl_strain_dl.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kl_strain_dc.setPixmap(pix)
        self.kl_strain_dc.setScaledContents(True)
        self.kl_strain_dc.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kl_strain_dr.setPixmap(pix)
        self.kl_strain_dr.setScaledContents(True)
        self.kl_strain_dr.installEventFilter(self)

        pix = QPixmap('./images/strain_sensor.png')
        self.kl_strain_pc.setPixmap(pix)
        self.kl_strain_pc.setScaledContents(True)
        self.kl_strain_pc.installEventFilter(self)



        pix = QPixmap('./images/strain_sensor.png')
        self.strain_lb.setPixmap(pix)
        self.strain_lb.setScaledContents(True)

        pix = QPixmap('./images/img_cn1.png')
        self.cn1.setPixmap(pix)
        self.cn1.setScaledContents(True)

        pix = QPixmap('./images/img_cn2.png')
        self.cn2.setPixmap(pix)
        self.cn2.setScaledContents(True)

        pix = QPixmap('./images/img_cn3.png')
        self.cn3.setPixmap(pix)
        self.cn3.setScaledContents(True)

        pix = QPixmap('./images/img_cn4.png')
        self.cn4.setPixmap(pix)
        self.cn4.setScaledContents(True)

        pix = QPixmap('./images/img_cn1.png')
        self.pg1_cn1.setPixmap(pix)
        self.pg1_cn1.setScaledContents(True)

        pix = QPixmap('./images/img_cn2.png')
        self.pg1_cn2.setPixmap(pix)
        self.pg1_cn2.setScaledContents(True)

        pix = QPixmap('./images/img_cn3.png')
        self.pg1_cn3.setPixmap(pix)
        self.pg1_cn3.setScaledContents(True)

        pix = QPixmap('./images/img_cn4.png')
        self.pg1_cn4.setPixmap(pix)
        self.pg1_cn4.setScaledContents(True)

        pix = QPixmap('./images/img_cn1.png')
        self.pg1_cn1_2.setPixmap(pix)
        self.pg1_cn1_2.setScaledContents(True)

        pix = QPixmap('./images/img_cn2.png')
        self.pg1_cn2_2.setPixmap(pix)
        self.pg1_cn2_2.setScaledContents(True)

        pix = QPixmap('./images/img_cn3.png')
        self.pg1_cn3_2.setPixmap(pix)
        self.pg1_cn3_2.setScaledContents(True)

        pix = QPixmap('./images/img_cn4.png')
        self.pg1_cn4_2.setPixmap(pix)
        self.pg1_cn4_2.setScaledContents(True)

        pix = QPixmap('./images/img_cn1.png')
        self.pg1_cn1_3.setPixmap(pix)
        self.pg1_cn1_3.setScaledContents(True)

        pix = QPixmap('./images/img_cn2.png')
        self.pg1_cn2_3.setPixmap(pix)
        self.pg1_cn2_3.setScaledContents(True)

        pix = QPixmap('./images/img_cn3.png')
        self.pg1_cn3_3.setPixmap(pix)
        self.pg1_cn3_3.setScaledContents(True)

        pix = QPixmap('./images/img_cn4.png')
        self.pg1_cn4_3.setPixmap(pix)
        self.pg1_cn4_3.setScaledContents(True)

        # self.pg1_cam = QMovie('./images/cam.gif')
        # self.pg1_camlb.setMovie(self.pg1_cam)
        # self.pg1_cam.start()
        # self.pg1_camlb.setScaledContents(True)

    def sensorclicked_zh(self):
        sensor_index = str(self.select_blocknum)+ '_C_' + str(self.select_localsensornum)
        self.page1_selectsensorlb.setText(sensor_index)
        self.select_glbid = self.sensor_dict[sensor_index].globalnum
        self.displaydata()

    def sensorclicked_r(self):
        sensor_index = str(self.select_blocknum)+ '_R_' + str(self.select_localsensornum)
        self.page1_selectsensorlb.setText(sensor_index)
        self.select_glbid = self.sensor_dict[sensor_index].globalnum
        self.displaydata()

    def sensorclicked_l(self):
        sensor_index = str(self.select_blocknum)+ '_L_' + str(self.select_localsensornum)
        self.page1_selectsensorlb.setText(sensor_index)
        self.select_glbid = self.sensor_dict[sensor_index].globalnum
        self.displaydata()

    def displaydata(self):
        if host_glb == None:
            QMessageBox.about(self,"警告",'未连接数据库')
            return
            
        if len(qthread_pool):
            for item in qthread_pool:
                item.stop()
            qthread_pool.clear()
        
        self.last_date = time.strftime('%Y%m%d',time.localtime())
        self.table_name = 'LLH' + str('%03d' % self.select_glbid) + self.last_date
        self.con = get_conn(host_glb,port_glb,user_glb,pwd_glb,database_glb)
        # self.con1 = get_conn(host_glb,port_glb,user_glb,pwd_glb,database_glb)
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT id FROM `%s` order by id DESC limit 1;" % (self.table_name))
        self.lastid = int(self.cursor.fetchall()[0][0])
        self.cur_id = self.lastid
        self.dislist.clear()
        self.t1 = QTimer()
        self.t1.timeout.connect(self.update_plot)
        qthread_pool.append(self.t1)
        self.t1.start(100)

    def update_plot(self):

        self.cur_date = time.strftime('%Y%m%d',time.localtime())
        tbname = 'LLH' + str('%03d' % self.select_glbid) + self.cur_date
        if self.cur_date != self.last_date:
            self.last_date = self.cur_date
            self.lastid = 1
            self.cur_id = 1

        if len(self.dislist) <= self.winwidth:
            self.con1 = get_conn(host_glb,port_glb,user_glb,pwd_glb,database_glb)
            self.cursor1 = self.con1.cursor()
            cmd = "SELECT val FROM `%s` WHERE id = %i;" % (tbname,self.cur_id)
            # print(cmd)
            self.cursor1.execute(cmd)
            fetch_inf = self.cursor1.fetchall()
            if len(fetch_inf):
                val = fetch_inf[0][0]
                self.dislist.append(float(val))
                self.main_curve.setData(self.dislist)
                self.cur_id += 1
            self.cursor1.close()
            self.con1.close()
        else:
            self.dislist.clear()

    def showtime(self):
        date = QDate.currentDate()
        text = date.toString(Qt.ISODate)
        # print(text)
        self.lcdNumber_2.display(text)

        curtime = QTime.currentTime()
        text = curtime.toString()
        # print(text)
        self.lcdNumber.display(text)


        # print(text)

    def linkDBwindow(self):
        self.myshow3 = Sqlwindow()
        self.myshow3.show()
        self.myshow3.setStyleSheet(qssStyle2)

    def init_3d(self):
     
        reader_zl1 = vtk.vtkSTLReader()
        reader_zl1.SetFileName("./stl/zl_1.stl")
        reader_zl2 = vtk.vtkSTLReader()
        reader_zl2.SetFileName("./stl/zl_2.stl")
        reader_zl3 = vtk.vtkSTLReader()
        reader_zl3.SetFileName("./stl/zl_3.stl")
        reader_zl4 = vtk.vtkSTLReader()
        reader_zl4.SetFileName("./stl/zl_4.stl")
        reader_zl5 = vtk.vtkSTLReader()
        reader_zl5.SetFileName("./stl/zl_5.stl")
        reader_zl6 = vtk.vtkSTLReader()
        reader_zl6.SetFileName("./stl/zl_6.stl")
        reader_zl7 = vtk.vtkSTLReader()
        reader_zl7.SetFileName("./stl/zl_7.stl")
        reader_zl8 = vtk.vtkSTLReader()
        reader_zl8.SetFileName("./stl/zl_8.stl")
        reader_zl9 = vtk.vtkSTLReader()
        reader_zl9.SetFileName("./stl/zl_9.stl")
        reader_zl10 = vtk.vtkSTLReader()
        reader_zl10.SetFileName("./stl/zl_10.stl")
        reader_zl11 = vtk.vtkSTLReader()
        reader_zl11.SetFileName("./stl/zl_11.stl")

        reader_zz1 = vtk.vtkSTLReader()
        reader_zz1.SetFileName("./stl/zz_1.stl")
        reader_zz2 = vtk.vtkSTLReader()
        reader_zz2.SetFileName("./stl/zz_2.stl")
        reader_zz3 = vtk.vtkSTLReader()
        reader_zz3.SetFileName("./stl/zz_3.stl")
        reader_zz4 = vtk.vtkSTLReader()
        reader_zz4.SetFileName("./stl/zz_4.stl")
        reader_zz5 = vtk.vtkSTLReader()
        reader_zz5.SetFileName("./stl/zz_5.stl")
        reader_zz6 = vtk.vtkSTLReader()
        reader_zz6.SetFileName("./stl/zz_6.stl")
        reader_zz7 = vtk.vtkSTLReader()
        reader_zz7.SetFileName("./stl/zz_7.stl")
        reader_zz8 = vtk.vtkSTLReader()
        reader_zz8.SetFileName("./stl/zz_8.stl")
        reader_zz9 = vtk.vtkSTLReader()
        reader_zz9.SetFileName("./stl/zz_9.stl")
        reader_zz10 = vtk.vtkSTLReader()
        reader_zz10.SetFileName("./stl/zz_10.stl")
        reader_zz11 = vtk.vtkSTLReader()
        reader_zz11.SetFileName("./stl/zz_11.stl")
        reader_zz12 = vtk.vtkSTLReader()
        reader_zz12.SetFileName("./stl/zz_12.stl")

        reader_lg1 = vtk.vtkSTLReader()
        reader_lg1.SetFileName("./stl/lg_1.stl")
        reader_lg2 = vtk.vtkSTLReader()
        reader_lg2.SetFileName("./stl/lg_2.stl")

        reader_bj1 = vtk.vtkSTLReader()
        reader_bj1.SetFileName("./stl/bj_1.stl")
        reader_bj2 = vtk.vtkSTLReader()
        reader_bj2.SetFileName("./stl/bj_2.stl")

        reader_ab1 = vtk.vtkSTLReader()
        reader_ab1.SetFileName("./stl/ab_1.stl")
        reader_ab2 = vtk.vtkSTLReader()
        reader_ab2.SetFileName("./stl/ab_2.stl")
        reader_bz1 = vtk.vtkSTLReader()
        reader_bz1.SetFileName("./stl/bz_1.stl")
        reader_hl1 = vtk.vtkSTLReader()
        reader_hl1.SetFileName("./stl/hl_1.stl")

        #load mapper
        mapper_zl1 = vtk.vtkPolyDataMapper()
        mapper_zl2 = vtk.vtkPolyDataMapper()
        mapper_zl3 = vtk.vtkPolyDataMapper()
        mapper_zl4 = vtk.vtkPolyDataMapper()
        mapper_zl5 = vtk.vtkPolyDataMapper()
        mapper_zl6 = vtk.vtkPolyDataMapper()
        mapper_zl7 = vtk.vtkPolyDataMapper()
        mapper_zl8 = vtk.vtkPolyDataMapper()
        mapper_zl9 = vtk.vtkPolyDataMapper()
        mapper_zl10 = vtk.vtkPolyDataMapper()
        mapper_zl11 = vtk.vtkPolyDataMapper()

        mapper_zz1 = vtk.vtkPolyDataMapper()
        mapper_zz2 = vtk.vtkPolyDataMapper()
        mapper_zz3 = vtk.vtkPolyDataMapper()
        mapper_zz4 = vtk.vtkPolyDataMapper()
        mapper_zz5 = vtk.vtkPolyDataMapper()
        mapper_zz6 = vtk.vtkPolyDataMapper()
        mapper_zz7 = vtk.vtkPolyDataMapper()
        mapper_zz8 = vtk.vtkPolyDataMapper()
        mapper_zz9 = vtk.vtkPolyDataMapper()
        mapper_zz10 = vtk.vtkPolyDataMapper()
        mapper_zz11 = vtk.vtkPolyDataMapper()
        mapper_zz12 = vtk.vtkPolyDataMapper()

        mapper_lg1 = vtk.vtkPolyDataMapper()
        mapper_lg2 = vtk.vtkPolyDataMapper()

        mapper_bj1 = vtk.vtkPolyDataMapper()
        mapper_bj2 = vtk.vtkPolyDataMapper()

        mapper_ab1 = vtk.vtkPolyDataMapper()
        mapper_ab2 = vtk.vtkPolyDataMapper()
        mapper_bz1 = vtk.vtkPolyDataMapper()
        mapper_hl1 = vtk.vtkPolyDataMapper()

        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper_zl1.SetInput(reader_zl1.GetOutput())
            mapper_zl2.SetInput(reader_zl2.GetOutput())
            mapper_zl3.SetInput(reader_zl3.GetOutput())
            mapper_zl4.SetInput(reader_zl4.GetOutput())
            mapper_zl5.SetInput(reader_zl5.GetOutput())
            mapper_zl6.SetInput(reader_zl6.GetOutput())
            mapper_zl7.SetInput(reader_zl7.GetOutput())
            mapper_zl8.SetInput(reader_zl8.GetOutput())
            mapper_zl9.SetInput(reader_zl9.GetOutput())
            mapper_zl10.SetInput(reader_zl10.GetOutput())
            mapper_zl11.SetInput(reader_zl11.GetOutput())

            mapper_zz1.SetInput(reader_zz1.GetOutput())
            mapper_zz2.SetInput(reader_zz2.GetOutput())
            mapper_zz3.SetInput(reader_zz3.GetOutput())
            mapper_zz4.SetInput(reader_zz4.GetOutput())
            mapper_zz5.SetInput(reader_zz5.GetOutput())
            mapper_zz6.SetInput(reader_zz6.GetOutput())
            mapper_zz7.SetInput(reader_zz7.GetOutput())
            mapper_zz8.SetInput(reader_zz8.GetOutput())
            mapper_zz9.SetInput(reader_zz9.GetOutput())
            mapper_zz10.SetInput(reader_zz10.GetOutput())
            mapper_zz11.SetInput(reader_zz11.GetOutput())
            mapper_zz12.SetInput(reader_zz12.GetOutput())

            mapper_lg1.SetInput(reader_lg1.GetOutput())
            mapper_lg2.SetInput(reader_lg2.GetOutput())

            mapper_bj1.SetInput(reader_bj1.GetOutput())
            mapper_bj2.SetInput(reader_bj2.GetOutput())

            mapper_ab1.SetInput(reader_ab1.GetOutput())
            mapper_ab2.SetInput(reader_ab2.GetOutput())
            mapper_bz1.SetInput(reader_bz1.GetOutput())
            mapper_hl1.SetInput(reader_hl1.GetOutput())

        else:
            mapper_zl1.SetInputConnection(reader_zl1.GetOutputPort())
            mapper_zl2.SetInputConnection(reader_zl2.GetOutputPort())
            mapper_zl3.SetInputConnection(reader_zl3.GetOutputPort())
            mapper_zl4.SetInputConnection(reader_zl4.GetOutputPort())
            mapper_zl5.SetInputConnection(reader_zl5.GetOutputPort())
            mapper_zl6.SetInputConnection(reader_zl6.GetOutputPort())
            mapper_zl7.SetInputConnection(reader_zl7.GetOutputPort())
            mapper_zl8.SetInputConnection(reader_zl8.GetOutputPort())
            mapper_zl9.SetInputConnection(reader_zl9.GetOutputPort())
            mapper_zl10.SetInputConnection(reader_zl10.GetOutputPort())
            mapper_zl11.SetInputConnection(reader_zl11.GetOutputPort())

            mapper_zz1.SetInputConnection(reader_zz1.GetOutputPort())
            mapper_zz2.SetInputConnection(reader_zz2.GetOutputPort())
            mapper_zz3.SetInputConnection(reader_zz3.GetOutputPort())
            mapper_zz4.SetInputConnection(reader_zz4.GetOutputPort())
            mapper_zz5.SetInputConnection(reader_zz5.GetOutputPort())
            mapper_zz6.SetInputConnection(reader_zz6.GetOutputPort())
            mapper_zz7.SetInputConnection(reader_zz7.GetOutputPort())
            mapper_zz8.SetInputConnection(reader_zz8.GetOutputPort())
            mapper_zz9.SetInputConnection(reader_zz9.GetOutputPort())
            mapper_zz10.SetInputConnection(reader_zz10.GetOutputPort())
            mapper_zz11.SetInputConnection(reader_zz11.GetOutputPort())
            mapper_zz12.SetInputConnection(reader_zz12.GetOutputPort())

            mapper_lg1.SetInputConnection(reader_lg1.GetOutputPort())
            mapper_lg2.SetInputConnection(reader_lg2.GetOutputPort())

            mapper_bj1.SetInputConnection(reader_bj1.GetOutputPort())
            mapper_bj2.SetInputConnection(reader_bj2.GetOutputPort())

            mapper_ab1.SetInputConnection(reader_ab1.GetOutputPort())
            mapper_ab2.SetInputConnection(reader_ab2.GetOutputPort())
            mapper_bz1.SetInputConnection(reader_bz1.GetOutputPort())
            mapper_hl1.SetInputConnection(reader_hl1.GetOutputPort())

        #create actor
        actor_zl1 = vtk.vtkActor()
        actor_zl2 = vtk.vtkActor()
        actor_zl3 = vtk.vtkActor()
        actor_zl4 = vtk.vtkActor()
        actor_zl5 = vtk.vtkActor()
        actor_zl6 = vtk.vtkActor()
        actor_zl7 = vtk.vtkActor()
        actor_zl8 = vtk.vtkActor()
        actor_zl9 = vtk.vtkActor()
        actor_zl10 = vtk.vtkActor()
        actor_zl11 = vtk.vtkActor()

        actor_zz1 = vtk.vtkActor()
        actor_zz2 = vtk.vtkActor()
        actor_zz3 = vtk.vtkActor()
        actor_zz4 = vtk.vtkActor()
        actor_zz5 = vtk.vtkActor()
        actor_zz6 = vtk.vtkActor()
        actor_zz7 = vtk.vtkActor()
        actor_zz8 = vtk.vtkActor()
        actor_zz9 = vtk.vtkActor()
        actor_zz10 = vtk.vtkActor()
        actor_zz11 = vtk.vtkActor()
        actor_zz12 = vtk.vtkActor()

        actor_lg1 = vtk.vtkActor()
        actor_lg2 = vtk.vtkActor()

        actor_bj1 = vtk.vtkActor()
        actor_bj2 = vtk.vtkActor()

        actor_ab1 = vtk.vtkActor()
        actor_ab2 = vtk.vtkActor()
        actor_bz1 = vtk.vtkActor()
        actor_hl1 = vtk.vtkActor()

        actor_zl1.SetMapper(mapper_zl1)
        actor_zl2.SetMapper(mapper_zl2)
        actor_zl3.SetMapper(mapper_zl3)
        actor_zl4.SetMapper(mapper_zl4)
        actor_zl5.SetMapper(mapper_zl5)
        actor_zl6.SetMapper(mapper_zl6)
        actor_zl7.SetMapper(mapper_zl7)
        actor_zl8.SetMapper(mapper_zl8)
        actor_zl9.SetMapper(mapper_zl9)
        actor_zl10.SetMapper(mapper_zl10)
        actor_zl11.SetMapper(mapper_zl11)

        actor_zz1.SetMapper(mapper_zz1)
        actor_zz2.SetMapper(mapper_zz2)
        actor_zz3.SetMapper(mapper_zz3)
        actor_zz4.SetMapper(mapper_zz4)
        actor_zz5.SetMapper(mapper_zz5)
        actor_zz6.SetMapper(mapper_zz6)
        actor_zz7.SetMapper(mapper_zz7)
        actor_zz8.SetMapper(mapper_zz8)
        actor_zz9.SetMapper(mapper_zz9)
        actor_zz10.SetMapper(mapper_zz10)
        actor_zz11.SetMapper(mapper_zz11)
        actor_zz12.SetMapper(mapper_zz12)

        actor_lg1.SetMapper(mapper_lg1)
        actor_lg2.SetMapper(mapper_lg2)

        actor_bj1.SetMapper(mapper_bj1)
        actor_bj2.SetMapper(mapper_bj2)

        actor_ab1.SetMapper(mapper_ab1)
        actor_ab2.SetMapper(mapper_ab2)
        actor_bz1.SetMapper(mapper_bz1)
        actor_hl1.SetMapper(mapper_hl1)

        #set color
        zl_odd_color_r = 100/255
        zl_odd_color_g = 0/255
        zl_odd_color_b = 230/255

        zl_even_color_r = 0/255
        zl_even_color_g = 255/255
        zl_even_color_b = 0/255

        actor_zl1.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
        actor_zl3.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
        actor_zl5.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
        actor_zl7.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
        actor_zl9.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
        actor_zl11.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)

        actor_zl2.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)
        actor_zl4.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)
        actor_zl6.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)
        actor_zl8.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)
        actor_zl10.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)

        actor_lg1.GetProperty().SetColor(255/255,0/255,0/255)
        actor_lg2.GetProperty().SetColor(255/255,0/255,0/255)

        actor_bj1.GetProperty().SetColor(150/255,70/255,50/255)
        actor_bj2.GetProperty().SetColor(150/255,70/255,50/255)

        actor_ab1.GetProperty().SetColor(209/255,170/255,52/255)
        actor_ab2.GetProperty().SetColor(209/255,170/255,52/255)
        actor_bz1.GetProperty().SetColor(225/255,111/255,0/255)
        actor_hl1.GetProperty().SetColor(30/255,144/255,255/255)
        
        # Create a rendering window and renderer
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(49/255, 54/255, 59/255)
        # self.ren.SetBackground2(25/255, 50/255, 100/255)
        # self.ren.SetGradientBackground(1)

        self.vtk_widget = QVTKWidget(self.page1_widget)
        self.page1_vlayout.addWidget(self.vtk_widget)

        #
        # axes = vtk.vtkAxesActor() 
        # axes.SetTotalLength(100, 100, 100)  # Set the total length of the axes in 3 dimensions 
        # # Set the type of the shaft to a cylinder:0, line:1, or user defined geometry. 
        # axes.SetShaftType(0) 
        # axes.SetCylinderRadius(0.02) 
        # axes.SetAxisLabels(0) 
        # self.ren.AddActor(axes)

        #


        self.renWin = self.vtk_widget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)

        self.renWin.SetSize(20000,20000)
        self.renWin.Render()
        iren = self.renWin.GetInteractor()
        # iren.SetRenderWindow(renWin)
        
        # Assign actor to the renderer
        self.ren.AddActor(actor_zl1)
        self.ren.AddActor(actor_zl2)
        self.ren.AddActor(actor_zl3)
        self.ren.AddActor(actor_zl4)
        self.ren.AddActor(actor_zl5)
        self.ren.AddActor(actor_zl6)
        self.ren.AddActor(actor_zl7)
        self.ren.AddActor(actor_zl8)
        self.ren.AddActor(actor_zl9)
        self.ren.AddActor(actor_zl10)
        self.ren.AddActor(actor_zl11)

        self.ren.AddActor(actor_zz1)
        self.ren.AddActor(actor_zz2)
        self.ren.AddActor(actor_zz3)
        self.ren.AddActor(actor_zz4)
        self.ren.AddActor(actor_zz5)
        self.ren.AddActor(actor_zz6)
        self.ren.AddActor(actor_zz7)
        self.ren.AddActor(actor_zz8)
        self.ren.AddActor(actor_zz9)
        self.ren.AddActor(actor_zz10)
        self.ren.AddActor(actor_zz11)
        self.ren.AddActor(actor_zz12)

        self.ren.AddActor(actor_lg1)
        self.ren.AddActor(actor_lg2)

        self.ren.AddActor(actor_bj1)
        self.ren.AddActor(actor_bj2)

        self.ren.AddActor(actor_ab1)
        self.ren.AddActor(actor_ab2)
        self.ren.AddActor(actor_bz1)
        self.ren.AddActor(actor_hl1)

        self.actor_zl1_inf = str(actor_zl1.GetMapper().GetInformation())[16:32]
        self.actor_zl2_inf = str(actor_zl2.GetMapper().GetInformation())[16:32]
        self.actor_zl3_inf = str(actor_zl3.GetMapper().GetInformation())[16:32]
        self.actor_zl4_inf = str(actor_zl4.GetMapper().GetInformation())[16:32]
        self.actor_zl5_inf = str(actor_zl5.GetMapper().GetInformation())[16:32]
        self.actor_zl6_inf = str(actor_zl6.GetMapper().GetInformation())[16:32]
        self.actor_zl7_inf = str(actor_zl7.GetMapper().GetInformation())[16:32]
        self.actor_zl8_inf = str(actor_zl8.GetMapper().GetInformation())[16:32]
        self.actor_zl9_inf = str(actor_zl9.GetMapper().GetInformation())[16:32]
        self.actor_zl10_inf = str(actor_zl10.GetMapper().GetInformation())[16:32]
        self.actor_zl11_inf = str(actor_zl11.GetMapper().GetInformation())[16:32]

        self.actor2inf_dic = {}

        self.actor2inf_dic.update({self.actor_zl1_inf:'1'})
        self.actor2inf_dic.update({self.actor_zl2_inf:'2'})
        self.actor2inf_dic.update({self.actor_zl3_inf:'3'})
        self.actor2inf_dic.update({self.actor_zl4_inf:'4'})
        self.actor2inf_dic.update({self.actor_zl5_inf:'5'})
        self.actor2inf_dic.update({self.actor_zl6_inf:'6'})
        self.actor2inf_dic.update({self.actor_zl7_inf:'7'})
        self.actor2inf_dic.update({self.actor_zl8_inf:'8'})
        self.actor2inf_dic.update({self.actor_zl9_inf:'9'})
        self.actor2inf_dic.update({self.actor_zl10_inf:'10'})
        self.actor2inf_dic.update({self.actor_zl11_inf:'11'})

        camera = vtk.vtkCamera()
        camera.SetPosition(0.1,0.1,0)
        camera.SetFocalPoint(0,0,0)

        mylight = vtk.vtkLight()
        mylight.SetPosition(1,1,0)
        mylight.SetFocalPoint(0,0,0)
        self.ren.AddLight(mylight)

        self.ren.SetActiveCamera(camera)
        self.ren.ResetCamera()

        camera.Zoom(3)

        self.style = vtk.vtkInteractorStyleTrackballCamera()
        iren.SetInteractorStyle(self.style)
        
        iren.Initialize()

        self.picker = vtk.vtkCellPicker()
        self.picker.AddObserver("EndPickEvent", self.pickerfunc)     #将事件与回调函数建立连接
        self.style.AddObserver ('RightButtonReleaseEvent', self.pickerfunc)
        self.style.AddObserver ('RightButtonPressEvent', self.pickerfunc)

        iren.SetPicker(self.picker)


    def pickerfunc(self,object, event):
        #style = clientdata;
        
        # print(event)
        if event == 'RightButtonReleaseEvent':
            clickPos = self.style.GetInteractor().GetEventPosition()
            self.picker.Pick(clickPos[0], clickPos[1], 0, self.ren)
            actor = self.picker.GetActor()
            actor_inf = str(actor.GetMapper().GetInformation())[16:32]
            try:
                selectedid = self.actor2inf_dic[actor_inf]
                self.page1_disp(int(selectedid))
            except:
                pass
            
            self.renWin.Render()

    def page1_disp(self,sltid):
        self.page1_selectbridgelb.setText('当前选择第  '+str(sltid)+'  跨')
        self.select_blocknum = sltid
        self.cleartab()
        #1-11中跨 1,2,3,4,应变
        self.kz_strain_dc.show()
        self.kz_strain_pc.show()
        self.kz_strain_pl.show()
        self.kz_strain_pr.show()

        if self.select_blocknum == 6:
            self.kl_strain_dc.show()
            self.kl_strain_dl.show()
            self.kl_strain_pc.show()
            self.kl_strain_dr.show()

            self.kr_strain_dc.show()
            self.kr_strain_dl.show()
            self.kr_strain_pc.show()
            self.kr_strain_dr.show()

        if self.select_blocknum == 11:
            self.kr_strain_dcl.show()
            self.kr_strain_dcr.show()
            self.kr_strain_pc.show()


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

    # myshow2 = MyWindow2()
    styleFile2 = './secondwin.qss'
    qssStyle2 = CommonHelper.readQss(styleFile2)
    # qssStyle2 = qdarkstyle.load_stylesheet_pyqt5()
    # myshow2.setStyleSheet(qssStyle2)
    # myshow2.show()
    # myshow.btn1.clicked.connect(myshow2.show)
    # myshow.hide()

    styleFile = './winstyle.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    # qssStyle = qdarkstyle.load_stylesheet_pyqt5()
    myshow.setStyleSheet(qssStyle)

    

    myshow.show()
    sys.exit(app.exec())