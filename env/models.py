from typing import Dict, Optional
from pydantic import BaseModel

class Action(BaseModel):
    signal: str  # NS_GREEN or EW_GREEN

class Observation(BaseModel):
    queues: Dict[str, int]
    emergency: Optional[str]
    time: int