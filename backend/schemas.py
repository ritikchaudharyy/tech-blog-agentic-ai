from pydantic import BaseModel

class GenerateDraftRequest(BaseModel):
    topic: str
    platform: str = "blogger"
