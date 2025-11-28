# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from configuration import user_collection
# from jwt_handler import SECRET_KEY, ALGORITHM

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token payload")

#         user = user_collection.find_one({"email": email})
#         if user is None:
#             raise HTTPException(status_code=401, detail="User not found")

#         return {"email": user["email"], "id": str(user["_id"])}

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")


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

        # CHANGED: include role in the returned dict
        return {
            "email": user["email"],
            "id": str(user["_id"]),
            "role": user.get("role", "CAMPUS_ADMIN"),  # default for old users
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# NEW: only HQ_ADMIN can access
def get_hq_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "HQ_ADMIN":
        raise HTTPException(status_code=403, detail="HQ admin access required")
    return current_user


# NEW: only CAMPUS_ADMIN can access
def get_campus_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "CAMPUS_ADMIN":
        raise HTTPException(status_code=403, detail="Campus admin access required")
    return current_user
