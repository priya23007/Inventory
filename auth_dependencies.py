# auth_dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from configuration import user_collection
from auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")
        if not email:
            raise HTTPException(401, "Invalid token payload (no sub)")

        user = user_collection.find_one({"email": email})
        if not user:
            raise HTTPException(401, "User not found")

        return {
            "email": email,
            "id": str(user["_id"]),
            "role": payload.get("role") or user.get("role", "CAMPUS_ADMIN")
        }

    except JWTError:
        raise HTTPException(401, "Invalid or expired token")



def get_hq_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "HQ_ADMIN":
        raise HTTPException(403, "HQ admin access required")
    return current_user


def get_campus_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "CAMPUS_ADMIN":
        raise HTTPException(403, "Campus admin access required")
    return current_user
