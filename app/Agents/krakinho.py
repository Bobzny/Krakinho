from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from app.config import OPENAI_API
import os

# Define chave
os.environ["OPENAI_API_KEY"] = OPENAI_API
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Agente chefe
# Agente-chefe Krakinho
krakinho = Agent(
    role="Krakinho, agente-chefe de atendimento da OctoCore",
    goal="Entender a pergunta do cliente e acionar o agente mais apropriado ou responder diretamente",
    backstory="""
        Você é o Krakinho, o cérebro do suporte OctoCore. 
        Sua missão é entender qualquer pergunta do cliente, decidir se consegue responder ou se precisa da ajuda dos agentes técnicos (montador, suporte ou revisor).
    """,
    llm=llm,
    verbose=True,
    allow_delegation=True,
    tools=[]  # Krakinho apenas delega
)
