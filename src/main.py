import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#with?
hands =  mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

rect_xx = (200,200)
rect_yy = (300,300)

while True:
    ret,image = cap.read()

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
        # save 21 landmarks
        for landmarks in hand_landmarks.landmark.x:
            print(landmarks)
    
    cv2.rectangle(image,pt1 = rect_xx, pt2 = rect_yy, color=(0,200,0), thickness = -1)

    cv2.imshow("Drag", image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()