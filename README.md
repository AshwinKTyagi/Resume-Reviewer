# Resume-Reviewer

## Tech Stack

**Backend**
- FastAPI
- pdfminer
- python-docx
- OpenAI API
- LLAMA
- MongoDB
- FastAPI JWT Auth
- Python Dotenv
- LangChain Community Embeddings

**Frontend**
- NextJS
- TailwindCSS
- React Dropzone
- React Markdown

## Overview

This project allows users to upload their resumes in PDF or DOCX format. The backend extracts the text from the uploaded resume and processes it using a language model to provide feedback.

### Backend

#### `main.py`
- Entry point for the FastAPI application.
- Initializes the FastAPI app and includes the routes for authentication and resume handling.
- Configures middleware for CORS and exception handling.
- Connects to the MongoDB database and sets up JWT authentication.
- Runs the FastAPI server when executed directly.

#### `config_mongo.py`
- Configuration for MongoDB connection and JWT secret.

#### `upload_resume/file_processing.py`
- Contains functions to handle file uploads and text extraction.
    - `process_pdf(file)`: Extracts text from an uploaded PDF file.
    - `process_docx(file)`: Extracts text from an uploaded DOCX file.
    - `process_file(file)`: Determines the file type and extracts text accordingly.
    - `generate_embeddings(text)`: Generates embeddings for the extracted text using a language model.

#### `upload_resume/process_llm.py`
- Contains functions to process the extracted text using LLAMA or OpenAI.
    - `__test_llama_connection()`: Tests connection to the LLAMA server.
    - `__test_openai_connection(client)`: Tests connection to the OpenAI API.
    - `__process_with_llama(extracted_text, prompt)`: Processes text using the LLAMA server.
    - `__process_with_openai(extracted_text, prompt)`: Processes text using the OpenAI API.
    - `process(extracted_text, option, prompt)`: Main method to process text based on the selected option (LLAMA or OpenAI).

#### `upload_resume/resume_repository.py`
- Contains functions to interact with the MongoDB database for resume storage and retrieval.
    - `get_user_resumes(user_id)`: Retrieves all resumes for a specific user.
    - `get_resume(file_id)`: Retrieves the extracted text and feedback for a specific resume.
    - `save_resume_feedback(user_id, filename, extracted_text, feedback, file_bytes, embedding)`: Saves the resume feedback and embedding to the database.
    - `get_resume_embedding(file_id)`: Retrieves the embedding for a specific resume if it exists.

#### `upload_resume/resume_routes.py`
- FastAPI routes for handling resume uploads, retrieval, and feedback.
    - `get_all_resumes(user_id: Optional[str])`: Retrieves all resumes for a specific user.
    - `get_resume(user_id: str, file_id: str)`: Retrieves the extracted text and feedback for a specific resume.
    - `upload_resume(file: UploadFile, modelOption: Optional[str], userId: Optional[str])`: Uploads a resume, extracts text, generates embeddings, and gets feedback from the language model.

#### `auth/auth_utils.py`
- Utility functions for password hashing, JWT creation, and verification.
    - `hash_password(password: str) -> str`: Hashes a plain text password using bcrypt.
    - `verify_password(plain_password: str, hashed_password: str) -> bool`: Verifies a plain text password against a hashed password.
    - `create_jwt_token(user_id: str) -> str`: Creates a JWT token with the user ID and an expiration time of 1 day.
    - `verify_jwt(token: str) -> dict`: Verifies a JWT token and returns the decoded token if valid, otherwise raises an error.

#### `auth/auth_routes.py`
- FastAPI routes for user registration, login, and protected routes.
    - `root()`: A simple root endpoint for the authentication service.
    - `register(user: UserRegister)`: Registers a new user by hashing their password and storing their details in the database.
    - `login(user: UserLogin)`: Logs in a user by verifying their email and password, and returns a JWT token if successful.
    - `protected_route(token: str = Depends(auth_utils.verify_jwt))`: A protected route that requires a valid JWT token to access.

### Frontend

#### `components/layout.js`
- Layout component for wrapping pages with a consistent header and footer.
- Displays navigation links and user information.

#### `index.js`
- React component for the home page.
- Provides links to the login and upload pages.

#### `upload.js`
- React component to handle file uploads and display extracted text and feedback.
- Uses `react-dropzone` for file drag-and-drop functionality.
- Allows users to select between OpenAI and LLAMA models for feedback.
- Sends the uploaded file to the backend for text extraction and feedback.
- Displays the extracted text and feedback in a formatted manner.

#### `login.js`
- React component to handle user login and registration.
- Allows users to register a new account or log in to an existing account.
- Uses context to manage authentication state.

#### `resume_list.js`
- React component to display a list of resumes and their feedback.
- Fetches resumes for the logged-in user and displays them in a sidebar.
- Allows users to select a resume to view its extracted text and feedback.

#### `context/AuthContext.js`
- Context provider for managing authentication state.
- Provides functions for logging in and logging out.

#### `utils/auth.js`
- Utility functions for handling authentication-related tasks.
    - `register(userData)`: Registers a new user.
    - `login(userData)`: Logs in a user and stores the token and user information in local storage.
    - `logout()`: Logs out a user by removing the token and user information from local storage.

#### `_app.tsx`
- Custom App component for Next.js.
- Wraps the application with the `AuthProvider` to provide authentication context to all pages.

## Installation and Setup

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
4. Set up environment variables for OpenAI or if you are hosting LLAMA:
        ```sh
        OPENAI_API_KEY='your_openai_api_key'
        LLAMA_SERVER='http://your-llama-server:11434'
        MONGO_URI='your_mongo_uri'
        JWT_SECRET='your_jwt_secret'
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