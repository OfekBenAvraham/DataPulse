from pydantic import BaseModel
from typing import List

class Chunk(BaseModel):
    order: int
    peers: List[str]  # List of emails of peers that own this chunk

class FileModel(BaseModel):
    name: str
    type: str
    total_chunks: int

class FileCheckRequest(BaseModel):
    name: str
    type: str