from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from upload_resume import extract_from_file
from upload_resume import process_llm 
from upload_resume import resume_repository
from upload_resume.resume_routes import resume_router
from auth.auth_routes import auth_router
import os

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(resume_router, prefix="/resumes", tags=["Resumes"])

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




