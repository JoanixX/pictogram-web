from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# New routers
from app.routers.recommend import router as recommend_router
from app.routers.chat import router as chat_router
from app.routers.auth import router as auth_router

# Existing routers (keeping for compatibility/image upload)
from app.routes.predict import router as predict_router
from app.api.v1.route_ollama_predict import router as sent_to_ollama

from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include new routers
app.include_router(recommend_router)
app.include_router(chat_router)
app.include_router(auth_router)

# Include existing routers
app.include_router(predict_router, prefix="/api")
app.include_router(sent_to_ollama, prefix="/api")