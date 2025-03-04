from fastapi import APIRouter, HTTPException, Form
import heapq
import numpy as np
from . import resume_repository, process_llm, file_processing

chat_router = APIRouter()

@chat_router.post("/")
async def chat(resume_text: str = Form(...), message: str = Form(...), model: str = "openai"):
    try:
        if not resume_text:
            raise HTTPException(status_code=404, detail="File not found")
        
        prompt = f"""
            You are a professional recruiter reviewing a resume. Have your feedback be succinct and constructive.
            When asked to give feedback, you should provide a response that uses short bullet points.
            Give some concrete examples of your feedback.
            You can make up some information if you need to, but make sure you let the user know that you are giving an example.
            Ensure your feedback is in raw markdown format, with correct bullet points and formatting.
            If you are unsure about something, you can say that you are unsure.
            The resume is as follows:
            Resume: {resume_text}
            
            Answer:
        """
        
        response = process_llm.process(message, model, prompt)
        print(response)
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