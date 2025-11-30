from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from typing import Dict
from pydantic import BaseModel

from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# In-memory user store (Cache)
# Format: {username: {"id": int, "username": str, "password_hash": str}}
fake_users_db: Dict[str, dict] = {}
user_id_counter = 1

class UserCreate(BaseModel):
    username: str
    password: str

@router.get("/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    data = decode_access_token(token)
    if not data or "sub" not in data:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    user_id = int(data["sub"])
    # Find user by ID in our fake db
    user = next((u for u in fake_users_db.values() if u["id"] == user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return {"id": user["id"], "username": user["username"]}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    global user_id_counter
    if user_data.username in fake_users_db:
        raise HTTPException(status_code=400, detail="username already exists")
    
    hashed_password = get_password_hash(user_data.password)
    new_user = {
        "id": user_id_counter,
        "username": user_data.username,
        "password_hash": hashed_password
    }
    fake_users_db[user_data.username] = new_user
    user_id_counter += 1
    
    return {"id": new_user["id"], "username": new_user["username"]}

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"DEBUG: Login attempt for user: {form_data.username}")
    print(f"DEBUG: Current users in DB: {list(fake_users_db.keys())}")
    
    user = fake_users_db.get(form_data.username)
    if not user:
        print("DEBUG: User not found")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not verify_password(form_data.password, user["password_hash"]):
        print("DEBUG: Password mismatch")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=60 * 24 * 7)
    access_token = create_access_token(subject=str(user["id"]), expires_delta=access_token_expires)
    print("DEBUG: Login successful")
    return {"access_token": access_token, "token_type": "bearer"}
