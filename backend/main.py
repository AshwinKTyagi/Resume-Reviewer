from fastapi import FastAPI, File, UploadFile
from extract import extract
import os

app = FastAPI()

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

    txt = extract(temp_path, file_ext)
        
    os.remove(temp_path)
    if not txt:
        return {"error": "Unsupported File Path"}
    else:
        return {"extracted_text": txt}
    

