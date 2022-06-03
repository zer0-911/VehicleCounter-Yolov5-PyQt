# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
import cv2
from cv2 import line
import imutils
import time
import numpy as np 
import torch


# Class UI 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 754)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 690, 111, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 690, 111, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(300, 690, 131, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 1071, 600))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("img/DisCov.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(660, 660, 161, 17))
        self.label_10.setObjectName("label_10")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setGeometry(QtCore.QRect(660, 690, 113, 25))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_11.setGeometry(QtCore.QRect(820, 690, 113, 25))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(820, 660, 121, 17))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(300, 660, 91, 17))
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(940, 660, 67, 17))
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(1000, 690, 91, 31))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(1000, 660, 81, 17))
        self.label_18.setObjectName("label_18")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_12.setGeometry(QtCore.QRect(490, 690, 113, 25))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(490, 660, 161, 17))
        self.label_13.setObjectName("label_13")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.yolo)
        self.pushButton_2.clicked.connect(self.Input_cam)
        self.lineEdit.returnPressed.connect(self.Path)
        self.lineEdit_10.cursorPositionChanged['int', 'int'].connect(
            self.x_changer2)
        self.lineEdit_11.cursorPositionChanged['int', 'int'].connect(
            self.y_changer)
        self.lineEdit_12.cursorPositionChanged['int', 'int'].connect(
            self.x_changer)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.tmp = None
        self.started = False
        self.cam = True  # True for webcam
        self.path = ""  # Path to image
        self.y_now = 288
        self.x1_now = 400
        self.x2_now = 1500

    # Fungsi untuk mengupdate tampilan
    def setFrame(self, image):
        self.tmp = image
        image = imutils.resize(image, width=1071)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(
            frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label_7.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_7.setScaledContents(True)
    # Fungsi untuk mengupdate nilai iterasi dilatasi
    def x_changer(self):
        self.x1_now = int(self.lineEdit_12.text())
        if(self.x1_now < 0):
            self.x1_now = 0
        self.update()
    
    def x_changer2(self):
        self.x2_now = int(self.lineEdit_10.text())
        if(self.x2_now < 0):
            self.x2_now = 0
        self.update()

    # Fungsi untuk mengupdate nilai iterasi erosi
    def y_changer(self):
        self.y_now = int(self.lineEdit_11.text())
        if(self.y_now < 0):
            self.y_now = 0
        self.update()
    # Fungsi untuk menggunakan video atau webcam
    def Input_cam(self):
        if self.cam:
            self.cam = False
            self.pushButton.setText('Video')
        else:
            self.cam = True
            self.pushButton.setText('WebCam')
        self.update()
    # Fungsi untuk mengupdate menggunakan video atau webcam
    def Path(self):
        self.path = self.lineEdit.text()
        self.update()
    # Fungsi untuk mengupdate frame
    def update(self):
        self.setFrame(self.image)

    def VehicleDetection(self, model, frame): 
        results =model(frame)
        resBBox =results.pandas().xyxy[0]
        DetectedBBox =resBBox.values.tolist()
        BBox=[]
        pmin = np.array([-1,-1])
        pmax= np.array([-1,-1])
        pmid = (pmin+pmax)/2  
        #Inisialisasi BBox
        BBox.append([pmin,pmax,pmid,-1,-1,-1,-1])
        #---Start For.....
        for xmin,ymin,xmax,ymax,conf,cl,nama  in DetectedBBox:
            IdPrev=-1
            #Menyimpan Bounding Box
            xmid =(xmin+xmax)/2
            ymid =(ymin+ymax)/2
            BBox.append([xmin,ymin,xmax,ymax,xmid,ymid,conf,cl,nama,IdPrev])
        #---End For.....
        return BBox
        
    def VehicleTracking(self, ListBBox):
        # Memastikan sedikitnya terdapat dua frame yang di proses 
        #---Begin  len(ListBBox)>2    
        if len(ListBBox)>=2:
            # Bounding Box yang frame yang terakhir disimpan 
            CurrentBBox =ListBBox[-1]
            # Bounding Box dari frame sebelumnya
            PrevBBox =ListBBox[-2]
            
            #---Begin for IndexLast = 0 in range(len(LastBBox): 
            for IndexLast in range(1,len(CurrentBBox)): 
                
                
                xminc,yminc,xmaxc,ymaxc,xmidc,ymidc,  confc,clc,namac,IdPrevC=CurrentBBox[IndexLast]
                rCocok =100000000000
                IndexCocok =-1 
                #********************************************************
                #***Mencari Obyek yang bersesuaian dari frame sebelumnya
                #********************************************************
                #---Start IndexPrev =0 in range(PrevBBox
                for IndexPrev in range(1,len(PrevBBox)):
                    xminp,yminp,xmaxp,ymaxp,xmidp,ymidp,  confp,clp,namep,IdPrevp =PrevBBox[IndexPrev]
                    # 3. pmax1 dan pmax2 
                    v =np.array([xmidc-xmidp,ymidc-ymidp])  
                    RTot =  np.linalg.norm(v)
                    #---Begin IndexSave ==-1
                    if IndexCocok ==-1: 
                        rCocok =RTot 
                        IndexCocok =IndexPrev
                    else: 
                        if RTot<rCocok:
                            rCocok =RTot 
                            IndexCocok =IndexPrev
                    #--- End IndexSave ==-1
                #---End for IndexPrev =0 in range(PrevBBox)
                
                #--- Start if IndexCocok>-1:
                if IndexCocok>-1:
                    #Update 
                    
                    ListBBox[-1][IndexLast][9]=IndexCocok  
                #--- end if IndexCocok>-1:
            #---End for IndexLast = 0 in range(len(LastBBox): 
        #-- End if len(ListBBox)>2 
        return ListBBox

    def VehicleCounting(self, ListBBox,CarCounterLeft,CarCounterRight,MidLineY,MidLineY2,MidLineX,MidLineX2):
        # Memastikan sedikitnya terdapat dua frame yang di proses 
        #---Begin  len(ListBBox)>2        
        
        if len(ListBBox)>=2:
            # Bounding Box yang frame yang terakhir disimpan 
            CurrentBBox =ListBBox[-1]
            # Bounding Box dari frame sebelumnya
            PrevBBox =ListBBox[-2]
            #---Begin for IndexLast = 0 in range(len(LastBBox): 
            for IndexLast in range(1,len(CurrentBBox)): 
                xminc,yminc,xmaxc,ymaxc,xmidc,ymidc,  confc,clc,namac,IdPrevC=CurrentBBox[IndexLast]
                #---Start if IdPrevC>-1 
                if IdPrevC>-1:
                
                    xminm, yminm,xmaxm,ymaxm,xmidm,ymidm=PrevBBox[IdPrevC][0:6]
                    LewatBatas = (ymidc-MidLineY)*(ymidm-MidLineY)
                    #Apabila nilai LewatBatas <0 maka kendaraan sedang melewati garis pembatas
                    #---Startif LewatBatas<=0 
                    if(xmidc>MidLineX and xmidm<MidLineX2):
                        if LewatBatas<=0:
                            #Menentukan apakah arah kendaraan menuju ke atas atau kebawah 
                            Arah = ymidc-MidLineY
                            #---Start Arah>0
                            if Arah >=0 :
                                CarCounterRight = CarCounterRight +1
                            else:
                                CarCounterLeft = CarCounterLeft +1
                        #---End Arah>0
                    #---Startif LewatBatas<=0
                #---end if IdPrevC>-1
            #---End for IndexLast = 0 in range(len(LastBBox):
            self.textBrowser_3.setText(str(CarCounterRight))
        return CarCounterLeft,CarCounterRight 

    #Menggambar Bounding DaftarBounding Box terakhir yang disimpan dalam list
    def DrawLastBoundingBox(self, frame, ListBBox):
        # Bounding Box yang frame yang terakhir disimpan 
        CurrentBBox =ListBBox[-1]
        # Bounding Box dari frame sebelumnya
        #---Begin for IndexLast = 0 in range(len(LastBBox): 
        for IndexLast in range(1,len(CurrentBBox)): 
            xminc,yminc,xmaxc,ymaxc,xmidc,ymidc,  confc,clc,namac,IdPrevC=CurrentBBox[IndexLast]
            pc1 =(int(xminc),int(yminc))
            pc2 =( int(xmaxc),int(ymaxc))
            pcc=( int(xmidc),int(ymidc))
            frame=cv2.rectangle(frame,pc1,pc2,(255,0,255),1)
            frame=cv2.circle(frame,pcc,2,(255,255,255),1)
            
        return frame 
    #Menggambar Vektor Pergerakan Kendaraan
    def DrawVehicleVector(self, frame,ListBBox):
        if len(ListBBox)>=2:
            # Bounding Box yang frame yang terakhir disimpan 
            CurrentBBox =ListBBox[-1]
            # Bounding Box dari frame sebelumnya
            PrevBBox =ListBBox[-2]
            #---Begin for IndexLast = 0 in range(len(LastBBox): 
            for IndexLast in range(1,len(CurrentBBox)): 
                xminc,yminc,xmaxc,ymaxc,xmidc,ymidc,  confc,clc,namac,IdPrevC=CurrentBBox[IndexLast]
                #---Start IdPrevC>-1 
                if IdPrevC>-1:
                
                    xminm, yminm,xmaxm,ymaxm,xmidm,ymidm=PrevBBox[IdPrevC][0:6]
                    p1 =(int(xmidc),int(ymidc))
                    p2 =(int(2*xmidc-xmidm),int(2*ymidc-ymidm))
                    
                    frame=cv2.line(frame,p1,p2,(255,255,255),1)
                #---End  IdPrevC>-1
            #---End for IndexLast = 0 in range(len(LastBBox): 
        return frame


    #Menggambar Jumlah kendaraam ke lauar   
    def DrawCountedCar(self, frame,CarCounterLeft,CarCounterRight):
        org = (100, 50)
        # fontScale
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        # frame = cv2.putText(frame, "Left :"+str(CarCounterLeft), org, font, fontScale, color, thickness, cv2.LINE_AA)
        org = (1000, 50)
        # frame = cv2.putText(frame,"Right :" +str(CarCounterRight), org, font, fontScale, color, thickness, cv2.LINE_AA)
        return frame 
    
    def yolo(self):
        if self.started:
            self.started = False
            self.pushButton.setText('Start Video')
        else:
            self.started = True
            self.pushButton.setText('Stop Video')

        if self.cam:
            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture(self.path)
        yolov5_cek = '/home/iqbalf/Documents/VsCode/VehicleCounter-YoloV5/yolov5s.pt'
        model = torch.hub.load('', 'custom', path=yolov5_cek, source='local',_verbose=False)
        model.img=360
        model.classes=[2,3,5,7]
        #model.conf =0.4
        #model.iou=0.2
        if (vid.isOpened()== False): 
            print("Error opening video stream or file")
        #Membuat Daftar Untuk menyimpan Bounding Box yang diperoleh disetiap frame.
        ListBBox=[];
        # Membaca setiap frame sampai selesai
        #---Begin while(cap.isOpened()):
        CarCounterLeft = 0 
        CarCounterRight = 0 

        while(vid.isOpened()):
            # Capture frame-by-frame
            QtWidgets.QApplication.processEvents()
            img, self.image = vid.read()
            #Membuat Garis batas untuk perhitungan Kendaraan yang Lewat
                       
            b, c, w = self.image.shape
            

            if img == True:
                MidLineY = self.y_now
                MidLineY2 = self.y_now
                MidLineX = self.x1_now
                MidLineX2 = self.x2_now
                print(MidLineX)
                BBox = self.VehicleDetection(model, self.image)
                    #Menambahkan Bounding box ke ListBBox
                ListBBox.append(BBox)
                if len(ListBBox)>2:
                    ListBBox.pop(0)
                ListBBox= self.VehicleTracking(ListBBox)
                CarCounterLeft,CarCounterRight = self.VehicleCounting(ListBBox,CarCounterLeft,CarCounterRight,MidLineY,MidLineY2,MidLineX,MidLineX2)
                frame = self.DrawCountedCar(self.image,CarCounterLeft,CarCounterRight)
                    
                frame= self.DrawLastBoundingBox(frame, ListBBox)
                frame= self.DrawVehicleVector(frame,ListBBox)
                p1= (int(MidLineX),int(MidLineY)) 
                p2 = (int(MidLineX2), int(MidLineY2))
                self.image=cv2.line(frame,p1,p2,(0,255,0),3)
                self.update()
                key = cv2.waitKey(1) & 0xFF
                if self.started == False:
                    break
                    print('Loop break')            

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowIcon(QtGui.QIcon('img/DisLog.png'))
        MainWindow.setWindowTitle(_translate("MainWindow", "Vehicle Counter With YOLOV5"))
        self.pushButton.setText(_translate("MainWindow", "Open Video"))
        self.pushButton_2.setText(_translate("MainWindow", "WebCam"))
        self.label_10.setText(_translate("MainWindow", "Batas X 2"))
        self.label_11.setText(_translate("MainWindow", "Batas Y"))
        self.label_12.setText(_translate("MainWindow", "Path Video"))
        self.label_18.setText(_translate("MainWindow", "Kendaraan"))
        self.label_13.setText(_translate("MainWindow", "Batas X 1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
