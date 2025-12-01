from fastapi import APIRouter, UploadFile, File
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

router = APIRouter()

# =============================
# CARGA DEL MODELO Y CLASES
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Assuming models are in IA-repo/app/models
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "pictogram_mobilenet.keras")
CLASS_MAP_PATH = os.path.join(BASE_DIR, "..", "models", "classes.txt")

print(f"Loading model from: {MODEL_PATH}")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Modelo cargado.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Cargar mapeo class_id -> nombre
class_map = {}
try:
    with open(CLASS_MAP_PATH, "r", encoding="utf-8") as f:
        for line in f:
            idx, name = line.strip().split(":")
            class_map[int(idx)] = name
except Exception as e:
    print(f"Error loading class map: {e}")

IMG_SIZE = (224, 224)

# =============================
# ENDPOINT
# =============================
@router.post("/api/predict")
async def predict_image(file: UploadFile = File(...)):
    if not model:
        return {"error": "Model not loaded"}

    # Leer bytes
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # Preprocesado igual que el entrenamiento
    img = img.resize(IMG_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predicción
    preds = model.predict(img_array)
    class_id = int(np.argmax(preds[0]))
    confidence = float(np.max(preds[0]))
    class_name = class_map.get(class_id, "Unknown")

    return {
        "class_id": class_id,
        "class_name": class_name,
        "confidence": round(confidence, 4)
    }
