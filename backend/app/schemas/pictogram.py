from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PredictionBase(BaseModel):
    filename: Optional[str] = None
    group_prediction: str
    description_prediction: str
    confidence: Optional[float] = None

class PredictionCreate(PredictionBase):
    user_id: int

class PredictionUpdate(BaseModel):
    filename: Optional[str] = None
    group_prediction: Optional[str] = None
    description_prediction: Optional[str] = None
    confidence: Optional[float] = None

class PredictionOut(PredictionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
