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
    Aquí mapeamos la letra 'A' como ejemplo, con las condiciones para los dedos.
    """
    # Coordenadas de los puntos clave de la mano
    thumb_tip = landmarks.landmark[4]   # Punta del dedo pulgar
    index_tip = landmarks.landmark[8]   # Punta del dedo índice
    middle_tip = landmarks.landmark[12] # Punta del dedo medio
    ring_tip = landmarks.landmark[16]   # Punta del dedo anular
    pinky_tip = landmarks.landmark[20]  # Punta del dedo meñique

    # Definir las condiciones para la letra 'A' (solo el pulgar extendido)
    if index_tip.y > thumb_tip.y and middle_tip.y > thumb_tip.y and ring_tip.y > thumb_tip.y and pinky_tip.y > thumb_tip.y:
        return "Letra A (pulgar extendido)"
    
    # Para la letra 'B' (todos los dedos extendidos, excepto el pulgar)
    if thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y and thumb_tip.y < ring_tip.y and thumb_tip.y < pinky_tip.y:
        if index_tip.y < middle_tip.y and middle_tip.y < ring_tip.y and ring_tip.y < pinky_tip.y:
            return "Letra B (todos los dedos extendidos)"

    # Para la letra 'C' (pulgar y los dedos doblados en forma de 'C')
    if index_tip.y > thumb_tip.y and middle_tip.y > thumb_tip.y and ring_tip.y > thumb_tip.y and pinky_tip.y > thumb_tip.y:
        if (abs(index_tip.x - middle_tip.x) < 0.1) and (abs(middle_tip.x - ring_tip.x) < 0.1) and (abs(ring_tip.x - pinky_tip.x) < 0.1):
            return "Letra C (forma de C)"
    
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

            # Detectar el gesto de la mano (por ejemplo, letra 'A', 'B', etc.)
            gesto = detectar_gero_señas(landmarks)
            if gesto:
                cv2.putText(fotograma, gesto, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar el fotograma con la detección de las manos
    cv2.imshow("Detección de Manos", fotograma)

    # Salir si presionas 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
