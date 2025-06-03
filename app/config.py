from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

OPENAI_API = os.getenv("OPENAI_API_KEY")
SERPER_API = os.getenv("SERPER_API")

if not OPENAI_API:
    raise ValueError("A variável de ambiente OPENAI_API_KEY não foi carregada corretamente.")

if not SERPER_API:
    raise ValueError("A variável de ambiente SERPER_API não foi carregada corretamente.")
