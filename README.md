# Resume-Reviewer

### Tech Stack

Backend
- FastAPI
- pdfminer
- python-docx
- OpenAI API
- LLAMA

Frontend
- NextJS
- TailwindCSS
- React Dropzone
- React Markdown

### Overview

This project allows users to upload their resumes in PDF or DOCX format. The backend extracts the text from the uploaded resume and processes it using a language model to provide feedback.

### Backend

#### `extract_from_file.py`
- Contains functions to extract text from PDF and DOCX files.
- `__from_pdf(fp)`: Extracts text from a PDF file.
- `__from_docx(fp)`: Extracts text from a DOCX file.
- `extract(file_path, file_ext)`: Main method to extract text based on file extension.

#### `process_llm.py`
- Contains functions to process the extracted text using LLAMA or OpenAI.
- `__test_llama_connection()`: Tests connection to the LLAMA server.
- `__test_openai_connection(client)`: Tests connection to the OpenAI API.
- `__process_with_llama(extracted_text)`: Processes text using the LLAMA server.
- `__process_with_openai(extracted_text)`: Processes text using the OpenAI API.
- `process(extracted_text, option)`: Main method to process text based on the selected option (LLAMA or OpenAI).

#### `main.py`
- FastAPI application to handle file uploads and text extraction.
- `upload_resume(file: UploadFile)`: Endpoint to upload a resume, extract text, and get feedback from the language model.

### Frontend

#### `index.js`
- React component to handle file uploads and display extracted text and feedback.
- Uses `react-dropzone` for file drag-and-drop functionality.
- Sends the uploaded file to the backend for text extraction and feedback.
- Displays the extracted text and feedback in a formatted manner.

### Installation and Setup

#### Prerequisites
- Python 3.8+
- Node.js 14+
- npm 6+

#### Backend Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/resume-reviewer.git
    cd resume-reviewer/backend
    ```
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Set up environment variables for OpenAI or if you are hosting ollama :
    ```sh
    OPENAI_API_KEY='your_openai_api_key'
    LLAMA_SERVER='http://your-llama-server:11434'
    ```
5. Run the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```

#### Frontend Setup
1. Navigate to the frontend directory:
    ```sh
    cd ../frontend
    ```
2. Install the required dependencies:
    ```sh
    npm install
    ```
3. Start the Next.js development server:
    ```sh
    npm run dev
    ```

Your application should now be running, with the backend accessible at `http://localhost:8000` and the frontend at `http://localhost:3000`.