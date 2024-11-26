
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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

# Carga el dataset
with open("senas.json", "r") as f:
    data = json.load(f)

# Verifica que haya suficientes datos
if len(data) < 2:
    raise ValueError("El dataset tiene menos de 2 muestras, no se puede dividir en conjunto de entrenamiento y prueba.")

# Extrae landmarks y etiquetas
X = [sample["landmarks"] for sample in data]
y = [sample["label"] for sample in data]

# Aplana las listas de landmarks para usarlas en el modelo
X = [sum(landmark, []) for landmark in X]

# Divide en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrena un modelo Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evalúa el modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy * 100:.2f}%")

# Guarda el modelo entrenado
joblib.dump(model, "modelo_senhas.pkl")
print("Modelo guardado en 'modelo_senhas.pkl'")
