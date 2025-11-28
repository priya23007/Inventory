# from fastapi import FastAPI, APIRouter, HTTPException, Depends
# from configuration import university_collection, college_collection
# from database.schemas import all_task
# from database.schemas import individual_data
# from database.models import University_model,College_model
# from bson.objectid import ObjectId
# from datetime import datetime
# from auth_dependencies import get_current_user

# router = APIRouter()

# @router.put("/campus/requests/{request_id}", tags=["University"])
# async def approve_reject(request_id:str, status:str, current_user: str = Depends(get_current_user)):
#     try:
#         id = ObjectId(request_id)
#         exesting = college_collection.find_one({"_id":id, "status":"pending"})
#         if not exesting:
#             return HTTPException(status_code=404, detail=f"Request not found")
#         elif status not in ["approved", "rejected"]:
#             return HTTPException(status_code=400, detail=f"Might be approved or rejected")
#             id = ObjectId(request_id)
#             existing = college_collection.find_one({"_id": id, "status": "pending"})
#         resp = college_collection.update_one({"_id":id}, {"$set":{"status":status}})
#         return {"status_code":200, "message":f"Request {status} successfully"}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")    

# @router.post("/", tags=["University"])
# async def create_stock(new_task: University_model,current_user: str = Depends(get_current_user)):
#     try:
#         resp = university_collection.insert_one(dict(new_task))
#         return{"status_code":200, "id":("resp.inserted_id")}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured{e}")
    
# @router.get("/university/stock", tags=["University"])
# async def get_stock(current_user: str = Depends(get_current_user)):
#     data = university_collection.find({"is_deleted":False})
#     return all_task(data)

# @router.put("/{item_id}", tags=["University"])
# async def update_stock(item_id:str, updated_task:University_model,current_user: str = Depends(get_current_user)):
#     try:
#         id = ObjectId(item_id)
#         exesting_doc = university_collection.find_one({"_id":id, "is_deleted":False})
#         if not exesting_doc:
#             return HTTPException(status_code=404, detail=f"Stock does not exits")
#         updated_task.updated_at = datetime.timestamp(datetime.now())
#         resp = university_collection.update_one({"_id":id}, {"$set":dict(updated_task)})
#         return {"status_code":200, "message": "Stock Updated Successfully"}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")
    
# @router.delete("/{item_id}", tags=["University"])
# async def delete_stock(item_id:str,current_user: str = Depends(get_current_user)):
#     try:
#         id = ObjectId(item_id)
#         exesting_doc = university_collection.find_one({"_id":id, "is_deleted":False})
#         if not exesting_doc:
#             return HTTPException(status_code=404, detail=f"Stock does not exits")
#         resp = university_collection.update_one({"_id":id},{"$set":{"is_deleted":True}})
#         raise {"status_code":200, "message":"Stock deleted Successfully"}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Some error occured {e}")


from fastapi import FastAPI, APIRouter, HTTPException, Depends
from configuration import university_collection, college_collection
from database.schemas import all_task
from database.schemas import individual_data
from database.models import University_model,College_model
from bson.objectid import ObjectId
from datetime import datetime
# CHANGED: import HQ-role guard
from auth_dependencies import get_current_user, get_hq_admin_user

router = APIRouter()

@router.put("/campus/requests/{request_id}", tags=["University"])
async def approve_reject(
    request_id: str,
    status: str,
    # CHANGED: only HQ_ADMIN can approve/reject
    current_user: dict = Depends(get_hq_admin_user)
):
    try:
        id = ObjectId(request_id)
        exesting = college_collection.find_one({"_id":id, "status":"pending"})
        if not exesting:
            return HTTPException(status_code=404, detail=f"Request not found")
        elif status not in ["approved", "rejected"]:
            return HTTPException(status_code=400, detail=f"Might be approved or rejected")
            id = ObjectId(request_id)
            existing = college_collection.find_one({"_id": id, "status": "pending"})
        resp = college_collection.update_one({"_id":id}, {"$set":{"status":status}})
        return {"status_code":200, "message":f"Request {status} successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")    

@router.post("/", tags=["University"])
async def create_stock(
    new_task: University_model,
    current_user: dict = Depends(get_hq_admin_user)
):
    try:
        resp = university_collection.insert_one(dict(new_task))
        return{"status_code":200, "id":("resp.inserted_id")}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured{e}")
    
@router.get("/university/stock", tags=["University"])
async def get_stock(
    current_user: dict = Depends(get_hq_admin_user)
):
    data = university_collection.find({"is_deleted":False})
    return all_task(data)

@router.put("/{item_id}", tags=["University"])
async def update_stock(
    item_id: str,
    updated_task: University_model,
    current_user: dict = Depends(get_hq_admin_user)
):
    try:
        id = ObjectId(item_id)
        exesting_doc = university_collection.find_one({"_id":id, "is_deleted":False})
        if not exesting_doc:
            return HTTPException(status_code=404, detail=f"Stock does not exits")
        updated_task.updated_at = datetime.timestamp(datetime.now())
        resp = university_collection.update_one({"_id":id}, {"$set":dict(updated_task)})
        return {"status_code":200, "message": "Stock Updated Successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")
    
@router.delete("/{item_id}", tags=["University"])
async def delete_stock(
    item_id: str,
    current_user: dict = Depends(get_hq_admin_user)
):
    try:
        id = ObjectId(item_id)
        exesting_doc = university_collection.find_one({"_id":id, "is_deleted":False})
        if not exesting_doc:
            return HTTPException(status_code=404, detail=f"Stock does not exits")
        resp = university_collection.update_one({"_id":id},{"$set":{"is_deleted":True}})
        raise {"status_code":200, "message":"Stock deleted Successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")
