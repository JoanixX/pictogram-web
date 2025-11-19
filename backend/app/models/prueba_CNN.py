import tensorflow as tf
import numpy as np
from PIL import Image

# Cargar modelo
model = tf.keras.models.load_model(r"D:\User\onedrive\Documentos\IA_web_proyect\pictogram-web\backend\app\models\pictogram_mobilenet.keras")

# Cargar etiquetas
class_map = {}
with open(r"D:\User\onedrive\Documentos\IA_web_proyect\pictogram-web\backend\app\models\classes.txt", "r", encoding="utf-8") as f:
    for line in f:
        idx, label = line.strip().split(":")
        class_map[int(idx)] = label

def preprocess_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize((224, 224))       # o el tamaño que usaste
    img = np.array(img) / 255.0        # normalizar
    img = np.expand_dims(img, axis=0)  # batch de 1
    return img


image_path = r"D:\User\onedrive\Documentos\TP-1ASI0404-12621-grupo1\data\numeros\catorce_29266.png"
img = preprocess_image(image_path)

pred = model.predict(img)
pred_class = np.argmax(pred)
print("Predicción:", class_map[pred_class])
