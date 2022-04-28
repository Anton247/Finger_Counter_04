import cv2
import mediapipe as mp
import time

class fingerDetector():
    def __init__(self, mode=False, maxHands=2, complexity=0, detectinCon=0.75, trackCon=0.75):
        self.mpHands = mp.solutions.hands # инициализация модуля распознавания рук
        self.hands = self.mpHands.Hands(mode, maxHands, complexity, detectinCon, trackCon) # характеристики для распознавания
        self.mpDraw = mp.solutions.drawing_utils # инициализация утилит для рисования
        self.fingertips = [4, 8, 12, 16, 20] # кончики пальцев
        self.handList = {}
        self.fingers = {} 

    def findHands(self, img, draw=True):
        RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        RGB_image.flags.writeable = False
        self.result = self.hands.process(RGB_image)
        RGB_image.flags.writeable = True
        if draw:
            if self.result.multi_hand_landmarks:
                for handLms in self.result.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
            
        return img
    
    def findPosition(self, img, handNumber=0, draw=True):
        xList = []
        yList = []
        self.handList[handNumber] = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNumber]
            for lm in myHand.landmark:
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.handList[handNumber].append([cx, cy])
                
            if draw:
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                print('(',xmin ,',', ymin, ')', '(',xmax ,',', ymax, ')')
                offset = 20
                cv2.rectangle(img, (xmin-offset, ymin-offset), (xmax+offset, ymax+offset), (0, 255, 0), 2)

    def fingersUp(self):
        if self.result.multi_hand_landmarks:
            handCount = len(self.result.multi_hand_landmarks)
            for i in range(handCount):
                side = 'left'
                if self.handList[i][5][0] > self.handList[i][17][0]:
                    side = 'right'
                
                if side == 'left':
                    if self.handList[i][self.fingertips[0]][0] < self.handList[i][self.fingertips[0] - 1][0]:
                        self.fingers[i].append(1)
                    else:
                        self.fingers[i].append(0)
                else:
                    if self.handList[i][self.fingertips[0]][0] > self.handList[i][self.fingertips[0] - 1][0]:
                        self.fingers[i].append(1)
                    else:
                        self.fingers[i].append(0)

                for id in range(1, 5):
                    if self.handList[i][self.fingertips[id]][1] < self.handList[i][self.fingertips[id] - 2][1]:
                        self.fingers[i].append(0)
                    else:
                        self.fingers[i].append(1)
                
                print(self.fingers[i])
                
                

def main():
    cap = cv2.VideoCapture(0)
    detector = fingerDetector()
    while cap.isOpened():
        success, image = cap.read()
        prevTime = time.time()
        if not success:
            print('Не удалось получить кадр с web-камеры')
            continue
        image = cv2.flip(image, 1) # зеркально отражаем изображение
        image = detector.findHands(image)
        if detector.result.multi_hand_landmarks:
            handCount = len(detector.result.multi_hand_landmarks)
            for i in range(handCount):
                detector.findPosition(image, i)
        detector.fingersUp()
        currentTime = time.time()
        fps = 1 / (currentTime - prevTime)
        cv2.putText(image, f'FPS: {int(fps)}', (400, 150), cv2.FONT_HERSHEY_PLAIN, 3, (240, 100, 0), 3)
        cv2.imshow('image', image)
        if cv2.waitKey(1) & 0xFF == 27: # ESC
            break

main()
