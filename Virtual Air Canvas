import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Initializqe MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize deques to store drawing points
points = [deque(maxlen=1024)]
colorIndex = 0
is_drawing = False

# Set up the drawing colors
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
paintWindow = np.ones((471, 636, 3)) * 255

# Draw the color buttons
button_coords = [
    (40, 1, 140, 65),
    (160, 1, 255, 65),
    (275, 1, 370, 65),
    (390, 1, 485, 65),
    (505, 1, 600, 65),
]
button_texts = ["CLEAR", "BLUE", "GREEN", "RED", "YELLOW"]
for i, (x1, y1, x2, y2) in enumerate(button_coords):
    paintWindow = cv2.rectangle(
        paintWindow, (x1, y1), (x2, y2), (0, 0, 0) if i == 0 else colors[i - 1], -1
    )
    cv2.putText(
        paintWindow,
        button_texts[i],
        (x1 + 10, 33),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

cv2.namedWindow("Paint", cv2.WINDOW_AUTOSIZE)

# Start capturing video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)
    hand_landmarks = result.multi_hand_landmarks

    # Draw color buttons on the frame
    for i, (x1, y1, x2, y2) in enumerate(button_coords):
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (122, 122, 122) if i == 0 else colors[i - 1], -1)
        cv2.putText(
            frame,
            button_texts[i],
            (x1 + 10, 33),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    if hand_landmarks:
        for landmarks in hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the landmarks for the index finger tip and thumb tip
            index_finger_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Calculate the positions
            index_finger_tip_pos = (
                int(index_finger_tip.x * frame.shape[1]),
                int(index_finger_tip.y * frame.shape[0]),
            )
            thumb_tip_pos = (
                int(thumb_tip.x * frame.shape[1]),
                int(thumb_tip.y * frame.shape[0]),
            )

            # Check if the index finger is up or making a fist
            if index_finger_tip.y < index_finger_mcp.y:
                is_drawing = True
            else:
                is_drawing = False

            if is_drawing:
                # Check if user clicked on the buttons
                if index_finger_tip_pos[1] <= 65:
                    if 40 <= index_finger_tip_pos[0] <= 140:
                        points = [deque(maxlen=1024)]
                        paintWindow[67:, :, :] = 255
                        colorIndex = 0  # Reset to the default color
                    elif 160 <= index_finger_tip_pos[0] <= 255:
                        colorIndex = 0
                    elif 275 <= index_finger_tip_pos[0] <= 370:
                        colorIndex = 1
                    elif 390 <= index_finger_tip_pos[0] <= 485:
                        colorIndex = 2
                    elif 505 <= index_finger_tip_pos[0] <= 600:
                        colorIndex = 3
                else:
                    if len(points) <= colorIndex:
                        points.append(deque(maxlen=1024))
                    points[colorIndex].appendleft(index_finger_tip_pos)
            else:
                if len(points) <= colorIndex:
                    points.append(deque(maxlen=1024))
                points[colorIndex].appendleft(None)

    for i, color_points in enumerate(points):
        for j in range(1, len(color_points)):
            if color_points[j - 1] is None or color_points[j] is None:
                continue
            cv2.line(frame, color_points[j - 1], color_points[j], colors[i], 2)
            cv2.line(paintWindow, color_points[j - 1], color_points[j], colors[i], 2)

    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
