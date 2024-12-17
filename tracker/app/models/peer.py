from pydantic import BaseModel, EmailStr

class PeerModel(BaseModel):
    email: EmailStr
    password: str
    ip: str
    port: int
    logged_in: bool
    last_active: str

class RegisterPeer(BaseModel):
    email: EmailStr
    password: str
    ip: str
    port: int

class LoginPeer(BaseModel):
    email: EmailStr
    password: str
