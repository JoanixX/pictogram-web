from fastapi import APIRouter
from app.core.nlp import nlp
from app.core.arasaac import search_pictograms
from app.core.rules import NEXT_POS_RULES, POS_SEEDS, SEMANTIC_RULES

router = APIRouter()

@router.post("/recommend")
def recommend(data: dict):
    words = data.get("selected", [])

    if not words:
        # Default recommendations for empty input
        candidates = ["yo", "tú", "quiero", "necesito"]
    else:
        last = words[-1]
        doc = nlp(last)
        
        # Default if NLP fails
        if not doc or len(doc) == 0:
             candidates = ["yo", "tú", "quiero", "necesito"]
        else:
            pos = doc[0].pos_
            expected = NEXT_POS_RULES.get(pos, ["NOUN"])

            candidates = []
            # 1. Semantic Context
            if last.lower() in SEMANTIC_RULES:
                candidates.extend(SEMANTIC_RULES[last.lower()])
            
            # 2. Grammatical Fallback (Always add these too, like gpt2_predictor)
            for cat in expected:
                candidates.extend(POS_SEEDS.get(cat, []))

    # Deduplicate while preserving order
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            unique_candidates.append(c)
            seen.add(c)
            
    # Limit to top 20
    unique_candidates = unique_candidates[:20]

    pictos = []
    for w in unique_candidates:
        result = search_pictograms(w)
        if result:
            picto_id = result[0]["_id"]
            pictos.append({
                "palabra": w,
                "id": picto_id,
                "url": f"https://static.arasaac.org/pictograms/{picto_id}/{picto_id}_300.png",
                "keywords": result[0]["keywords"]
            })

    return {
        "recommended": pictos
    }
