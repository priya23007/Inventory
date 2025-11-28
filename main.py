from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from configuration import user_collection
from database.models import User
from auth import create_access_token, verify_password, get_password_hash, oauth2_scheme
from auth_dependencies import get_current_user

app = FastAPI(title="University Inventory API")

@app.post("/signup")
async def signup(user: User):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(400, "User already exists")

    hashed_pw = get_password_hash(user.password)

    user_collection.insert_one({
        "email": user.email,
        "password": hashed_pw
    })

    return {"message": "User created successfully"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"email": form_data.username})

    if not user:
        raise HTTPException(400, "User not found")

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(400, "Incorrect password")

    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/profile")
async def profile(current_user: dict = Depends(get_current_user)):
    return {"message": "Authorized user", "user": current_user}


from router.college import router as college_router
from router.university import router as university_router

app.include_router(college_router)
app.include_router(university_router)
