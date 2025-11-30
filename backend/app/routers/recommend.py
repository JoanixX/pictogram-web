from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.core.gpt2_predictor import predictor
from app.core.arasaac import search_pictograms

router = APIRouter(prefix="/recommend", tags=["Recommendation"])

class RecommendRequest(BaseModel):
    selected: List[str]

@router.post("/")
def recommend(data: RecommendRequest):
    words = data.selected
    text = " ".join(words)
    
    print(f"DEBUG: Recommend request for text: '{text}'")
    candidates = predictor.predict_next_words(text)
    print(f"DEBUG: Candidates: {candidates}")
    
    pictos = []
    seen_ids = set()
    
    for w in candidates:
        result = search_pictograms(w)
        if result:
            for res in result:
                picto_id = res["_id"]
                if picto_id not in seen_ids:
                    pictos.append({
                        "palabra": w,
                        "id": picto_id,
                        "url": f"https://static.arasaac.org/pictograms/{picto_id}/{picto_id}_300.png",
                        "keywords": res["keywords"]
                    })
                    seen_ids.add(picto_id)
                    break
        
        if len(pictos) >= 12:
            break

    return {
        "recommended": pictos
    }

@router.post("/convert")
def convert_to_pictograms(data: RecommendRequest):
    words = data.selected
    pictos = []
    
    for w in words:
        result = search_pictograms(w)
        if result:
            res = result[0]
            picto_id = res["_id"]
            pictos.append({
                "palabra": w,
                "id": picto_id,
                "url": f"https://static.arasaac.org/pictograms/{picto_id}/{picto_id}_300.png",
                "keywords": res.get("keywords", [])
            })
        else:
            pass

    return {
        "pictograms": pictos
    }
