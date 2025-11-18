import httpx

class AIClient:
    def __init__(self):
        self.url = "http://localhost:9000/predict"

    async def predict(self, image_bytes):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                files={"file": ("image.png", image_bytes, "image/png")}
            )
        return response.json()
