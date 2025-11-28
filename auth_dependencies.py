from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from configuration import user_collection
from jwt_handler import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = user_collection.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return {"email": user["email"], "id": str(user["_id"])}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
