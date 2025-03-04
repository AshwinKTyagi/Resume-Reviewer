from openai import OpenAI
import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the LLAMA server URL from environment variables, default to localhost if not set
LLAMA_SERVER = os.getenv("LLAMA_SERVER", "http://localhost:11434")
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

base_prompt = ("You are a professional resume reviewer. "
        "Analyze the following resume text and provide feedback on the candidate's strengths, weaknesses, "
        "and suggestions for improvement. Focus on the clarity, relevance, and impact of the information provided. "
        "Ensure your feedback is in raw markdown format, with correct bullet points and formatting."
        "Ignore formatting issues."
        "Also, highlight any grammatical errors. Here is the resume text:\n\n")

# Function to test connection to the LLAMA server
def __test_llama_connection():
    try:
        # Send a GET request to the LLAMA server
        response = requests.get(f"{LLAMA_SERVER}/api/tags", timeout=3)  
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

# Function to test connection to the OpenAI API
def __test_openai_connection(client):
    try:
        # List available models from OpenAI
        response = client.models.list()
        if response:
            return True
    except Exception:
        pass
    return False

# Function to process resume text using the LLAMA server
def __process_with_llama(extracted_text: str, prompt: str):
    if not __test_llama_connection():
        return "Error: Unable to connect to llama server."

    # Create a prompt for the LLAMA server
    llama_prompt = (
        f"{prompt}"
        f"{extracted_text}"
    )

    try:
        # Send a POST request to the LLAMA server with the prompt
        response = requests.post(f"{LLAMA_SERVER}/api/generate", json={
            "model": "llama3.1:latest",
            "prompt": f"{llama_prompt}"
        })
        return response.json().get("response", "No response from llama.")
    except Exception as e:
        return f"Error processing resume: {str(e)}"

# Function to process resume text using the OpenAI API
def __process_with_openai(extracted_text: str, prompt: str):

    try:
        # Initialize the OpenAI client
        client = OpenAI(api_key=OPEN_API_KEY)

        if not __test_openai_connection(client):
            return "Error: Unable to connect to llama server."
        
        # Create a chat completion request to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": extracted_text}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing resume: {str(e)}"

# Main function to process resume text based on the selected option (LLAMA or OpenAI)
def process(extracted_text: str, option: str, prompt: str = base_prompt):
    if option == "ollama":
        return __process_with_llama(extracted_text, prompt)
    elif option == "openai":
        return __process_with_openai(extracted_text, prompt)
    
    
