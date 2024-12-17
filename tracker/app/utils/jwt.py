from datetime import datetime, timedelta
from jose import JWTError, jwt

# Secret key for signing JWTs (replace with a secure key in production)
SECRET_KEY = "RAnxWEYFC6Nq6bpd08YF_C1FmsdA0udixa1JuxIMN4I"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token validity period in minutes

def create_access_token(data: dict):
    """
    Create a JWT access token.

    Input:
        data (dict): Payload to include in the token.
    Output:
        str: Encoded JWT.
    """
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """
    Verify a JWT token and return its payload.

    Input:
        token (str): Encoded JWT.
    Output:
        dict: Decoded token payload.
    Raises:
        JWTError: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError("Invalid or expired token") from e
