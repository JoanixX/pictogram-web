import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a tu carpeta "data" con subcarpetas por clase
DATASET_PATH = r"D:\User\Downloads\dataset_big\dataset_big"

MODEL_OUTPUT = os.path.join(BASE_DIR, "pictogram_mobilenet.keras")

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15

print("Usando dataset en:", DATASET_PATH)

# ===============================
# DATA AUGMENTATION SOLO PARA TRAIN
# ===============================
train_datagen = ImageDataGenerator(
    validation_split=0.2,
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    shear_range=0.1
)

# VALIDACIÓN SIN AUGMENTATION
val_datagen = ImageDataGenerator(
    validation_split=0.2,
    rescale=1./255
)

train_gen = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_gen = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

num_classes = len(train_gen.class_indices)
print("\nClases detectadas:", train_gen.class_indices)

# ===============================
# MODELO: MobileNetV2 + capa de clasificación
# ===============================
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False  # congelamos el modelo base al inicio

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ===============================
# ENTRENAMIENTO INICIAL
# ===============================
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS
)

# ===============================
# OPCIONAL: FINE-TUNING (mejora la accuracy)
# ===============================
print("\nIniciando fine-tuning del modelo...")

base_model.trainable = True
# Congelamos las primeras capas (solo entrenamos las últimas capas)
for layer in base_model.layers[:100]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history_ft = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=5
)

# ===============================
# GUARDADO DEL MODELO FINAL
# ===============================
model.save(MODEL_OUTPUT)
print(f"\nModelo guardado en: {MODEL_OUTPUT}")
