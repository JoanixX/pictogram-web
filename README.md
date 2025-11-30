# PictoChat - Asistente de Comunicación con Pictogramas

PictoChat es una aplicación web diseñada para facilitar la comunicación a través de pictogramas, potenciada por Inteligencia Artificial. Permite a los usuarios convertir texto a pictogramas en tiempo real, construir oraciones, y aprender de manera interactiva con "Chambi", el asistente virtual.

## 🚀 Características Principales

- **Aprende con Chambi**: Un chat interactivo donde un asistente virtual (Capibara) te enseña pictogramas y responde a tus mensajes.
- **Chat en Tiempo Real**: Conversa en salas de chat donde tus mensajes se convierten automáticamente en secuencias de pictogramas.
- **Constructor de Oraciones**: Herramienta para crear frases seleccionando pictogramas sugeridos por IA.
- **Reconocimiento de Imágenes**: Sube una foto y la IA identificará qué es y te mostrará el pictograma correspondiente.
- **Autenticación de Usuarios**: Sistema de registro e inicio de sesión seguro.

## 🛠️ Tecnologías Utilizadas

### Frontend

- **React** + **Vite**: Framework principal.
- **Tailwind CSS**: Estilizado moderno y responsivo.
- **Shadcn/ui**: Componentes de UI reutilizables y accesibles.
- **Lucide React**: Iconografía.

### Backend

- **FastAPI**: Framework de Python para la API REST y WebSockets.
- **ARASAAC API**: Fuente de pictogramas.
- **TensorFlow/Keras**: Para la clasificación de imágenes (si aplica).
- **Spacy**: Procesamiento de Lenguaje Natural (NLP).

## 📋 Requisitos Previos

- **Node.js** (v16 o superior)
- **Python** (v3.9 o superior)

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto localmente.

### 1. Configurar el Backend

Navega a la carpeta del backend e instala las dependencias:

```bash
cd backend
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
# Activar entorno virtual:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo de lenguaje de Spacy
python -m spacy download es_core_news_lg
```

### 2. Configurar el Frontend

Navega a la carpeta del frontend e instala las dependencias:

```bash
cd frontend
npm install
```

## ▶️ Ejecución

Necesitarás dos terminales abiertas.

### Terminal 1: Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8001
```

El servidor estará corriendo en `http://127.0.0.1:8001`.

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

La aplicación web estará disponible generalmente en `http://localhost:5173`.

## 🧪 Uso de la Aplicación

1. **Registro**: Al abrir la app, ve a "Aprende con Chambi" o "Chat en Tiempo Real" y regístrate con un usuario y contraseña.
2. **Chat**: Escribe mensajes para ver cómo se transforman en pictogramas.
3. **Imágenes**: En el chat con Chambi, usa el botón de subir imagen para que la IA la analice.

## ⚠️ Notas Importantes

- **Persistencia**: Actualmente, la base de datos de usuarios es **volátil (en memoria)**. Si reinicias el backend, los usuarios registrados se borrarán y deberás registrarte nuevamente.
- **Puertos**: Asegúrate de que el puerto `8001` esté libre para el backend.

## 👥 Autores

- Juan José Rodríguez
- Joaquin Alvarado
