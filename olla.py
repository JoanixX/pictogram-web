import tensorflow as tf
model = tf.keras.models.load_model(r"D:\User\onedrive\Documentos\IA_web_proyect\pictogram-web\backend\app\models\pictogram_mobilenet.keras")
print(model.summary())
