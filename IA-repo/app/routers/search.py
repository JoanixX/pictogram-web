from fastapi import APIRouter
from app.core.arasaac import search_pictograms

router = APIRouter()

@router.get("/search/{word}")
def search(word: str):
    result = search_pictograms(word)
    if result:
        # Return the best match
        picto_id = result[0]["_id"]
        return {
            "palabra": word,
            "id": picto_id,
            "url": f"https://static.arasaac.org/pictograms/{picto_id}/{picto_id}_300.png",
            "keywords": result[0]["keywords"]
        }
    return None
