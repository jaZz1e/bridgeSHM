#jazzy 2020.11.13 inital version @Shenyang
#jazzy 2020.11.27 update version @Dalian

import Ui_LoginWin,Ui_inputSQLinf,Ui_BridgeSelectWin,Ui_llhBridgeWin
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel,QThread,QTimer,QDateTime, QDate, QTime, Qt, QEvent
from PyQt5.QtGui import QPixmap, QImage, QMovie, QMouseEvent
from PyQt5.QtWidgets import QGraphicsPixmapItem,QGraphicsScene,QMessageBox,QTreeWidgetItem,QMenu,QAction
import sys
import pyqtgraph as pg
import MySQLdb
import queue
import time
import numpy as np
import vtk
import threading
import cv2
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget

#定义数据库全局变量
conn_glb = None

host_glb = None
port_glb = None
user_glb = None
pwd_glb = None
database_glb = None

#定义登录名数据字典
userdict = {}

qthread_pool = []

def createSelectWin():
    selectBridgeWin = SelectBridgeWindow()
    selectBridgeWin.show()

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


#主窗口
class LoginWindow(QtWidgets.QMainWindow,Ui_LoginWin.Ui_MainWindow):
    def __init__(self):
        super(LoginWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("桥梁健康监测子系统")
        self.loginWinInit()

    def loginWinInit(self):

        self.qssSet()
        self.eventbind()

    def qssSet(self):

        styleFile = './loginWidget.qss'
        qssStyle = CommonHelper.readQss(styleFile)
        self.loginWidget.setStyleSheet(qssStyle)

    def eventbind(self):

        self.loginBtn.clicked.connect(self.loginOp)
        self.conSQLBtn.clicked.connect(self.conSQLOp)

    def loginOp(self):
        if host_glb == None:
            QMessageBox.about(self,"警告",'未连接数据库')
            return
        
        self.con1 = get_conn(host_glb,port_glb,user_glb,pwd_glb,database_glb)
        self.cursor1 = self.con1.cursor()

        usernameInput = self.userInputBox.text()
        passwordInput = self.pwdInputBox.text()

        cmd = "SELECT `password` FROM `usertable` WHERE `username`='%s';" % (usernameInput)
        self.cursor1.execute(cmd)
        ret = self.cursor1.fetchall()
        if not len(ret):
            QMessageBox.about(self,"警告",'用户名不存在')
            self.con1.close()
            return
        else:
            if passwordInput == ret[0][0]:
                QMessageBox.about(self,"警告",'登录成功')

                cmd = "SELECT * FROM `usertable` WHERE `username`='%s';" % (usernameInput)
                self.cursor1.execute(cmd)
                ret = self.cursor1.fetchall()
                username = ret[0][0]
                authority = ret[0][2]
                name = ret[0][3]
                department = ret[0][4]
                position = ret[0][5]
                email = ret[0][6]
                wechat = ret[0][7]

                userdict.update({'username':username})
                userdict.update({'authority':authority})
                userdict.update({'name':name})
                userdict.update({'department':department})
                userdict.update({'position':position})
                userdict.update({'email':email})
                userdict.update({'wechat':wechat})

                # createSelectWin()
                self.selectBridgeWin = SelectBridgeWindow()
                styleFile = './selectBridge.qss'
                qssStyle = CommonHelper.readQss(styleFile)
                self.selectBridgeWin.setStyleSheet(qssStyle)
                self.selectBridgeWin.show()
                self.con1.close()
                return
            else:
                QMessageBox.about(self,"警告",'密码错误')
                self.con1.close()
                return

    def conSQLOp(self):
        self.sqlSetWin = Sqlwindow()
        self.sqlSetWin.show()

#数据库设置窗口
class Sqlwindow(QtWidgets.QMainWindow,Ui_inputSQLinf.Ui_MainWindow):
    def __init__(self):
        super(Sqlwindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("数据库设置")
        self.btnBind()
    
    def btnBind(self):
        self.testconBtn.clicked.connect(self.testConOp)
        self.confirmBtn.clicked.connect(self.confirmOp)
        self.canBtn.clicked.connect(self.canOp)

    def confirmOp(self):

        self.host = self.hostEdit.text()
        port = self.portEdit.text()
        try:
            self.port = int(port)
        except:
            QMessageBox.about(self,"警告",'输入错误：port')
            return
        self.user = self.userEdit.text()
        self.pwd = self.pwdEdit.text()
        self.database = self.dbEdit.text()

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
    
    def canOp(self):
        self.close()

    
    def testConOp(self):
        host = self.hostEdit.text()
        port = self.portEdit.text()
        try:
            port = int(port)
        except:
            QMessageBox.about(self,"警告",'输入错误：port')
            return
        user = self.userEdit.text()
        pwd = self.pwdEdit.text()
        database = self.dbEdit.text()


        try:
            self.con = get_conn(host,port,user,pwd,database)
            cursor = self.con.cursor()
            self.tipLabel.setText('测试成功')
            self.con.close()
        
        except:
            self.tipLabel.setText('测试失败')
            return

#桥梁选择窗口
class SelectBridgeWindow(QtWidgets.QMainWindow,Ui_BridgeSelectWin.Ui_MainWindow):
    def __init__(self):
        super(SelectBridgeWindow,self).__init__()
        self.setupUi(self)
        self.winInit()

    def winInit(self):
        self.thqBtn.clicked.connect(self.thqSelect)
        self.llhqBtn.clicked.connect(self.llhSelect)

    def thqSelect(self):
        pass

    def llhSelect(self):
        self.llhwin = LlhWin()
        styleFile = './llhBridge.qss'
        qssStyle = CommonHelper.readQss(styleFile)
        self.llhwin.setStyleSheet(qssStyle)
        self.llhwin.show()

#拉林河窗口
class LlhWin(QtWidgets.QMainWindow,Ui_llhBridgeWin.Ui_MainWindow):
    def __init__(self):
        super(LlhWin,self).__init__()
        self.setupUi(self)
        self.paraInit()
        self.sensor_init()
        self.winInit()
        self.eventBind()

    def paraInit(self):
        self.realTimeSelectType = 1
        self.realTimeSelectBlock = 1

    def winInit(self):
        self.model3dInit()
        self.displayDataInit()
        self.displayCrossInit()
        self.rtpgInit()
        self.treeWidgetInit()
        self.calinit()
        self.pg2disinit()
        self.showtimeInit()
        self.stateInit()
        self.cameraInit()

        self.historyDisBtn.clicked.connect(self.pg2display)
        self.userinf.setText('当前用户：'+userdict['username'])

        self.selectSensorTypeCB.addItems(['应变','裂缝','加速度'])
        self.selectSensorTypeCB.currentIndexChanged.connect(self.cbSelectionChange)

    def stateInit(self):
        self.stateLabel.setText('良好')
        self.stateLabel.setStyleSheet("color:#00FF00;font-weight:bold;")

    def pg2disinit(self):
        # pg.setConfigOption('background', '#31363b')
        self.main_pw2 = pg.GraphicsLayoutWidget()
        self.main_p2 = self.main_pw2.addPlot(row=0,col=0)
        self.main_p2.setLabel('bottom', "时间")
        self.main_p2.setLabel('left', "幅值")

        self.main_curve2 = self.main_p2.plot()

        self.historyLayout.addWidget(self.main_pw2)

    def pg2display(self):

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
        self.display3 = [float(x[0]) for x in fetch_inf]
        self.display3.reverse()
        self.main_curve2.setData(self.display3)
        con.close()
    
    def cbSelectionChange(self):
        if self.selectSensorTypeCB.currentText() == '应变':
            self.realTimeSelectType = 1
        elif self.selectSensorTypeCB.currentText() == '裂缝':
            self.realTimeSelectType = 2
        elif self.selectSensorTypeCB.currentText() == '加速度':
            self.realTimeSelectType = 3
        self.crossUpdate()

    def treeWidgetInit(self):
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
            elif sensor.type == 'crack':
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

    @staticmethod
    def gen_branch(node: QTreeWidgetItem, texts: list):
        for text in texts:
            item = QTreeWidgetItem()
            item.setText(0, text)
            # item.setCheckState(0, Qt.Unchecked)
            node.addChild(item)
    
    def calinit(self):
        self.selectdate = time.strftime('%Y%m%d',time.localtime())
        self.calendarWidget.selectionChanged.connect(self.changeDate)
    
    def changeDate(self):
        self.selectdate = self.calendarWidget.selectedDate().toString("yyyyMMdd")

    def add_sensor(self, _type, bdpos, pos, lcnum):
        index = str(bdpos) + pos + str(lcnum)
        sensor = Sensor(_type, self.num_cnt, index)
        self.sensor_dict.update({index: sensor})
        self.sensor_index.update({self.num_cnt: sensor})
        self.num_cnt += 1

    def sensor_init(self):
        self.sensor_dict = {}
        self.sensor_index = {}

        self.strain_cross = []
        self.strain_cross.append([[1,2,3,4],[],[2,5,6]])    #block1 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block2 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block3 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block4 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block5 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[1,2,7,8],[1,2,7,8]]) #block6 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block7 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block8 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block9 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block10 kz-kn-kb
        self.strain_cross.append([[1,2,3,4],[],[]])         #block11 kz-kn-kb

        self.crack_cross = []
        self.crack_cross.append([[],[],[9]])                #block1 kz-kn-kb
        self.crack_cross.append([[],[9],[9,10]])            #block2 kz-kn-kb
        self.crack_cross.append([[11],[9,10],[9,10]])       #block3 kz-kn-kb
        self.crack_cross.append([[],[],[9]])                #block4 kz-kn-kb
        self.crack_cross.append([[],[9,10],[9,10]])         #block5 kz-kn-kb
        self.crack_cross.append([[],[9],[9]])               #block6 kz-kn-kb
        self.crack_cross.append([[12],[9],[10]])            #block7 kz-kn-kb
        self.crack_cross.append([[],[],[9,10]])             #block8 kz-kn-kb
        self.crack_cross.append([[11],[9],[9,10]])          #block9 kz-kn-kb
        self.crack_cross.append([[12],[9],[]])              #block10 kz-kn-kb
        self.crack_cross.append([[11,12],[],[10]])          #block11 kz-kn-kb
        

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
        self.add_sensor('strain', 1, '_R_', 2)
        self.add_sensor('strain', 1, '_R_', 5)
        self.add_sensor('strain', 1, '_R_', 6)

        #crack sensor init
        self.add_sensor('crack', 1, '_R_', 9)   #1-1

        self.add_sensor('crack', 2, '_L_', 9)   #2-2

        self.add_sensor('crack', 2, '_R_', 9)   #3-3
        self.add_sensor('crack', 2, '_R_', 10) 

        self.add_sensor('crack', 3, '_L_', 9)   #4-4
        self.add_sensor('crack', 3, '_L_', 10)

        self.add_sensor('crack', 3, '_C_', 11)  #5-5

        self.add_sensor('crack', 3, '_R_', 9)   #6-6
        self.add_sensor('crack', 3, '_R_', 10)        

        self.add_sensor('crack', 4, '_R_', 9)   #7-7

        self.add_sensor('crack', 5, '_L_', 9)   #8-8
        self.add_sensor('crack', 5, '_L_', 10)  

        self.add_sensor('crack', 5, '_R_', 9)   #9-9
        self.add_sensor('crack', 5, '_R_', 10)

        self.add_sensor('crack', 6, '_L_', 9)   #10-10

        self.add_sensor('crack', 6, '_R_', 9)   #11-11

        self.add_sensor('crack', 7, '_L_', 9)   #12-12

        self.add_sensor('crack', 7, '_C_', 12)  #13-13

        self.add_sensor('crack', 7, '_R_', 10)  #14-14

        self.add_sensor('crack', 8, '_R_', 9)   #15-15
        self.add_sensor('crack', 8, '_R_', 10)

        self.add_sensor('crack', 9, '_L_', 9)   #16-16

        self.add_sensor('crack', 9, '_C_', 11)  #17-17

        self.add_sensor('crack', 9, '_R_', 9)   #18-18
        self.add_sensor('crack', 9, '_R_', 10)

        self.add_sensor('crack', 10, '_L_', 9)  #19-19

        self.add_sensor('crack', 10, '_C_', 12) #20-20

        self.add_sensor('crack', 11, '_C_', 11) #21-21
        self.add_sensor('crack', 11, '_C_', 12)

        self.add_sensor('crack', 11, '_R_', 10) #22-22


    def eventBind(self):
        self.realTimeBtn.clicked.connect(self.realTimeOp)
        self.dataPreProcBtn.clicked.connect(self.dataPreProcOp)
        self.consDiagBtn.clicked.connect(self.consDiagOp)
        self.warnInfBtn.clicked.connect(self.warnInfOp)
        self.userManBtn.clicked.connect(self.userManOp)
        self.printRepBtn.clicked.connect(self.printRepOp)
        self.exitBtn.clicked.connect(self.exitOp)
        self.threeDimBtn.clicked.connect(self.threeDimOp)
        self.sensorDataBtn.clicked.connect(self.sensorDataOp)
        self.historyDataBtn.clicked.connect(self.historyDataOp)
    
    def threeDimOp(self):
        self.disStackedWidget.setCurrentIndex(0)
    
    def sensorDataOp(self):
        self.disStackedWidget.setCurrentIndex(1)
    
    def historyDataOp(self):
        self.disStackedWidget.setCurrentIndex(2)


    def realTimeOp(self):
        self.mainStackedWidget.setCurrentIndex(0)

    def dataPreProcOp(self):
        self.mainStackedWidget.setCurrentIndex(1)

    def consDiagOp(self):
        self.mainStackedWidget.setCurrentIndex(2)

    def warnInfOp(self):
        pass

    def userManOp(self):
        pass

    def printRepOp(self):
        pass

    def exitOp(self):
        pass
    
    def displayDataInit(self):
        # pix = QPixmap('./images/bridgeView.png')
        # self.bridgeViewLabel.setPixmap(pix)
        # self.bridgeViewLabel.setScaledContents(True)
        self.selectedid = 0

        self.blockList = []
        self.blockList.append(self.block1Label)
        self.blockList.append(self.block2Label)
        self.blockList.append(self.block3Label)
        self.blockList.append(self.block4Label)
        self.blockList.append(self.block5Label)
        self.blockList.append(self.block6Label)
        self.blockList.append(self.block7Label)
        self.blockList.append(self.block8Label)
        self.blockList.append(self.block9Label)
        self.blockList.append(self.block10Label)
        self.blockList.append(self.block11Label)

        main_gif = QMovie('./images/sensor2.gif')
        for item in self.blockList:
            item.setMovie(main_gif)
            # item.resize(40,40)
        
        main_gif.start()
        for item in self.blockList:
            item.setScaledContents(True)
            item.installEventFilter(self)

    def eventFilter(self, watched, event):
        for i in range(len(self.blockList)):
            if watched == self.blockList[i]:
                if event.type() == QEvent.MouseButtonPress:
                    mouseEvent = QMouseEvent(event)
                    if mouseEvent.buttons() == Qt.LeftButton:
                        self.realTimeSelectBlock = i+1
                        self.crossUpdate()

        for i in range(len(self.kzLabelList)):
            if watched == self.kzLabelList[i]:
                if event.type() == QEvent.MouseButtonPress:
                    mouseEvent = QMouseEvent(event)
                    if mouseEvent.buttons() == Qt.LeftButton:
                        self.select_localsensornum = i+1
                        self.select_pos = '_C_'
                        self.rtdisplay()
        
        for i in range(len(self.knLabelList)):
            if watched == self.knLabelList[i]:
                if event.type() == QEvent.MouseButtonPress:
                    mouseEvent = QMouseEvent(event)
                    if mouseEvent.buttons() == Qt.LeftButton:
                        self.select_localsensornum = i+1
                        self.select_pos = '_L_'
                        self.rtdisplay()
        
        for i in range(len(self.kbLabelList)):
            if watched == self.kbLabelList[i]:
                if event.type() == QEvent.MouseButtonPress:
                    mouseEvent = QMouseEvent(event)
                    if mouseEvent.buttons() == Qt.LeftButton:
                        self.select_localsensornum = i+1
                        self.select_pos = '_R_'
                        self.rtdisplay()

        return QtWidgets.QMainWindow.eventFilter(self, watched, event)

    def rtdisplay(self):
        sensor_index = str(self.realTimeSelectBlock)+ self.select_pos + str(self.select_localsensornum)
        self.select_glbid = self.sensor_dict[sensor_index].globalnum
        settext = '当前选择第%s跨 第%s号传感器'%(self.realTimeSelectBlock,self.select_glbid)
        self.infLabelKZ.setText(settext)
        self.infLabelKN.setText(settext)
        self.infLabelKB.setText(settext)

        if host_glb == None:
            QMessageBox.about(self,"警告",'未连接数据库')
            return
            
        if len(qthread_pool):
            for item in qthread_pool:
                item.stop()
            qthread_pool.clear()

        self.dislist.clear()
        self.t1 = QTimer()
        self.t1.timeout.connect(self.update_plot)
        qthread_pool.append(self.t1)
        self.t1.start(1000)

    def update_plot(self):
        print(1)

        self.last_date = time.strftime('%Y%m%d',time.localtime())
        self.table_name = 'LLH' + str('%03d' % self.select_glbid) + self.last_date

        self.con2 = get_conn(host_glb,port_glb,user_glb,pwd_glb,database_glb)
        self.cursor2 = self.con2.cursor()
        self.cursor2.execute("SELECT id FROM `%s` order by id DESC limit 1;" % (self.table_name))
        self.lastid = int(self.cursor2.fetchall()[0][0])

        if self.lastid < self.winwidth:
            self.cursor2.execute("SELECT val FROM `%s` order by id DESC limit %s;" % (self.table_name,str(self.lastid)))
        else:
            self.cursor2.execute("SELECT val FROM `%s` order by id DESC limit %s;" % (self.table_name,str(self.winwidth)))
        fetch_inf = self.cursor2.fetchall()
        self.display2 = [float(x[0]) for x in fetch_inf]
        self.display2.reverse()
        self.main_curve.setData(self.display2)
        self.con2.close()


    def rtpgInit(self):
        self.dislist = []
        pg.setConfigOption('background', (54, 80, 167,0))
        pg.setConfigOption('foreground', (255, 255, 255))
        self.winwidth = 200
        self.main_pw = pg.GraphicsLayoutWidget()

        self.main_p1 = self.main_pw.addPlot(row=0,col=0)
        self.main_p1.setLabel('bottom', "时间")
        self.main_p1.setLabel('left', "幅值")
        # self.main_p1.setYRange(0,100)
        self.main_p1.setXRange(0,self.winwidth)

        self.main_curve = self.main_p1.plot()

        self.rtpglayout.addWidget(self.main_pw)

    def clearTab(self):
        for item in self.kzLabelList:
            item.hide()
        for item in self.knLabelList:
            item.hide()
        for item in self.kbLabelList:
            item.hide()

    def crossUpdate(self):
        self.clearTab()
        if self.realTimeSelectType == 1:            #strain
            dislist = self.strain_cross[self.realTimeSelectBlock-1]
            kzList = dislist[0]
            knList = dislist[1]
            kbList = dislist[2]
            # print(self.kzLabelList)
            # print(kzList)
            if len(kzList):
                for i in kzList:
                    self.kzLabelList[i-1].show()
            if len(knList):
                for i in knList:
                    self.knLabelList[i-1].show()
            if len(kbList):
                for i in kbList:
                    self.kbLabelList[i-1].show()
        elif self.realTimeSelectType == 2:            #strain
            dislist = self.crack_cross[self.realTimeSelectBlock-1]
            kzList = dislist[0]
            knList = dislist[1]
            kbList = dislist[2]
            # print(self.kzLabelList)
            # print(kzList)
            if len(kzList):
                for i in kzList:
                    self.kzLabelList[i-1].show()
            if len(knList):
                for i in knList:
                    self.knLabelList[i-1].show()
            if len(kbList):
                for i in kbList:
                    self.kbLabelList[i-1].show()

    def displayCrossInit(self):

        self.kzLabelList = []
        self.kbLabelList = []
        self.knLabelList = []
        self.kzLabelList.append(self.kzLabel1)
        self.kzLabelList.append(self.kzLabel2)
        self.kzLabelList.append(self.kzLabel3)
        self.kzLabelList.append(self.kzLabel4)
        self.kzLabelList.append(self.kzLabel5)
        self.kzLabelList.append(self.kzLabel6)
        self.kzLabelList.append(self.kzLabel7)
        self.kzLabelList.append(self.kzLabel8)
        self.kzLabelList.append(self.kzLabel9)
        self.kzLabelList.append(self.kzLabel10)
        self.kzLabelList.append(self.kzLabel11)
        self.kzLabelList.append(self.kzLabel12)

        self.kbLabelList.append(self.kbLabel1)
        self.kbLabelList.append(self.kbLabel2)
        self.kbLabelList.append(self.kbLabel3)
        self.kbLabelList.append(self.kbLabel4)
        self.kbLabelList.append(self.kbLabel5)
        self.kbLabelList.append(self.kbLabel6)
        self.kbLabelList.append(self.kbLabel7)
        self.kbLabelList.append(self.kbLabel8)
        self.kbLabelList.append(self.kbLabel9)
        self.kbLabelList.append(self.kbLabel10)
        self.kbLabelList.append(self.kbLabel11)
        self.kbLabelList.append(self.kbLabel12)

        self.knLabelList.append(self.knLabel1)
        self.knLabelList.append(self.knLabel2)
        self.knLabelList.append(self.knLabel3)
        self.knLabelList.append(self.knLabel4)
        self.knLabelList.append(self.knLabel5)
        self.knLabelList.append(self.knLabel6)
        self.knLabelList.append(self.knLabel7)
        self.knLabelList.append(self.knLabel8)
        self.knLabelList.append(self.knLabel9)
        self.knLabelList.append(self.knLabel10)
        self.knLabelList.append(self.knLabel11)
        self.knLabelList.append(self.knLabel12)


        pix = QPixmap('./images/zl_cross1.png')
        self.crossLabelKZ.setPixmap(pix)
        self.crossLabelKZ.setScaledContents(True)
        self.crossLabelKN.setPixmap(pix)
        self.crossLabelKN.setScaledContents(True)
        self.crossLabelKB.setPixmap(pix)
        self.crossLabelKB.setScaledContents(True)

        pix = QPixmap('./images/sensor.png')
        for item in self.kzLabelList:
            item.setPixmap(pix)
            item.setScaledContents(True)
            item.installEventFilter(self)
            item.hide()

        for item in self.kbLabelList:
            item.setPixmap(pix)
            item.setScaledContents(True)
            item.installEventFilter(self)
            item.hide()

        for item in self.knLabelList:
            item.setPixmap(pix)
            item.setScaledContents(True)
            item.installEventFilter(self)
            item.hide()
        
        

    def model3dInit(self):
        
        #reader
        zlNum = 11
        zzNum = 12
        self.zlReaderList = []
        for i in range(zlNum):
            reader = vtk.vtkSTLReader()
            reader.SetFileName("./stl/zl_%s.stl" % (str(i+1)))
            self.zlReaderList.append(reader)

        self.zzReaderList = []
        for i in range(zzNum):
            reader = vtk.vtkSTLReader()
            reader.SetFileName("./stl/zz_%s.stl" % (str(i+1)))
            self.zzReaderList.append(reader)

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
        
        #mapper
        self.zlMapperList = []
        for i in range(zlNum):
            mapper = vtk.vtkPolyDataMapper()
            self.zlMapperList.append(mapper)

        self.zzMapperList = []
        for i in range(zzNum):
            mapper = vtk.vtkPolyDataMapper()
            self.zzMapperList.append(mapper)

        mapper_lg1 = vtk.vtkPolyDataMapper()
        mapper_lg2 = vtk.vtkPolyDataMapper()

        # mapper_bj1 = vtk.vtkPolyDataMapper()
        # mapper_bj2 = vtk.vtkPolyDataMapper()

        # mapper_ab1 = vtk.vtkPolyDataMapper()
        # mapper_ab2 = vtk.vtkPolyDataMapper()
        # mapper_bz1 = vtk.vtkPolyDataMapper()
        # mapper_hl1 = vtk.vtkPolyDataMapper()

        #bind
        if vtk.VTK_MAJOR_VERSION <= 5:
            for i in range(zlNum):
                self.zlMapperList[i].SetInput(self.zlReaderList[i].GetOutput())
            for i in range(zzNum):
                self.zzMapperList[i].SetInput(self.zzReaderList[i].GetOutput())
            mapper_lg1.SetInput(reader_lg1.GetOutput())
            mapper_lg2.SetInput(reader_lg2.GetOutput())

            # mapper_bj1.SetInput(reader_bj1.GetOutput())
            # mapper_bj2.SetInput(reader_bj2.GetOutput())

            # mapper_ab1.SetInput(reader_ab1.GetOutput())
            # mapper_ab2.SetInput(reader_ab2.GetOutput())
            # mapper_bz1.SetInput(reader_bz1.GetOutput())
            # mapper_hl1.SetInput(reader_hl1.GetOutput())
        else:
            for i in range(zlNum):
                self.zlMapperList[i].SetInputConnection(self.zlReaderList[i].GetOutputPort())
            for i in range(zzNum):
                self.zzMapperList[i].SetInputConnection(self.zzReaderList[i].GetOutputPort())
            mapper_lg1.SetInputConnection(reader_lg1.GetOutputPort())
            mapper_lg2.SetInputConnection(reader_lg2.GetOutputPort())

            # mapper_bj1.SetInputConnection(reader_bj1.GetOutputPort())
            # mapper_bj2.SetInputConnection(reader_bj2.GetOutputPort())

            # mapper_ab1.SetInputConnection(reader_ab1.GetOutputPort())
            # mapper_ab2.SetInputConnection(reader_ab2.GetOutputPort())
            # mapper_bz1.SetInputConnection(reader_bz1.GetOutputPort())
            # mapper_hl1.SetInputConnection(reader_hl1.GetOutputPort())

        #actor
        self.zlActorList = []
        for i in range(zlNum):
            actor = vtk.vtkActor()
            self.zlActorList.append(actor)
        for i in range(zlNum):
            self.zlActorList[i].SetMapper(self.zlMapperList[i])
        
        self.zzActorList = []
        for i in range(zzNum):
            actor = vtk.vtkActor()
            self.zzActorList.append(actor)
        for i in range(zzNum):
            self.zzActorList[i].SetMapper(self.zzMapperList[i])

        for i in range(zzNum):
            self.zzActorList[i].GetProperty().SetColor(155/255,155/255,155/255)

        actor_lg1 = vtk.vtkActor()
        actor_lg2 = vtk.vtkActor()

        actor_bj1 = vtk.vtkActor()
        actor_bj2 = vtk.vtkActor()

        actor_ab1 = vtk.vtkActor()
        actor_ab2 = vtk.vtkActor()
        actor_bz1 = vtk.vtkActor()
        actor_hl1 = vtk.vtkActor()

        actor_lg1.SetMapper(mapper_lg1)
        actor_lg2.SetMapper(mapper_lg2)

        # actor_bj1.SetMapper(mapper_bj1)
        # actor_bj2.SetMapper(mapper_bj2)

        # actor_ab1.SetMapper(mapper_ab1)
        # actor_ab2.SetMapper(mapper_ab2)
        # actor_bz1.SetMapper(mapper_bz1)
        # actor_hl1.SetMapper(mapper_hl1)

        actor_lg1.GetProperty().SetColor(255/255,0/255,0/255)
        actor_lg2.GetProperty().SetColor(255/255,0/255,0/255)

        # actor_bj1.GetProperty().SetColor(150/255,70/255,50/255)
        # actor_bj2.GetProperty().SetColor(150/255,70/255,50/255)

        # actor_ab1.GetProperty().SetColor(209/255,170/255,52/255)
        # actor_ab2.GetProperty().SetColor(209/255,170/255,52/255)
        # actor_bz1.GetProperty().SetColor(225/255,111/255,0/255)
        # actor_hl1.GetProperty().SetColor(30/255,144/255,255/255)
        

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(250/255, 250/255, 250/255)
        self.ren.SetBackground2(25/255, 50/255, 100/255)
        self.ren.SetGradientBackground(1)
        # self.ren.SetBackground2(25/255, 50/255, 100/255)
        self.vtkWidget = QVTKWidget()
        self.display3dLayout_2.addWidget(self.vtkWidget)
        self.renWin = self.vtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)
        self.renWin.SetSize(20000,20000)
        self.renWin.Render()
        self.iren = self.renWin.GetInteractor()

        #add
        for i in range(zlNum):
            self.ren.AddActor(self.zlActorList[i])
        for i in range(zzNum):
            self.ren.AddActor(self.zzActorList[i])
        
        self.ren.AddActor(actor_lg1)
        self.ren.AddActor(actor_lg2)

        # self.ren.AddActor(actor_bj1)
        # self.ren.AddActor(actor_bj2)

        # self.ren.AddActor(actor_ab1)
        # self.ren.AddActor(actor_ab2)
        # self.ren.AddActor(actor_bz1)
        # self.ren.AddActor(actor_hl1)

        self.zlActorInfList = []
        for i in range(zlNum):
            actorInf = str(self.zlActorList[i].GetMapper().GetInformation())[16:32]
            self.zlActorInfList.append(actorInf)
        
        self.actor2InfDic = {}
        for i in range(zlNum):
            self.actor2InfDic.update({self.zlActorInfList[i]:str(i+1)})

        camera = vtk.vtkCamera()
        camera.SetPosition(1,0.5,1)
        camera.SetFocalPoint(0,0,0)
        
        mylight = vtk.vtkLight()
        mylight.SetPosition(1,1,1)
        mylight.SetFocalPoint(0,0,0)
        self.ren.AddLight(mylight)

        self.ren.SetActiveCamera(camera)
        self.ren.ResetCamera()

        camera.Zoom(3)
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)

        self.iren.Initialize()

        self.picker = vtk.vtkCellPicker()
        self.picker.AddObserver("EndPickEvent", self.pickerfunc)     #将事件与回调函数建立连接
        self.style.AddObserver ('RightButtonReleaseEvent', self.pickerfunc)
        self.style.AddObserver ('RightButtonPressEvent', self.pickerfunc)

        self.iren.SetPicker(self.picker)

        #设置颜色闪烁timer
        self.twinkleFlag = True
        self.twinkleTimer = QTimer(self)
        self.twinkleTimer.timeout.connect(self.twinkleDisplay)
        self.twinkleTimer.start(1000)

    def twinkleDisplay(self):
        self.twinkleFlag = not self.twinkleFlag
        if self.twinkleFlag:
            self.zlOddColorR = 155/255
            self.zlOddColorG = 155/255
            self.zlOddColorB = 155/255

            self.zlEvenColorR = 0/255
            self.zlEvenColorG = 255/255
            self.zlEvenColorB = 0/255
        else:
            self.zlOddColorR = 0/255
            self.zlOddColorG = 255/255
            self.zlOddColorB = 0/255

            self.zlEvenColorR = 155/255
            self.zlEvenColorG = 155/255
            self.zlEvenColorB = 155/255

        for i in range(len(self.zlActorList)):
            if i % 2 == 0:
                self.zlActorList[i].GetProperty().SetColor(self.zlEvenColorR,self.zlEvenColorG,self.zlEvenColorB)
            else:
                self.zlActorList[i].GetProperty().SetColor(self.zlOddColorR,self.zlOddColorG,self.zlOddColorB)

        self.iren.Initialize()

    def pickerfunc(self,object, event):
        if event == 'RightButtonReleaseEvent':
            clickPos = self.style.GetInteractor().GetEventPosition()
            self.picker.Pick(clickPos[0], clickPos[1], 0, self.ren)
            actor = self.picker.GetActor()
            actor_inf = str(actor.GetMapper().GetInformation())[16:32]
            try:
                self.selectedid = self.actor2InfDic[actor_inf]
                self.vtkWidget.setContextMenuPolicy(Qt.CustomContextMenu)
                self.vtkWidget.customContextMenuRequested.connect(self.show_menu)
            except:
                self.selectedid = 0
            
            self.renWin.Render()

    def show_menu(self,point):

        self.rightButtonMenu = QMenu(self.vtkWidget)
        if self.selectedid:
            self.titleaction = QAction('当前选择第%s跨'%(self.selectedid),self.rightButtonMenu)

            self.callDisplayAction = QAction('选择传感器',self.rightButtonMenu)
            self.callDisplayAction.triggered.connect(self.selectedBlockOp)
            self.rightButtonMenu.addAction(self.titleaction)
            self.rightButtonMenu.addAction(self.callDisplayAction)
        else:
            self.titleaction = QAction('当前未选择',self.rightButtonMenu)
            self.rightButtonMenu.addAction(self.titleaction)

        self.dest_point=self.vtkWidget.mapToGlobal(point)
        self.rightButtonMenu.exec_(self.dest_point)

    def selectedBlockOp(self):
        self.realTimeSelectBlock = int(self.selectedid)
        self.sensorDataOp()
        self.crossUpdate()
    
    def showtimeInit(self):
        st_timer = QTimer(self)
        st_timer.timeout.connect(self.showtime)
        st_timer.start(1000)

    def showtime(self):
        date = QDate.currentDate()
        text = date.toString(Qt.ISODate)
        # print(text)
        self.lcdNumber_2.display(text)

        curtime = QTime.currentTime()
        text = curtime.toString()
        # print(text)
        self.lcdNumber.display(text)

    def cameraInit(self):
        self.cap = cv2.VideoCapture(0)
        camera_timer = QTimer(self)
        camera_timer.timeout.connect(self.cameraDisplay)
        camera_timer.start(100)
        
    
    def cameraDisplay(self):

        if self.cap.isOpened():
            success, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # frame.resize(230, 295)
            # frame = cv2.resize(frame, (230,295),0,0, interpolation=cv2.INTER_AREA)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.cameraLabel.setPixmap(QPixmap.fromImage(img))

            cv2.waitKey(1)



class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginWin = LoginWindow()

    styleFile = './loginwin.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    # qssStyle = qdarkstyle.load_stylesheet_pyqt5()
    loginWin.setStyleSheet(qssStyle)

    
    loginWin.show()
    sys.exit(app.exec())