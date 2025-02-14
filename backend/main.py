from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import extract_from_file
import process_llm 
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Resume Reviewer API"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):

    # Write the uploaded file's content to a temporary path
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
    
    llm_feedback = process_llm.process(txt, option="openai")
    
    return {"extracted_text": txt, "llm_feedback": llm_feedback}
    

