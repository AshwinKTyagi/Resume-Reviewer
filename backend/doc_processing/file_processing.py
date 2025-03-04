import pdfminer.high_level
from docx import Document
import numpy as np
from langchain_community.embeddings import OpenAIEmbeddings

# Extract text from a PDF file
def __from_pdf(fp):
    return pdfminer.high_level.extract_text(fp)

# Extract text from a DOCX file
def __from_docx(fp):
    doc = Document(fp)
    return "\n".join([p.text for p in doc.paragraphs])

# Main method used to extract text based on file extension
def extract(file_path, file_ext):
    if file_ext == "pdf":
        return __from_pdf(file_path)
    elif file_ext == "docx":
        return __from_docx(file_path)

# Generate an embedding for a given text using OpenAI
def generate_embeddings(text):
    embedding_model = OpenAIEmbeddings()
    return embedding_model.embed_documents([text])

