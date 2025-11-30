from app.core.nlp import nlp
from app.core.fallback import NEXT_POS_RULES, POS_SEEDS, SEMANTIC_RULES

class GPT2Predictor:
    def __init__(self):
        # Placeholder for GPT-2 model
        # In a real implementation, this would load the quantized model
        pass

    def predict_next_words(self, text, top_k=20):
        # Mock implementation using Spacy/Rules as a fallback
        # This simulates the "Hybrid" behavior by using the rule-based logic
        # but wrapping it in the expected class structure.
        
        if not text:
             return ["yo", "tú", "quiero", "necesito"]
        words = text.split()
        if not words:
            return ["yo", "tú", "quiero", "necesito"]

        last = words[-1]
        doc = nlp(last)
        
        if not doc or len(doc) == 0:
             return ["yo", "tú", "quiero", "necesito"]

        pos = doc[0].pos_

        expected = NEXT_POS_RULES.get(pos, ["NOUN"])
        
        candidates = []
        # 1. Semantic Context
        if last.lower() in SEMANTIC_RULES:
            candidates.extend(SEMANTIC_RULES[last.lower()])
        
        # 2. Grammatical Fallback
        for cat in expected:
            candidates.extend(POS_SEEDS.get(cat, []))
            
        return candidates[:top_k]

predictor = GPT2Predictor()
