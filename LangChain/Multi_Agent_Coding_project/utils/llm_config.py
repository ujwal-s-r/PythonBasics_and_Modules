#shared LLM models
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
google_api_key=os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")
try:
    shared_llm= ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=google_api_key,
        temperature=0.2
        )
    print("utils/llm_config.py: Shared LLM initialized successfully.")
except:
    raise ValueError("Failed to initialize shared LLM. Please check your GOOGLE_API_KEY and internet connection.")