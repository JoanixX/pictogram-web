import requests
from functools import lru_cache

@lru_cache(maxsize=100)
def search_pictograms(word):
    url = f"https://api.arasaac.org/v1/pictograms/es/search/{word}"
    try:
        print(f"DEBUG: Calling ARASAAC for: {word}")
        r = requests.get(url)
        data = r.json()
        print(f"DEBUG: ARASAAC response length: {len(data)}")
        return data
    except Exception as e:
        print(f"DEBUG: ARASAAC error: {e}")
        return []
