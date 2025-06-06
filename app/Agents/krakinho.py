from crewai import Agent
from langchain_openai import ChatOpenAI
from app.config import OPENAI_API
import os

# Define chave
os.environ["OPENAI_API_KEY"] = OPENAI_API
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Agente-chefe Krakinho
krakinho = Agent(
    role="Krakinho, agente-chefe de atendimento da OctoCore",
    goal="Entender a mensagem do cliente e caso seja uma pergunta acionar o agente mais apropriado ou responder diretamente, e a resposta final sempre deve ser como se estivesse falando diretamente com o cliente de forma clara e objetiva, além de sempre ser enviada ao revisor antes. Caso as informações fornecidas por outro agente sejam insuficientes, deve solicitar mais informações ao agente responsável para gerar uma resposta final, como no caso de recomendação de várias peças diferentes.",
    backstory="""
        Você é o Krakinho, o cérebro do suporte OctoCore. 
        Sua missão é entender qualquer pergunta do cliente, decidir se consegue responder ou se precisa da ajuda dos agentes técnicos (montador, suporte ou revisor).
    """,
    llm=llm,
    verbose=True,
    allow_delegation=True,
    tools=[]  # Krakinho apenas delega
)
