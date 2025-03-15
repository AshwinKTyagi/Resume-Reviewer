from config_mongo import resume_collection, db
from pydantic import BaseModel
import gridfs
from bson import ObjectId
import datetime

# Initialize GridFS
fs = gridfs.GridFS(db)

# Pydantic model for resumes
class Resume(BaseModel):
    user_id: str
    file_id: str
    file_name: str 
    resume_text: str
    feedback: str
    embedding: list[float]
    created_at: datetime.datetime

# Function to save resume feedback
def save_resume_feedback(user_id: str, file_name: str, resume_text: str, feedback: str, file_content: bytes, embedding: list[float]):
    file_id = fs.put(file_content, filename=file_name, content_type="application/pdf")
    
    document = {
        "user_id": user_id,
        "file_id": file_id,
        "file_name": file_name,
        "resume_text": resume_text,
        "feedback": feedback,
        "chat_history": [],
        "embedding": embedding,
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc)
    }
    
    resume_collection.insert_one(document)
    
def save_resume_chat_history(file_id: str, chat_history: list[dict]):
    query = {
        "_id": ObjectId(file_id)
    }
    update = {
        "$set": {
            "chat_history": chat_history
        }
    }
    resume_collection.update_one(query, update)

# Function to get all resumes for a user
def get_user_resumes(user_id: str) -> list[dict]:
    resumes = resume_collection.find({"user_id": user_id})
    return [{"id": str(resume["_id"]), "file_id": str(resume["file_id"]), "file_name": resume["file_name"], "created_at": resume["created_at"], "embedding": resume["embedding"]} for resume in resumes]

# Function to get resume by user_id and original_filename
def get_resume(user_id: str, original_filename: str, resume_text: str):
    query = {
        "user_id": user_id,
        "file_name": original_filename,
        "resume_text": resume_text
    }
    result = resume_collection.find_one(query)
    if result:
        return [result["resume_text"], result["feedback"]]
    return None

# Function to get resume by file_id
def get_resume_by_file_id(file_id: str):
    query = {
        "_id": ObjectId(file_id)
    }
    result = resume_collection.find_one(query)
    if result:
        return [result.get("resume_text"), result.get("feedback")]
    return None

# Function to get resume embedding by file_id
def get_resume_embedding(file_id: str):
    query = {
        "_id": ObjectId(file_id)
    }
    result = resume_collection.find_one(query)
    if result:
        return result.get("embedding")
    return None

# Function to get chat history by file_id
def get_resume_chat_messages(file_id:str):
    query = {
        "_id": ObjectId(file_id)
    }
    result = resume_collection.find_one(query)
    if result:
        return [result.get("chat_history"), result.get("resume_text"), result.get("feedback")]
    return [[], None, None]