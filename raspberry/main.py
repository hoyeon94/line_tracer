import cv2
import socket
import sys
import os
import numpy as np
import pdb
import serial
import cv2
import time

from Image import *
from Utils import *

BOUNDARY = 100
TIMESLICE=80
edge=310
ser = serial.Serial('/dev/ttyUSB0',9600)
if ser is None:
    ser = serial.Serial('/dev/ttyUSB1',9600)
    
cap = cv2.VideoCapture(0)
print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))

dev=10
base_speed=50


i=0
cmd1=("F%d\n"%(150)).encode('ascii')
ser.write(cmd1)
prestate=0
print ("ready")
#직각에서 회전 요청을 70번 보낸다.
MAXROTATENUM =70
# 처음 직각 요청은 위에 정의한 숫자로 설정한다.
currentRotateNum = MAXROTATENUM

while True:
    #print(ser.readline()) suspend!
    #time.sleep(0.1)
    ret, fram = cap.read()
    i+=1
    if ret:
        font = cv2.FONT_HERSHEY_SIMPLEX
        direction = 0
        Images=[]
        N_SLICES = 3

        for q in range(N_SLICES):
            Images.append(Image())
        if fram is not None:
    #이미지를 조각내서 윤곽선을 표시하게 무게중심 점을 얻는다
            Points = SlicePart(fram, Images, N_SLICES)

    #N_SLICES 개의 무게중심 점을 x좌표, y좌표끼리 나눈다
        x = Points[::2]
        y = Points[1::2]

    #조각난 이미지를 한 개로 합친다
        fm = RepackImages(Images)
    
    #완성된 이미지를 표시한다
        



    ####모터 구동 알고리즘#####


        #현재 표시되는 무게중심 점과 수직선사이의 거리를 구함.
        #minus->왼쪽으로 가야 함.
        #plus->오른쪽으로 가야 함.
        difference_forward=Points[2][0]-320
        difference_center=Points[1][0]-320
        difference_backward=Points[0][0]-320
        difference=0
        #이전 트랙 상태가 직각이였다면 정해진 회수만큼 방향을 전환
        if currentRotateNum != MAXROTATENUM :
            difference = prestate
            currentRotateNum = currentRotateNum -1
            print("difference , prestate: " ,(difference,prestate)   )
            print("currentRotateNum : ",currentRotateNum)
        #방향전환 완료 후 정상적인 무게중심 점을 찾을 때 까지 자동차를 직진함.
            if currentRotateNum ==0:
                    currentRotateNum = currentRotateNum+1 
                    tmp = 0
                    if abs(difference_forward)<200:
                        tmp = tmp+1
                    if abs(difference_center) < 200:
                        tmp = tmp+1
                    if abs(difference_backward) < 200:
                        tmp = tmp +1
                    if tmp >=2 :
                        currentRotateNum = MAXROTATENUM
			continue
		#직진하기 위한 설정값.
                    difference_forward = 0
                    difference_backward = 0
                    difference_center = 0
        #가장 자동차로부터 먼 무게중심 점을 기준으로 자동차 방향을 결정
        elif (abs(difference_forward) < edge):
            difference=difference_forward
        #만일 가장 먼 무게중심점이 화면을 이탈했다면 중간 무게중심점으로 방향을 결정
        elif (abs(difference_center)<edge):
            difference=difference_center
        #모든 무게중심점이 화면을 이탈했다면 직각 상태이므로 원래 회전하던 방향으로 고정된 회수만큼 방향을 전환
        else:
            print( "10 times call  ") 
            difference = prestate
            currentRotateNum = currentRotateNum-1
            print("difference , prestate: " ,(difference,prestate) 
        
            # 직각 회전 시, 사용할 변수, 이전에 움직임이 좌회인지 우회인지 저장한다.
	    # 한번 아두이노 보드로 이동요청을 보낼 때마다 덮어쓴다.  
        prestate = difference

        #만약 세 점이 모두 boundary 안에 있다면 직진
        if(abs(difference_forward)<BOUNDARY and abs(difference_center)<BOUNDARY and (abs(difference_backward)<BOUNDARY)):
                cmd1=("F%d\n"%(150)).encode('ascii')
                print("forward")
        #무게중심 점이 왼쪽으로 치우쳐 있다면 오른쪽바퀴를 구동시켜 자동차르 왼쪽으로 회전
        elif difference> BOUNDARY :
                print("right")
                cmd1=("R%d\n"%(150)).encode('ascii')
	#무게중심 점이 오른쪽으로 치우쳐있다면 왼쪽바퀴를 구동시켜 자동차를 오른쪽으로 회전
        elif difference< -BOUNDARY:
                cmd1=("L%d\n"%(150)).encode('ascii')
                print("left")
        print(cmd1)
        ser.write(cmd1)
        
        cv2.imshow("Vision Race", fm)
        print(Points[0],Points[1],Points[2])
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    else:
        print('error')
cap.release()
cv2.destroyAllWindows()
