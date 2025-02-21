from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from upload_resume import extract_from_file
from upload_resume import process_llm 
from upload_resume import resume_repository
from auth.auth_routes import auth_router
import os

app = FastAPI()
app.include_router(auth_router, prefix="/auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Reviewer API"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...), modelOption: Optional[str] = Form("openai"), userId: Optional[str] = Form(None)):
    
    
    # Write the uploaded file's content to a temporary path
    original_filename = file.filename
    file_ext = file.filename.split(".")[-1]
    temp_path = f"temp.{file_ext}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Extract information from file
    txt = extract_from_file.extract(temp_path, file_ext)    
    os.remove(temp_path)

    # If invalid filetype, raise an error
    if not txt:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    
    # If user is provided, check if a document exists
    if userId:
        resume_feedback = resume_repository.get_resume_feedback(userId, original_filename, txt)
        if resume_feedback:
            return {"extracted_text": txt, "llm_feedback": resume_feedback}
    
    llm_feedback = process_llm.process(txt, option=modelOption)

    # Save data
    if userId:
        resume_repository.save_resume_feedback(userId, original_filename, txt, llm_feedback)


    return {"extracted_text": txt, "llm_feedback": llm_feedback}


