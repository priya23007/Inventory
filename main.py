from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from configuration import user_collection
from database.models import User
from auth import create_access_token, verify_password, get_password_hash, oauth2_scheme
from auth_dependencies import get_current_user

app = FastAPI(title="University Inventory API")

# NEW: Allowed roles
ALLOWED_ROLES = {"HQ_ADMIN", "CAMPUS_ADMIN"}  # NEW


@app.post("/signup")
async def signup(user: User):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(400, "User already exists")

    # NEW: Get role from user model or default to CAMPUS_ADMIN
    role = getattr(user, "role", "CAMPUS_ADMIN")  # NEW

    if role not in ALLOWED_ROLES:  # NEW
        raise HTTPException(400, "Invalid role. Allowed roles: HQ_ADMIN, CAMPUS_ADMIN")  # NEW

    hashed_pw = get_password_hash(user.password)

    user_collection.insert_one({
        "email": user.email,
        "password": hashed_pw,
        "role": role,  # NEW
    })

    return {"message": "User created successfully", "role": role}  # NEW


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(400, "User not found")

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(400, "Incorrect password")

    token_payload = {
        "sub": user["email"],       # ALWAYS EMAIL
        "role": user.get("role", "CAMPUS_ADMIN")
    }

    token = create_access_token(token_payload)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": token_payload["role"]
    }



@app.get("/profile")
async def profile(current_user: dict = Depends(get_current_user)):
    # NEW: make sure role is visible in profile
    return {
        "message": "Authorized user",
        "user": {
            "email": current_user.get("email"),
            "role": current_user.get("role", "CAMPUS_ADMIN")  # NEW
        }
    }


from router.college import router as college_router
from router.university import router as university_router

app.include_router(college_router)
app.include_router(university_router)

