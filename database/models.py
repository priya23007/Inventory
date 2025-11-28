from pydantic import BaseModel , EmailStr
from datetime import datetime 

class University_model(BaseModel):
    item_id: str
    item_name: str
    category: str
    quantity: int
    purchase_date: datetime
    expiry_date: datetime | None = None
    vendor_name: str 
    is_deleted: bool = False
    updated_at: float = datetime.timestamp(datetime.now())

class College_model(BaseModel):
    college_name: str
    item_name: str
    category: str
    quantity: int
    status: str = "pending"

class user_registration_model(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class user_login_model(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    password: str
    

