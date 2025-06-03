from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from config import OPENAI_API 
import os

from langchain_openai import ChatOpenAI

# Carrega chave da OpenAI
os.environ["OPENAI_API_KEY"] = OPENAI_API

# Define o modelo OpenAI 
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Ferramenta de pesquisa Serper (Google Search API)
pesquisa = SerperDevTool(api_key=os.getenv("SERPER_API"))

# Agente coordenador
krakinho = Agent(
    role="Coordenador da equipe de montagem de computadores do site OctoCore",
    goal="Ajudar clientes com pouco conhecimento a montar o melhor PC possível com base no que desejam",
    backstory="Você trabalha há anos na OctoCore ajudando clientes a entender as melhores opções para montar seus PCs.",
    tools=[pesquisa],
    llm=llm,
    verbose=True,
    allow_delegation=True,
)

# Agente montador
montador = Agent(
    role="Especialista em montagem de computadores gamer",
    goal="Pesquisar peças compatíveis e ideais para atender às exigências do cliente, dentro do orçamento",
    backstory="Você já teve PCs ruins e aprendeu por conta própria a montar setups otimizados. Hoje, pesquisa a fundo para entregar as melhores combinações de peças.",
    tools=[pesquisa],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Agente verificador
verificador = Agent(
    role="Verificador de orçamento",
    goal="Revisar se o orçamento foi respeitado e sugerir ajustes, se necessário",
    backstory="Especialista em finanças para configurações de PC. Sua função é validar orçamentos dos técnicos.",
    tools=[],
    llm=llm,
    verbose=True
)

# Agente suporte 
suporte = Agent(
    role="Atendente de suporte ao cliente do OctoCore",
    goal="Responder dúvidas frequentes e ajudar o cliente a usar o site de forma eficiente",
    backstory="Você é um especialista no uso da plataforma OctoCore, ajudando diariamente usuários com problemas comuns, como como montar um PC, fazer login, rastrear pedidos, entender prazos de entrega e devoluções.",
    tools=[],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Tarefa de montagem
montarPC = Task(
    description="Montar um PC para jogos com orçamento de até R$5000. Deve rodar bem jogos populares como Fortnite, GTA V e Valorant.",
    expected_output="Lista de componentes com nome, modelo e preço aproximado",
    agent=montador,
)
# Crew
crew = Crew(
    agents=[krakinho, montador, verificador],
    tasks=[montarPC],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n💻 Resultado da montagem:\n")
    print(result)
