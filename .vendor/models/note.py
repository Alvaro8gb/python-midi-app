from pydantic import BaseModel


class Note(BaseModel):
    frequency: float
    duration: float
