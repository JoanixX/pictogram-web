from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.pictogram import PictogramPrediction
from app.schemas.pictogram import PredictionOut, PredictionCreate, PredictionUpdate
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/pictograms", tags=["Pictograms"])

@router.post("/predict", response_model=PredictionOut, status_code=status.HTTP_201_CREATED)
async def predict_image(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    service = PredictionService()
    result = await service.process(file)

    data = PredictionCreate(
        user_id=user_id,
        filename=file.filename,
        group_prediction=result.get("group", ""),
        description_prediction=result.get("description", ""),
        confidence=result.get("confidence", None),
    )

    db_item = PictogramPrediction(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


@router.post("/", response_model=PredictionOut, status_code=status.HTTP_201_CREATED)
def create_prediction_manual(payload: PredictionCreate, db: Session = Depends(get_db)):
    db_item = PictogramPrediction(**payload.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[PredictionOut])
def list_predictions(
    user_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    q = db.query(PictogramPrediction)
    if user_id is not None:
        q = q.filter(PictogramPrediction.user_id == user_id)
    items = q.offset(skip).limit(limit).all()
    return items


@router.get("/{prediction_id}", response_model=PredictionOut)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    item = db.query(PictogramPrediction).filter(PictogramPrediction.id == prediction_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="prediction not found")
    return item


@router.patch("/{prediction_id}", response_model=PredictionOut)
def update_prediction(prediction_id: int, payload: PredictionUpdate, db: Session = Depends(get_db)):
    item = db.query(PictogramPrediction).filter(PictogramPrediction.id == prediction_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="prediction not found")

    if payload.filename is not None:
        item.filename = payload.filename
    if payload.group_prediction is not None:
        item.group_prediction = payload.group_prediction
    if payload.description_prediction is not None:
        item.description_prediction = payload.description_prediction
    if payload.confidence is not None:
        item.confidence = payload.confidence

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    item = db.query(PictogramPrediction).filter(PictogramPrediction.id == prediction_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="prediction not found")
    db.delete(item)
    db.commit()
    return
