from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from app.utils.auth import get_current_peer
from app.utils.jwt import create_access_token
from app.database.connection import peer_collection
from fastapi import APIRouter, HTTPException, Depends
from app.models.peer import RegisterPeer, LoginPeer, UpdateBusyStatus

# Initialize router and password context
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    

@router.post("/register")
async def register_peer(peer_data: RegisterPeer):
    """
    Register a new peer in the system.

    Input:
        email:  unique email for the peer.
        password:  password for the peer.
        ip:  peer's IP address.
        port: peer's port.
    Expected result:
        A peer is saved in the database and marked as logged in.
    """
    # Check if the peer already exists
    existing_peer = await peer_collection.find_one({"email": peer_data.email})
    if existing_peer:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(peer_data.password)

    # Save peer to the database
    new_peer = {
        "email": peer_data.email,
        "password": hashed_password,
        "ip": peer_data.ip,
        "port": peer_data.port,
        "logged_in": False,
        "is_busy": False,
    }
    await peer_collection.insert_one(new_peer)
    return {"message": "Peer registered successfully"}


@router.post("/login")
async def login_peer(login_data: LoginPeer):
    """
    Authenticate a peer with email and password and issue a JWT.

    Input:
        email: the peer's email.
        password: the peer's password.
        ip: the peer's ip.
        port: the peer's port.
    Output:
        JWT and peer information.
    """
    print("here")
    peer = await peer_collection.find_one({"email": login_data.email})
    if not peer or not pwd_context.verify(login_data.password, peer["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Mark peer as logged in
    await peer_collection.update_one({"email": login_data.email}, {"$set": {"logged_in": True, "ip": login_data.ip, "port": login_data.port , "is_busy": False }})

    # Generate JWT token
    token = create_access_token(data={"email": peer["email"]})

    return {"access_token": token, "token_type": "bearer", "peer": {"email": peer["email"], "ip": peer["ip"], "port": peer["port"]}}

class LogoutRequest(BaseModel):
    email: EmailStr

@router.post("/logout")
async def logout_peer(request: LogoutRequest):
    """
    Log out a peer.

    Input:
        request: {
            "email": str - the peer's email.
        }
    Expected result:
        The peer's `logged_in` status is updated to `False`.
    """
    # Check if the peer exists
    peer = await peer_collection.find_one({"email": request.email})
    if not peer:
        raise HTTPException(status_code=404, detail="Peer not found")

    # Update logged_in status to False
    await peer_collection.update_one({"email": request.email}, {"$set": {"logged_in": False}})
    return {"message": "Logout successful"}

@router.post("/update_status")
async def update_busy_status(request: UpdateBusyStatus, current_peer=Depends(get_current_peer)):
    """
    Update the busy status of a peer.

    Input:
        request: {
            "email": str - the user's email.
            "is_busy": bool - the new busy status.
        }
    """
    email = request.email
    is_busy = request.is_busy
    # Ensure the peer exists
    peer = await peer_collection.find_one({"email": email})
    if not peer:
        raise HTTPException(status_code=404, detail="Peer not found")

    # Update the is_busy status
    await peer_collection.update_one({"email": email}, {"$set": {"is_busy": is_busy}})
    return {"message": f"Peer {email} is now {'busy' if is_busy else 'not busy'}"}
