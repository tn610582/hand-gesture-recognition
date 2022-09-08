import cv2
import numpy as np
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

L1_diff = 0
L2_diff = 0

# Flag check if finger on square
on_square = False

#with?
hands =  mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Capture video from device 0
cap = cv2.VideoCapture(0)

# get width and height of captured frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Parameters of rectangle
rect_xx = 200
rect_yy = 200
rect_width = 150

# Read images
# img_1 = cv2.imread('src/IMG_5889.jpg')
# img_2 = cv2.imread('src/IMG_5890.jpg')
# img_1 = cv2.resize(img_1, (140,300))
# img_2 = cv2.resize(img_2, (140,300))
# tmp_img = img_1

# Main loop
while True:
    ret,image = cap.read()
    #Fix image
    image = cv2.flip(image,1)
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    results = hands.process(image)
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Check hands
    if results.multi_hand_landmarks:
        # decode hands
        for hand_landmarks in results.multi_hand_landmarks:
            #draw 21 landmarks
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        # save 21 landmarks in lists
        x_s = []
        y_s = []
        for landmarks in hand_landmarks.landmark:
            x_s.append(landmarks.x)
            y_s.append(landmarks.y)

        # get index finger coordinates
        finger_8_x = int(x_s[8]*width)
        finger_8_y = int(y_s[8]*height)
        # get thumb coordinates
        finger_4_x = int(x_s[4]*width)
        finger_4_y = int(y_s[4]*height)
        # Calculate distance of two fingers
        length = math.hypot((finger_8_x-finger_4_x),(finger_8_y-finger_4_y))

        # Circle follow finger 8
        # cv2.circle(image,(finger_8_x,finger_8_y),20,(200,0,0),-1)
        # print(finger_8_x,finger_8_y)

        # Calculate finger on rectangle
        if length < 100:
            if (finger_8_x > rect_xx) and (finger_8_x<(rect_xx+rect_width)):
                if(finger_8_y > rect_yy) and (finger_8_y < (rect_yy+rect_width)):
                    if on_square == False:
                            L1_diff = abs(finger_8_x - rect_xx)
                            L2_diff = abs(finger_8_y - rect_yy)
                            on_square = True   
                            # tmp_img = img_2
        else: 
            on_square = False
            # tmp_img = img_1
        
        # Update rectangle coordinates
        if on_square:    
            rect_xx = finger_8_x - L1_diff
            rect_yy = finger_8_y - L2_diff
        
    # Draw rectangle
    cv2.rectangle(image,pt1 = (rect_xx,rect_yy), pt2 = (rect_xx+rect_width,rect_yy+rect_width), color=(0,200,0), thickness = -1)
    #image[rect_yy:rect_yy+300, rect_xx:rect_xx+140] = tmp_img   
    cv2.imshow("Drag", image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()