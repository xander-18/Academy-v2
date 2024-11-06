import cv2
import mediapipe as mp
import numpy as np

def euclidean_distance(p1, p2):
    """Calculate the Euclidean distance between two points."""
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def draw_bounding_box(image, hand_landmarks):
    """Draw a bounding box around the detected hand."""
    image_height, image_width, _ = image.shape
    x_min, y_min = image_width, image_height
    x_max, y_max = 0, 0

    for landmark in hand_landmarks.landmark:
        x, y = int(landmark.x * image_width), int(landmark.y * image_height)
        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y

    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

def recognize_gesture(image, hand_landmarks):
    """Recognize hand gestures for addition."""
    image_height, image_width, _ = image.shape

    index_finger_tip = (int(hand_landmarks.landmark[8].x * image_width),
                        int(hand_landmarks.landmark[8].y * image_height))
    thumb_tip = (int(hand_landmarks.landmark[4].x * image_width),
                 int(hand_landmarks.landmark[4].y * image_height))

    # Detect the "plus" gesture
    if abs(thumb_tip[1] - index_finger_tip[1]) < 50 and \
       abs(thumb_tip[0] - index_finger_tip[0]) < 50:
        return "+"
    else:
        return "Unknown"

def calculate_sum(image, hand_landmarks):
    """Calculate the sum of two numbers using hand gestures."""
    image_height, image_width, _ = image.shape

    index_finger_tip = (int(hand_landmarks.landmark[8].x * image_width),
                        int(hand_landmarks.landmark[8].y * image_height))
    thumb_tip = (int(hand_landmarks.landmark[4].x * image_width),
                 int(hand_landmarks.landmark[4].y * image_height))

    # Detect the number of fingers raised
    fingers_raised = 0
    if index_finger_tip[1] < thumb_tip[1]:
        fingers_raised += 1
    if (int(hand_landmarks.landmark[12].y * image_height) < thumb_tip[1]):
        fingers_raised += 1
    if (int(hand_landmarks.landmark[16].y * image_height) < thumb_tip[1]):
        fingers_raised += 1
    if (int(hand_landmarks.landmark[20].y * image_height) < thumb_tip[1]):
        fingers_raised += 1

    return fingers_raised

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            if num_hands == 2:
                hand1_landmarks = results.multi_hand_landmarks[0]
                hand2_landmarks = results.multi_hand_landmarks[1]

                # Recognize gestures for each hand
                hand1_gesture = recognize_gesture(image, hand1_landmarks)
                hand2_gesture = recognize_gesture(image, hand2_landmarks)

                # Calculate the sum
                if hand1_gesture == "+" and hand2_gesture == "Unknown":
                    num1 = calculate_sum(image, hand1_landmarks)
                    num2 = calculate_sum(image, hand2_landmarks)
                    result = num1 + num2
                    cv2.putText(image, f"{num1} + {num2} = {result}", (50, 150),
                               cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)
                else:
                    cv2.putText(image, "Invalid gesture", (50, 150),
                               cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 4)

                # Draw bounding boxes
                draw_bounding_box(image, hand1_landmarks)
                draw_bounding_box(image, hand2_landmarks)

        cv2.imshow('Hand Gesture Calculator', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()