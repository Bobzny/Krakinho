from fastapi import FastAPI, WebSocket 
from pydantic import BaseModel
import requests
import asyncio

#Instanciando o app pra rodar com o uvicorn dps
app = FastAPI()

@app.websocket("/chat")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    conversa = []
    while True:
        data = await websocket.receive_text()
        resposta = krakinho(historico = conversa,entrada=data)
        conversa.append({"role": "user", "content": data})
        conversa.append({"role": "bot", "content": resposta})
        await asyncio.sleep(5)
        await websocket.send_text(resposta)


def krakinho (historico,entrada):
    return f"{historico}{entrada}? Krakinho está pronto para ajudar!"
