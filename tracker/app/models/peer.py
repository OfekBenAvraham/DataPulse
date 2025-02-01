from pydantic import BaseModel, EmailStr

class PeerModel(BaseModel):
    email: EmailStr
    password: str
    ip: str
    port: int
    logged_in: bool
    is_busy: bool

class RegisterPeer(BaseModel):
    email: EmailStr
    password: str
    ip: str
    port: int

class LoginPeer(BaseModel):
    email: EmailStr
    password: str
    ip: str
    port: int

class UpdateBusyStatus(BaseModel):
    email: EmailStr  # EmailStr is from Pydantic and ensures a valid email format
    is_busy: bool
    
    