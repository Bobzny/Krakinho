from crewai import Agent
from langchain_openai import ChatOpenAI
from config import OPENAI_API
from tools.consulta_estoque import EstoqueTool  
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

montador = Agent(
    role="Especialista técnico em montagem de PCs Gamer",
    goal="Sugerir as melhores peças possíveis com base no orçamento e necessidades do cliente",
    backstory="Você é o técnico principal da OctoCore. Sabe montar PCs para qualquer jogo ou uso, sempre respeitando compatibilidade e orçamento.",
    tools=[EstoqueTool()],
    llm=llm,
    verbose=True,
    allow_delegation=False
)