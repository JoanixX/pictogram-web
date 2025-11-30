from fastapi import APIRouter, UploadFile, File, Form
from ollama import Client
from PIL import Image
import io
import tensorflow as tf
import numpy as np
import os

router = APIRouter()

# =============================
# Carga del modelo de pictogramas
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels from app/api/v1 to app, then to models
MODEL_PATH = os.path.join(BASE_DIR, "..", "..", "models", "pictogram_mobilenet.keras")
CLASS_MAP_PATH = os.path.join(BASE_DIR, "..", "..", "models", "classes.txt")

model = tf.keras.models.load_model(MODEL_PATH)

class_map = {}
with open(CLASS_MAP_PATH, "r", encoding="utf-8") as f:
    for line in f:
        idx, name = line.strip().split(":")
        class_map[int(idx)] = name

IMG_SIZE = (224, 224)

# =============================
# Cliente Ollama
# =============================
client = Client(host="http://localhost:11434")

# =============================
# Endpoint que recibe texto y/o imagen
# =============================
@router.post("/ollama")
async def send_to_ollama(
    text: str = Form(...),
    file: UploadFile | None = File(None)
):
    # Si hay imagen, predecir su clase
    pictogram_text = ""
    if file:
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize(IMG_SIZE)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = model.predict(img_array)
        class_id = int(np.argmax(preds[0]))
        confidence = float(np.max(preds[0]))
        class_name = class_map[class_id]

        pictogram_text = f"Se subió una imagen que representa: {class_name}"

    # Combinar texto del usuario + descripción de la imagen
    full_message = text
    if pictogram_text:
        full_message += f"\n{pictogram_text}"

    # Llamada a Ollama
    response = client.chat(
        model="phi3:mini",  # cambia por tu modelo
        messages=[{"role": "user", "content": full_message}]
    )

    return {"response": response.message.content}
