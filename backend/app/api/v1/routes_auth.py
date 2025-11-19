from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.models.user import User as UserModel
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

from app.core.security import decode_access_token


@router.get("/me")
def read_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    data = decode_access_token(token)
    if not data or "sub" not in data:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    user_id = int(data["sub"])
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return {"id": user.id, "username": user.username}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(username: str, password: str, db: Session = Depends(get_db)):
    exists = db.query(UserModel).filter(UserModel.username == username).first()
    if exists:
        raise HTTPException(status_code=400, detail="username already exists")
    user = UserModel(username=username, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=60 * 24 * 7)
    access_token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
