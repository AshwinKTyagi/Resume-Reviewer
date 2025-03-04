from fastapi import APIRouter, HTTPException
import heapq
import numpy as np
from . import resume_repository, process_llm, file_processing

chat_router = APIRouter()

@chat_router.post("/")
async def chat(file_id: str, message: str, model: str = "openai"):
    try:
        resume_text, _ = resume_repository.get_resume_by_file_id(file_id)
        
        if not resume_text:
            raise HTTPException(status_code=404, detail="File not found")
        
        prompt = f"""
            Resume: {resume_text}
            
            User Question: {message}
            Answer:
        """
        
        response = process_llm.process(prompt, model, "")
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@chat_router.get("/similar-resumes")
async def get_similar_resumes(user_id: str, query: str):
    try:
        query_embedding = file_processing.generate_embeddings(query)
        
        user_resumes = resume_repository.get_user_resumes(user_id)
        n = len(user_resumes)

        similarties = []
        for doc in user_resumes:
            embedding = np.array(doc["embedding"])
            score = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
            heapq.heappush(similarties(-score, doc))
    

        return [heapq.heappop(similarties)[1] for _ in range(n)]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))