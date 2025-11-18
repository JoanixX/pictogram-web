from app.services.ai_client import AIClient

class PredictionService:
    def __init__(self):
        self.ai = AIClient()

    async def process(self, file):
        content = await file.read()
        result = await self.ai.predict(content)
        return result
