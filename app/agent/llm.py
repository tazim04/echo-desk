from app.config import GROQ_API_KEY
from langchain_groq import ChatGroq

MODEL = "llama-3.3-70b-versatile"

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL,
    temperature=0.1,
    max_tokens=1000,
    timeout=30,
    max_retries=2,
)
