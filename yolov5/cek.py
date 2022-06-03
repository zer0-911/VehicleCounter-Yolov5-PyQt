import cv2 
import torch
import numpy as np 
from time import sleep

def VehicleDetection(model, frame): 
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
        
def VehicleTracking(ListBBox):
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

def VehicleCounting(ListBBox,CarCounterLeft,CarCounterRight,MidLineY):
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
    return CarCounterLeft,CarCounterRight 

#Menggambar Bounding DaftarBounding Box terakhir yang disimpan dalam list
def DrawLastBoundingBox(frame, ListBBox):
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
def DrawVehicleVector(frame,ListBBox):
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
def DrawCountedCar(frame,CarCounterLeft,CarCounterRight):
    org = (100, 50)
    # fontScale
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.putText(frame, "Left :"+str(CarCounterLeft), org, font, fontScale, color, thickness, cv2.LINE_AA)
    org = (1000, 50)
    frame = cv2.putText(frame,"Right :" +str(CarCounterRight), org, font, fontScale, color, thickness, cv2.LINE_AA)
    return frame 

path = '/home/iqbalf/Documents/VsCode/VehicleCounter-YoloV5/yolov5s.pt'
model = torch.hub.load('', 'custom', path=path, source='local',_verbose=False)
model.img=360
model.classes=[2,5,7]
#model.conf =0.4
#model.iou=0.2
fn="/home/iqbalf/Documents/VsCode/VehicleCounter-YoloV5/yolov5/traffic.mp4"
cap = cv2.VideoCapture(fn)
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
#Membuat Daftar Untuk menyimpan Bounding Box yang diperoleh disetiap frame.
ListBBox=[];
# Membaca setiap frame sampai selesai
#---Begin while(cap.isOpened()):
CarCounterLeft = 0 
CarCounterRight = 0 

while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  #Membuat Garis batas untuk perhitungan Kendaraan yang Lewat
  b,c,w = frame.shape
  MidLineY = b*0.6
  

  if ret == True:
    BBox = VehicleDetection(model, frame)
        #Menambahkan Bounding box ke ListBBox
    ListBBox.append(BBox)
    if len(ListBBox)>2:
        ListBBox.pop(0)
    ListBBox=VehicleTracking(ListBBox)
    CarCounterLeft,CarCounterRight = VehicleCounting(ListBBox,CarCounterLeft,CarCounterRight,MidLineY)
    frame = DrawCountedCar(frame,CarCounterLeft,CarCounterRight)
        
    frame= DrawLastBoundingBox(frame, ListBBox)
    frame= DrawVehicleVector(frame,ListBBox)
    p1= (0,int(MidLineY)) 
    p2 = (c, int(MidLineY))
    frame=cv2.rectangle(frame,p1,p2,(0,255,0),3)

    cv2.imshow('Frame',frame)
    # Tekan Tombol Q Untuk Keluar
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  # Keluar dari loop
  else: 
    break
#---End while(cap.isOpened()):
cap.release()
# Hapus Semua frame
cv2.destroyAllWindows()