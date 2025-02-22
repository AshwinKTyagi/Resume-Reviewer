from config_mongo import resume_collection, db
from pydantic import BaseModel
import gridfs
from bson import ObjectId
import datetime

fs = gridfs.GridFS(db)

#Pydantic model for resumes
class Resume(BaseModel):
    user_id: str
    file_name: str 
    feedback: str
    created_at: datetime.datetime

def save_resume_feedback(user_id: str, file_name:str, resume_text: str, feedback: str, file_content: bytes):
    file_id = fs.put(file_content, filename=file_name, content_type="application/pdf")
    
    document = {
        "user_id": user_id,
        "file_name": file_name,
        "resume_text": resume_text,
        "feedback": feedback,
        "file_id": file_id,
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc)
    }
    
    resume_collection.insert_one(document)
    
def get_resume_feedback(user_id: str, file_name: str, resume_txt: str):
    query = {
        "user_id": user_id,
        "file_name": file_name,
        "resume_text": resume_txt
    }
    result = resume_collection.find_one(query)
    if result:
        return result.get("feedback")
    return None

def get_user_resumes(user_id: str):
    resumes = resume_collection.find({"user_id": user_id})
    return [{"id": str(resume["_id"]), "file_id": str(resume["file_id"]), "file_name": resume["file_name"], "created_at": resume["created_at"]} for resume in resumes]
    
def get_resume(user_id: str, file_id: str):
    query = {
        "_id": ObjectId(file_id)
    }
    result = resume_collection.find_one(query)
    if result:
        return [result.get("resume_text"), result.get("feedback")]
    return None