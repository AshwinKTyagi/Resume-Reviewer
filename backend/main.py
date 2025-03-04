from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from doc_processing.resume_routes import resume_router
from doc_processing.chat_routes import chat_router
from auth.auth_routes import auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(resume_router, prefix="/resumes", tags=["Resumes"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

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




