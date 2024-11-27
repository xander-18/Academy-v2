import cv2
import mediapipe as mp
import json

# Inicializa MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Inicializa captura de video
cap = cv2.VideoCapture(0)

dataset = []  # Lista para almacenar los datos capturados
current_label = None  # Etiqueta activa

print("Presiona 'c' para cambiar el label activo, 's' para guardar una muestra, y 'Esc' para salir.")

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
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extrae coordenadas de landmarks
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append([lm.x, lm.y, lm.z])

            # Guarda la muestra con la etiqueta activa
            if cv2.waitKey(1) & 0xFF == ord("s"):
                if current_label:
                    dataset.append({"landmarks": landmarks, "label": current_label})
                    print(f"Muestra guardada con etiqueta: {current_label}")
                else:
                    print("Primero define un label activo presionando 'c'.")

    # Cambia el label activo
    if cv2.waitKey(1) & 0xFF == ord("c"):
        current_label = input("Introduce el nuevo label activo: ")
        print(f"Label activo cambiado a: {current_label}")

    # Muestra el video en una ventana
    cv2.imshow("Capturador de Datos", frame)

    # Presiona 'Esc' para salir
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()

# Guarda el dataset en un archivo JSON
with open("senas.json", "w") as f:
    json.dump(dataset, f)

print("Dataset guardado en 'senas.json'")
