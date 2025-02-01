from fastapi import FastAPI
from app.routes import peer, file
app = FastAPI()
# to run the code - uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Include routes
app.include_router(peer.router, prefix="/peer", tags=["Peer"])
app.include_router(file.router, prefix="/file", tags=["File"])

@app.get("/")
async def root():
    return {"message": "Welcome to the DataPulse Tracker API"}
