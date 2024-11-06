import cv2
import torch
import sys
import ultralytics  

# Redirigir sys.stderr a un archivo de log
sys.stderr = open('error.log', 'w')
#pip install yolov5
#pip install yolov5
#pip install torch

# Cargar el modelo preentrenado de YOLOv5

modelo = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Diccionario de clases en español
clases_esp = {
    'person': 'persona',
    'bicycle': 'bicicleta',
    'car': 'coche',
    'motorbike': 'motocicleta',
    'aeroplane': 'avión',
    'bus': 'autobús',
    'train': 'tren',
    'truck': 'camión',
    'boat': 'barco',
    'traffic light': 'semáforo',
    'fire hydrant': 'hidrante',
    'stop sign': 'señal de stop',
    'parking meter': 'parquímetro',
    'bench': 'banco',
    'tie': 'corbata',
    'shirt': 'camisa',
    'jacket': 'casaca',
    'suit': 'traje',
    'hat': 'sombrero',
    'shoes': 'zapatos',
    'pants': 'pantalones',
    'shorts': 'pantalones cortos',
    'socks': 'calcetines',
    'scarf': 'bufanda',
    'gloves': 'guantes',
    'belt': 'cinturón',
    'suitcase': 'maleta',
    'umbrella': 'paraguas',
    'backpack': 'mochila',
    'wallet': 'billetera',
    'watch': 'reloj',
    'ring': 'anillo',
    'glasses': 'gafas',
    'sunglasses': 'gafas de sol',
    'tie clip': 'clip de corbata',
    'purse': 'bolso',
    'clutch': 'cartera',
    'computer': 'computadora',
    'laptop': 'portátil',
    'keyboard': 'teclado',
    'mouse': 'ratón',
    'monitor': 'pantalla',
    'printer': 'impresora',
    'scanner': 'escáner',
    'server': 'servidor',
    'headphones': 'auriculares',
    'webcam': 'cámara web',
    'microphone': 'micrófono',
    'cable': 'cable',
    'charger': 'cargador',
    'usb': 'usb',
    'flash drive': 'memoria usb',
    'router': 'enrutador',
    'switch': 'conmutador',
    'hard drive': 'disco duro',
    'tablet': 'tableta',
    'projector': 'proyector',
    'server rack': 'rack de servidores',
    'multimeter': 'multímetro',
    'soldering iron': 'soldador',
    'power strip': 'regleta de energía',
    'extension cord': 'extensión eléctrica',
    'circuit board': 'placa base',
    'monitor stand': 'soporte para monitor',
    'whiteboard': 'pizarra blanca',
    'desk': 'escritorio',
    'office chair': 'silla de oficina',
    'file cabinet': 'archivero',
    'paper': 'papel',
    'stapler': 'engrapadora',
    'pen': 'bolígrafo',
    'marker': 'marcador',
    'notebook': 'cuaderno',
    'mouse pad': 'alfombrilla para ratón',
    'post-it': 'nota adhesiva',
    'bottle':'botella',
    'cell phone':'celular',
    'chair': 'silla',
    'mouse': 'raton',
    
}

# Puedes imprimir el diccionario para verificar las clases
print(clases_esp)



cap = cv2.VideoCapture(0)  

while cap.isOpened():
    ret, fotograma = cap.read()
    if not ret:
        break
    
    # Realizar detección de objetos en el fotograma
    resultados = modelo(fotograma)
    
    # Obtener los resultados (detalles de las detecciones)
    predicciones = resultados.pred[0]  # Predicciones para el primer fotograma
    
    # Dibujar las cajas y mostrar las clases en español
    for *xyxy, conf, cls in predicciones:
        clase = resultados.names[int(cls)]  # Nombre de la clase en inglés
        clase_esp = clases_esp.get(clase, clase)  # Traducir la clase al español (si es posible)

        # Convertir las coordenadas a enteros
        xyxy = list(map(int, xyxy))
        
        # Dibujar la caja delimitadora
        cv2.rectangle(fotograma, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (255, 0, 0), 2)
        
        # Mostrar el nombre de la clase y la confianza
        cv2.putText(fotograma, f"{clase_esp} ({conf*100:.1f}%)", (xyxy[0], xyxy[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Mostrar el fotograma con las detecciones
    cv2.imshow('Detección en Video', fotograma)

    # Salir si presionas 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()