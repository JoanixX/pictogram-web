from fastapi import FastAPI
from app.api.v1.routes_users import router as users_router
from app.api.v1.routes_pictograms import router as pictograms_router
from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(pictograms_router, prefix="/api/v1/pictograms", tags=["Pictograms"])
