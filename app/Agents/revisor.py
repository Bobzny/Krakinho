from crewai import Agent
from langchain_openai import ChatOpenAI
from app.config import OPENAI_API
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

revisor = Agent(
    role="Verificador de qualidade de resposta",
    goal="Reescreva qualquer resposta que não seja diretamente endereçada ao cliente, que contenha pensamentos do agente ou explicações sobre o processo interno. A resposta final deve sempre ser uma mensagem clara, objetiva e diretamente para o cliente, em português brasileiro."

,
    backstory="Você é um agente experiente que revisa todas as respostas antes de irem ao cliente, evitando erros e respostas que não são diretas ao cliente.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)
