import pdfminer.high_level
from docx import Document


def __from_pdf(fp):
    return pdfminer.high_level.extract_text(fp)

def __from_docx(fp):
    doc = Document(fp)
    return "\n".join([p.text for p in doc.paragraphs])


def extract(file_path, file_ext):
    if file_ext == "pdf":
        __from_pdf(file_path)
    elif file_ext == "docx":
        __from_docx(file_path)
    
