from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

OPENAI_API = os.getenv("OPENAI_API_KEY")

if not OPENAI_API:
    raise ValueError("A variável de ambiente OPENAI_API_KEY não foi carregada corretamente.")

