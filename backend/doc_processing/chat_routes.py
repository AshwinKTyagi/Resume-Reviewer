from typing import List, Dict, Optional, TypedDict
from fastapi import APIRouter, HTTPException, Form, Query
import heapq
import numpy as np
from . import resume_repository, process_llm, file_processing
from .chat_utils import Message, ChatSession

chat_router = APIRouter()
chat_session: Dict[str, ChatSession] = {}

@chat_router.post("/")
async def chat(file_id: str = Form(...), message: str = Form(...), model: str = "openai"):
    try:
        print(chat_session.keys(), file_id)
        if file_id in chat_session:
            session = chat_session[file_id]
        else:
            raise HTTPException(status_code=404, detail="Chat session not found.")
        
        resume_text = session.resume
        resume_feedback = session.feedback
        
        formatted_chat_history = "\n".join([f"{msg.type}: {msg.text}" for msg in session.messages])
    
        
        prompt = f"""
            You are a professional recruiter reviewing a resume. Have your feedback be succinct and constructive.
            When asked to give feedback, you should provide a response that uses short bullet points.
            Give some concrete examples of your feedback.
            You can make up some information if you need to, but make sure you let the user know that you are giving an example.
            Ensure your feedback is in raw markdown format, with correct bullet points and formatting.
            If you are unsure about something, you can say that you are unsure.
            Try not to repeat information that has already been given unless explicitly asked to.
            The user has uploaded a resume and received feedback.

            Resume: 
            {resume_text}
            
            Feedback: 
            {resume_feedback}
            
            Chat History:
            {formatted_chat_history}
                        
            User: {message}
            Assistant:
        """
        
        response = process_llm.process(message, model, prompt)
        
        session.messages.append(Message(type="user", text=message))
        session.messages.append(Message(type="bot", text=response))
        
        session_messages_json = [msg.__dict__ for msg in session.messages]

        resume_repository.save_resume_chat_history(file_id, session_messages_json)
        return {"response": response}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
     
@chat_router.get("/start-chat")
async def start_chat(file_id: Optional[str] = Query(None)):
    if file_id in chat_session:
        session = chat_session[file_id]
    
    messages, txt, feedback = resume_repository.get_resume_chat_messages(file_id)
    
    session = ChatSession(messages=messages, resume=txt, feedback=feedback)
        
    chat_session[file_id] = session
    print(chat_session.keys(), file_id)
    return [msg.__dict__ for msg in session.messages]
    
    
    
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