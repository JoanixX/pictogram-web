# backend/app/api/v1/routes_ollama_stream.py
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import json
from ollama import Client

router = APIRouter()

@router.post("/ollama_stream")
async def ollama_stream(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"error": "No prompt provided"}

    client = Client()

    def event_stream():
        # Generamos el chat con streaming
        for chunk in client.chat(model="phi3:mini", messages=[{"role": "user", "content": prompt}], stream=True):
            # Cada chunk es un dict con contenido parcial
            text = chunk.get("content", "")
            if text:
                yield text.encode("utf-8")

    return StreamingResponse(event_stream(), media_type="text/plain")
