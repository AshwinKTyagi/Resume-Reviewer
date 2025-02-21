from config_mongo import resume_collection
from pydantic import BaseModel
import datetime

#Pydantic model for resumes
class Resume(BaseModel):
    user_id: str
    file_name: str 
    resume_text: str
    feedback: str
    created_at: datetime.datetime

def save_resume_feedback(user_id: str, file_name:str, resume_text: str, feedback: str):
    document = {
        "user_id": user_id,
        "file_name": file_name,
        "resume_text": resume_text,
        "feedback": feedback,
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