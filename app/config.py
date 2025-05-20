from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")
SERPER_API = os.getenv("SERPER_API")

os.environ["GEMINI_API_KEY"] = GEMINI_API