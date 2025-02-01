from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import verify_access_token
from app.database.connection import peer_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/peer/login")

async def get_current_peer(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get the current authenticated peer.

    Input:
        token: JWT token from the request.
    Output:
        Peer information from the token payload.
    """
    try:
        payload = verify_access_token(token)
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        peer = await peer_collection.find_one({"email": email, "logged_in": True})
        if not peer:
            raise HTTPException(status_code=401, detail="Peer not logged in")
        return peer
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
