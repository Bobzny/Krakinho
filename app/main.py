from fastapi import FastAPI 
from pydantic import BaseModel

#Instanciando o app pra rodar com o uvicorn dps
app = FastAPI()

class InputProps(BaseModel):
    nome: str
    preco: float

@app.get("/")
def home():
    return {"mensagem": "Isso ai 2"}
