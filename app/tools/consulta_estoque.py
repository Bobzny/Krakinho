from fastapi import FastAPI 
from pydantic import BaseModel
import requests

#Instanciando o app pra rodar com o uvicorn dps
app = FastAPI()

class InputProps(BaseModel):
    nome: str
    preco: float

@app.get("/")
def home():
    return {"mensagem": "Isso ai 2"}

@app.get("/produtos")
def buscarEstoque(categoria = ''):
    if categoria == '':
        url = "http://localhost/octocore_api/produtos"
    else:
        url = f"http://localhost/octocore_api/produtos/{categoria}"

    resposta = requests.get(url, timeout=5)
    return resposta.json()
        
