# from fastapi import FastAPI, APIRouter, HTTPException, Depends
# from configuration import university_collection, college_collection, qr_collection
# from database.schemas import all_task
# from database.schemas import individual_data
# from database.models import University_model,College_model
# from bson.objectid import ObjectId
# from datetime import datetime
# from auth_dependencies import get_current_user
# #import pyqrcode 

# router = APIRouter()

# @router.post("/request", tags=["Campus"])
# async def create_request(request:College_model,current_user: str = Depends(get_current_user)):
#     try:
#         request = request.dict()
#         request["status"] = "pending"
#         request["request_at"] = datetime.now()
#         resp = college_collection.insert_one(dict(request))
#         return {"status_code":200, "id":str(resp.inserted_id)}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")
    
# @router.get("/campus/approved_requests", tags=["Campus"])
# async def track_approved_requests(current_user: str = Depends(get_current_user)):
#     try:
#         data = college_collection.find({"status":"approved"})
#         return {"status_code":200, "data":all_task(data)}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")
    
# @router.post("/assign", tags=["Campus"])
# async def assign_items(data:College_model,current_user: str = Depends(get_current_user)):
#     try:
#         resp = college_collection.find({"status":"approved"})
#         return{"status_code":200, "data":all_task(resp)}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")

# @router.get("/campus/requests", tags=["Campus"])
# async def get_campus_requests(current_user: str = Depends(get_current_user)):
#     try:
#         data = college_collection.find({"status":"pending"})
#         return {"status_code":200, "data":all_task(data)}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")
    
# @router.put("/stock/{item_id}", tags=["Campus"])
# async def campus_stock(item_id:str,current_user: str = Depends(get_current_user)):
#     try:
#         resp = college_collection.find_one({"_id":ObjectId(item_id), "status":"approved"})
#         if not resp:
#             return HTTPException(status_code=404, detail=f"Request not found")
#         if resp.get("status") != "approved":
#             return HTTPException(status_code=400, detail=f"Request not approved")
#         college_collection.update_one({"_id": ObjectId(item_id)},{"$set": {"status": "assigned", "assigned_at": datetime.now()}})
#         return {"status_code": 200, "message": "Inventory assigned", "id": str(resp["_id"])} 
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")

# @router.get("/track_stock", tags=["Campus"])
# async def track_stock(current_user: str = Depends(get_current_user)):
#     try:
#         data = university_collection.find({"is_deleted":False})
#         return {"status_code":200, "data":all_task(data)}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")

# @router.get("/assign", tags=["Campus"])
# async def assign_items(current_user: str = Depends(get_current_user)):
#     try:
#         resp = college_collection.find({"status":"approved"})
#         return{"status_code":200, "data":all_task(resp)}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")



from fastapi import FastAPI, APIRouter, HTTPException, Depends
from configuration import university_collection, college_collection, qr_collection
from database.schemas import all_task
from database.schemas import individual_data
from database.models import University_model,College_model
from bson.objectid import ObjectId
from datetime import datetime
# CHANGED: import campus-role guard
from auth_dependencies import get_current_user, get_campus_admin_user

router = APIRouter()

@router.post("/request", tags=["Campus"])
async def create_request(
    request: College_model,
    # CHANGED: only CAMPUS_ADMIN can hit this
    current_user: dict = Depends(get_campus_admin_user)
):
    try:
        request = request.dict()
        request["status"] = "pending"
        request["request_at"] = datetime.now()
        resp = college_collection.insert_one(dict(request))
        return {"status_code":200, "id":str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")
    
@router.get("/campus/approved_requests", tags=["Campus"])
async def track_approved_requests(
    current_user: dict = Depends(get_campus_admin_user)
):
    try:
        data = college_collection.find({"status":"approved"})
        return {"status_code":200, "data":all_task(data)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")
    
@router.post("/assign", tags=["Campus"])
async def assign_items(
    data: College_model,
    current_user: dict = Depends(get_campus_admin_user)
):
    try:
        resp = college_collection.find({"status":"approved"})
        return{"status_code":200, "data":all_task(resp)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")

@router.get("/campus/requests", tags=["Campus"])
async def get_campus_requests(
    current_user: dict = Depends(get_campus_admin_user)
):
    try:
        data = college_collection.find({"status":"pending"})
        return {"status_code":200, "data":all_task(data)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")
    
@router.put("/stock/{item_id}", tags=["Campus"])
async def campus_stock(
    item_id: str,
    current_user: dict = Depends(get_campus_admin_user)
):
    try:
        resp = college_collection.find_one({"_id":ObjectId(item_id), "status":"approved"})
        if not resp:
            return HTTPException(status_code=404, detail=f"Request not found")
        if resp.get("status") != "approved":
            return HTTPException(status_code=400, detail=f"Request not approved")
        college_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {"status": "assigned", "assigned_at": datetime.now()}}
        )
        return {"status_code": 200, "message": "Inventory assigned", "id": str(resp["_id"])} 
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")

@router.get("/track_stock", tags=["Campus"])
async def track_stock(
    current_user: dict = Depends(get_campus_admin_user)
):
    try:
        data = university_collection.find({"is_deleted":False})
        return {"status_code":200, "data":all_task(data)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")

@router.get("/assign", tags=["Campus"])
async def assign_items(
    current_user: dict = Depends(get_campus_admin_user)
):
    try:
        resp = college_collection.find({"status":"approved"})
        return{"status_code":200, "data":all_task(resp)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")
