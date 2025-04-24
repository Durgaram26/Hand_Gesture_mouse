"""ai mouse controller demo version -by durgaram """

import cv2
import mediapipe as mp
import pyautogui
import threading
#cv2 impoert
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = 1366,768
#allignment of the mosue sensitivity
index_x = 0
index_y = 0
thumb_x = 0
thumb_y = 0
click_threshold = 50
move_threshold = 200

def process_hand_landmarks():
    global index_x, index_y, thumb_x, thumb_y
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_width)
                    y = int(landmark.y*frame_height)
                    if id == 8:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                        index_x = screen_width/frame_width*x
                        index_y = screen_height/frame_height*y

                    if id == 4:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                        thumb_x = screen_width/frame_width*x
                        thumb_y = screen_height/frame_height*y

        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)

# threading for perfomance
t = threading.Thread(target=process_hand_landmarks)
t.daemon = True
t.start()

# main threadinf for mouse
while True:
    if abs(index_y - thumb_y) < click_threshold:
        pyautogui.click()
        pyautogui.sleep(1)
    elif abs(index_y - thumb_y) < move_threshold:
        pyautogui.moveTo(index_x, index_y)
