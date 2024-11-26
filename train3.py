import cv2
import mediapipe as mp
import joblib  

import sys
import os
if hasattr(sys, '_MEIPASS'):
    # PyInstaller
    base_path = sys._MEIPASS
else:
    # En desarrollo
    base_path = os.path.abspath(".")

senas_path = os.path.join(base_path, 'senas.json')
modelo_path = os.path.join(base_path, 'modelo_senhas.pkl')

# Cargar el modelo entrenado
model = joblib.load("modelo_senhas.pkl")

# Inicializa MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar video")
        break

    # Voltea la imagen horizontalmente y conviértela a RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesa el cuadro con MediaPipe
    result = hands.process(rgb_frame)

    # Verifica si se detectan manos
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Dibuja puntos clave en la mano detectada
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extrae coordenadas de landmarks
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append([lm.x, lm.y, lm.z])

            # Aplana los landmarks y realiza la predicción
            flattened_landmarks = sum(landmarks, [])
            prediction = model.predict([flattened_landmarks])
            print("Sena detectada:", prediction[0])

            # Muestra la predicción en el video
            cv2.putText(frame, f"Sena: {prediction[0]}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Muestra el video en una ventana
    cv2.imshow("Detector de Senas", frame)

    # Presiona 'Esc' para salir
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
