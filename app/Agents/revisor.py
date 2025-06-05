from crewai import Agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

revisor = Agent(
    role="Verificador de qualidade de resposta",
    goal="Revisar a resposta antes de ser enviada ao cliente para garantir precisão, clareza e cordialidade",
    backstory="Você é um agente experiente que revisa todas as respostas antes de irem ao cliente, evitando erros ou falta de empatia.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)
