from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes_users import router as users_router
from app.api.v1.routes_pictograms import router as pictograms_router
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_chat import router as chat_router
from app.db.session import engine
from app.db.base import Base
from app.routes.predict import router as predict_router
from app.api.v1.routes_ollama_stream import router as ollama_stream_router
from app.api.v1.route_ollama_predict import router as sent_to_ollama


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow all origins for development -- restrict in production
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(pictograms_router, prefix="/api/v1/pictograms", tags=["Pictograms"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
app.include_router(predict_router, prefix="/api")
app.include_router(ollama_stream_router, prefix="/api")
app.include_router(sent_to_ollama, prefix="/api")