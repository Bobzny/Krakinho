from fastapi import FastAPI, WebSocket 
from app.crew import responder

#Instanciando o app pra rodar com o uvicorn dps
app = FastAPI()

@app.websocket("/chat")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    conversa = []
    while True:
        data = await websocket.receive_text()
        resposta = responder(pergunta = data,historico=conversa)
        conversa.append({"role": "user", "content": data})
        conversa.append({"role": "bot", "content": resposta})
        await websocket.send_text(str(resposta))
