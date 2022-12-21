from pydantic import BaseModel
from typing import List, Any


class Message(BaseModel):
    method: str
    args: List[Any]