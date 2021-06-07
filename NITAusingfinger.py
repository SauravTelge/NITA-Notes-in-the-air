import numpy as np
import cv2
from collections import deque
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
#default called trackbar function 
# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

#The kernel to be used for dilation purpose 
kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Here is code for Canvas setup
paintWindow = np.zeros((471,636,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

hi=0
# Loading the default webcam of PC.
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)


with mp_hands.Hands(
    min_detection_confidence=0.75,
    min_tracking_confidence=0.65) as hands:

    while cap.isOpened():
        
        

        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        #Flipping the frame to see same side of yours
       
        
       
        frame = cv2.cvtColor(cv2.flip(frame, 1),cv2.COLOR_BGR2RGB)
       
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        results = hands.process(frame)

        # Draw the hand annotations on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
        frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
        frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
        frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
        frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
        frame = cv2.rectangle(frame, (505,75), (600,140), (255,99,71), -1)
        frame = cv2.rectangle(frame, (505,155), (600,210), (255,99,71), -1)
        cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
        cv2.putText(frame, "CAPTURE ", (520, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "SCREEN", (520, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "CLOSE", (520, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # print('hand_landmarks:', hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP])
                center = (int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*640), int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*480))
            
                # mp_drawing.draw_landmarks(
                #     frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                if center[1] <= 65:
                    if 40 <= center[0] <= 140: # Clear Button
                        bpoints = [deque(maxlen=512)]
                        gpoints = [deque(maxlen=512)]
                        rpoints = [deque(maxlen=512)]
                        ypoints = [deque(maxlen=512)]
                       

                        blue_index = 0
                        green_index = 0
                        red_index = 0
                        yellow_index = 0

                        paintWindow[67:,:,:] = 255
                    elif 160 <= center[0] <= 255:
                            colorIndex = 0 # Blue
                        
                    elif 275 <= center[0] <= 370:
                            colorIndex = 1 # Green
                    elif 390 <= center[0] <= 485:
                            colorIndex = 2 # Red
                    elif 505 <= center[0] <= 600:
                            colorIndex = 3 # Yellow
                elif 520 <= center[0] <= 600 and 75 <=center[1] <= 140:
                    # cv2.waitKey(1)
                    # image = pyautogui.screenshot(region=(0,0, 800, 500))
                    # image = cv2.cvtColor(np.array(image),
                    #         cv2.COLOR_RGB2BGR)
        
                        # writing it to the disk using opencv
                    hi=hi+1
                    cv2.imwrite(f"image{hi}.jpg", paintWindow)
                elif 505 <= center[0] <= 600 and 155 <=center[1] <= 210:
                    cv2.destroyWindow(frame) 
                     
                else :
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("r"):
                        if colorIndex == 0:
                            bpoints[blue_index].appendleft(center)
                            
                        elif colorIndex == 1:
                            gpoints[green_index].appendleft(center)
                        elif colorIndex == 2:
                            rpoints[red_index].appendleft(center)
                        elif colorIndex == 3:
                            ypoints[yellow_index].appendleft(center)
                # Append the next deques when nothing is detected to avois messing up
        else:
            bpoints.append(deque(maxlen=512))
           
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

            # Draw lines of all the colors on the canvas and frame 
        points = [bpoints, gpoints, rpoints, ypoints]
        
        for i in range(len(points)):
            
            for j in range(len(points[i])):
                
                for k in range(1, len(points[i][j])):
                   
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    # Show all the windows
        cv2.imshow("Tracking", frame)
        cv2.imshow("Paint", paintWindow)
    

	# If the 'q' key is pressed then stop the application 
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()