import cv2
import numpy as np
import matplotlib.pyplot as plt
import yun_decting

cap = cv2.VideoCapture('D:\\shrimp\\testvideo\\Aquarium Fish Tank.avi')
ret ,frame = cap.read()
frame = cv2.resize(frame,(640,480))
cb = cv2.cvtColor( frame , cv2.COLOR_BGR2GRAY)
yun = yun_decting.dectect(frame,cb,0.1,10)

for i  in range (0,1):
    ret ,frame = cap.read()

frame_count=10000
ret = True
while ret == True :
    print (frame_count)
    frame_count = frame_count + 1
    for i  in range (0,1):
        ret ,frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    yun.frame = frame
    #a=yun.fgmask(cb)
    yun.make()
    cv2.imshow('frame',yun.frame)
    cv2.imshow('ap',yun.ap)
    cv2.imshow('mp',yun.mp)
    cv2.imshow('combine_renoise',yun.combine_renoise)
    cv2.imshow('rect_result',yun.rect_result)
    cv2.imshow('component_result',yun.component_result)
    aa = yun.combine_renoise
    #cv2.waitKey(1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #rect = yun.fish_list
    '''
    for i in range (1,rect.shape[0]):
        x=int(rect[i,1])
        x2=int(rect[i,3])
        y=int(rect[i,2])
        y2=int(rect[i,4])
        if (x2-x)*(y2-y) > 10000: 
            temp = frame[y:y2,x:x2]
            #cv2.imwrite('./temp/'+str(frame_count)+'_'+str(i)+'.png',temp)
            '''
cap.release()
cv2.destroyAllWindows()
    
