import cv2
import mediapipe as mp
# to check the frame rate
import time


print("HandTrackingMin Ready")

class handDetector():
    def __init__(self, mode=False, maxHands=1,modelComplex=1,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComplex= modelComplex
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                self.maxHands,self.modelComplex, self.detectionCon,
                self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        # convert to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                        self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):

        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 0, 255),
                            cv2.FILLED)

        return self.lmList

    def fingersUp(self):
        fingers = []

        # Thumb
        # open
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        #close
        else:
            fingers.append(0)


        # index to pinky finger
        for id in range(1, 5):
            # open
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            # close
            else:
                fingers.append(0)

        return fingers



def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        if len(lmList) !=0:
            print(lmList[4])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)


        cv2.imshow("Image", img)
        cv2.waitKey(1)




if __name__ == "__main__":
    main()