from pydantic import BaseModel
from typing import List, Dict

class Chunk(BaseModel):
    order: int
    peers: List[str]  # List of emails of peers that own this chunk

class FileModel(BaseModel):
    file_name: str
    total_chunks: int
