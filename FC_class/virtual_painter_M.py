import fingertrackingmodule as ftm
import cv2
import os
import numpy as np
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 1920
height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
ptime = time.time()
while cap.isOpened():
        success, image = cap.read()
        if not success:
            print('Не удалось получить кадр с web-камеры')
            continue
        
        ctime = time.time()
        fps = 1/(ctime - ptime)
        ptime = ctime
        cv2.putText(image, f'FPS: {int(fps)}', (400, 150), cv2.FONT_HERSHEY_PLAIN, 3, (240, 100, 0), 3)
        cv2.imshow("window", image)
        print(fps)
        if cv2.waitKey(1) & 0xFF == 27: # ESC
            break