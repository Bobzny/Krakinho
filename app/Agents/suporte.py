from crewai import Agent
from langchain_openai import ChatOpenAI
from app.config import OPENAI_API
from app.tools.faq_tool import FAQTool
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Caminho para o arquivo FAQ
faq_path = os.path.join(os.path.dirname(__file__), "..", "data", "faq_octocore.json")
faq_tool = FAQTool(os.path.abspath(faq_path))

suporte = Agent(
    role="Especialista em atendimento da plataforma OctoCore",
    goal="Ajudar o usuário a navegar e usar o site, resolvendo dúvidas comuns com precisão",
    backstory="Você é experiente em atendimento, conhece a fundo todas as funcionalidades do site e responde com empatia e clareza.",
    tools=[faq_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)