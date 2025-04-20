from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import JSONResponse

from app.auth.security import verify_client_credentials
from app.core.config import settings

router = APIRouter()


@router.post("/token")
async def generate_token(client_id: str = Form(...), client_secret: str = Form(...)):

    if not verify_client_credentials(client_id, client_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials",
        )

    access_token = create_access_token({"sub": client_id})
    token_type = "bearer"
    expires_in = 3600

    return JSONResponse(
        {
            "access_token": access_token,
            "token_type": token_type,
            "expires_in": expires_in,
        }
    )


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
