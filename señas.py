import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Captura de video
cap = cv2.VideoCapture(0)

def detectar_gero_señas(landmarks):
    """
    Función para detectar gestos específicos del lenguaje de señas.
    """
    # Coordenadas de los puntos clave de la mano
    thumb_tip = landmarks.landmark[4]   # Punta del dedo pulgar
    index_tip = landmarks.landmark[8]   # Punta del dedo índice
    middle_tip = landmarks.landmark[12] # Punta del dedo medio
    ring_tip = landmarks.landmark[16]   # Punta del dedo anular
    pinky_tip = landmarks.landmark[20]  # Punta del dedo meñique

    # Coordenadas de las bases de los dedos (más cerca de la palma)
    thumb_base = landmarks.landmark[2]
    index_base = landmarks.landmark[5]
    middle_base = landmarks.landmark[9]
    ring_base = landmarks.landmark[13]
    pinky_base = landmarks.landmark[17]

    # Definir las condiciones para los gestos con todos los dedos
    
    # Para la letra 'A' (solo el pulgar extendido, el resto de los dedos doblados)
    if (index_tip.y > index_base.y and 
        middle_tip.y > middle_base.y and 
        ring_tip.y > ring_base.y and 
        pinky_tip.y > pinky_base.y and 
        thumb_tip.y < thumb_base.y):
        return "Letra A (pulgar extendido)"

    # Para la letra 'B' (todos los dedos extendidos, excepto el pulgar)
    if (index_tip.y < index_base.y and
        middle_tip.y < middle_base.y and
        ring_tip.y < ring_base.y and
        pinky_tip.y < pinky_base.y and
        thumb_tip.y < thumb_base.y):
        return "Letra B (todos los dedos extendidos)"

    # Para la letra 'C' (forma de 'C', pulgar extendido y los otros dedos doblados)
    if (abs(index_tip.x - middle_tip.x) < 0.1 and
        abs(middle_tip.x - ring_tip.x) < 0.1 and
        abs(ring_tip.x - pinky_tip.x) < 0.1 and
        thumb_tip.y < thumb_base.y):
        return "Letra C (forma de C)"

    # Para la letra 'D' (solo el dedo índice extendido, el resto doblados)
    if (index_tip.y < index_base.y and 
        middle_tip.y > middle_base.y and 
        ring_tip.y > ring_base.y and 
        pinky_tip.y > pinky_base.y and 
        thumb_tip.y > thumb_base.y):
        return "Letra D (índice extendido)"

    # Para la letra 'F' (pulgar e índice formando un círculo, los demás dedos doblados)
    if (index_tip.y < index_base.y and 
        thumb_tip.y < thumb_base.y and 
        middle_tip.y > middle_base.y and 
        ring_tip.y > ring_base.y and 
        pinky_tip.y > pinky_base.y):
        return "Letra F (pulgar e índice formando círculo)"

    # Para la letra 'L' (índice y pulgar formando la letra L)
    if (index_tip.y < index_base.y and 
        pinky_tip.y > pinky_base.y and
        middle_tip.y > middle_base.y and
        ring_tip.y > ring_base.y and 
        thumb_tip.y < thumb_base.y and
        abs(index_tip.x - thumb_tip.x) < 0.1):
        return "Letra L (índice y pulgar extendidos)"

    # Para el número '1' (solo el dedo índice extendido)
    if (index_tip.y < index_base.y and
        middle_tip.y > middle_base.y and
        ring_tip.y > ring_base.y and
        pinky_tip.y > pinky_base.y and
        thumb_tip.y > thumb_base.y):
        return "Número 1 (índice extendido)"

    # Para el número '5' (todos los dedos extendidos)
    if (index_tip.y < index_base.y and
        middle_tip.y < middle_base.y and
        ring_tip.y < ring_base.y and
        pinky_tip.y < pinky_base.y and
        thumb_tip.y < thumb_base.y):
        return "Número 5 (todos los dedos extendidos)"

    # Para el número '0' (pulgar e índice formando un círculo)
    if (index_tip.y < index_base.y and
        thumb_tip.y < thumb_base.y and
        middle_tip.y > middle_base.y and
        ring_tip.y > ring_base.y and
        pinky_tip.y > pinky_base.y):
        return "Número 0 (pulgar e índice formando círculo)"

    return None

while cap.isOpened():
    ret, fotograma = cap.read()
    if not ret:
        break

    # Convertir la imagen a RGB (MediaPipe requiere imágenes RGB)
    imagen_rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)

    # Realizar la detección de manos
    resultados = hands.process(imagen_rgb)

    # Si se detectaron manos
    if resultados.multi_hand_landmarks:
        for landmarks in resultados.multi_hand_landmarks:
            # Dibujar las conexiones de los puntos de la mano
            mp_draw.draw_landmarks(fotograma, landmarks, mp_hands.HAND_CONNECTIONS)

            # Detectar el gesto de la mano (letras, números, etc.)
            gesto = detectar_gero_señas(landmarks)
            if gesto:
                cv2.putText(fotograma, gesto, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar el fotograma con la detección de las manos
    cv2.imshow("Reconocimiento de Lenguaje de Señas", fotograma)

    # Salir si presionas 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()