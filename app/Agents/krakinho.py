from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from config import OPENAI_API
from .montador import montador
from .suporte import suporte
from .revisor import revisor
import os

# Define chave
os.environ["OPENAI_API_KEY"] = OPENAI_API
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Agente chefe
krakinho = Agent(
    role="Agente-chefe de atendimento da krakinho",
    goal="Interpretar a dúvida do cliente e encaminhar para o agente mais apropriado ou responder diretamente",
    backstory="""Você é o krakinho, o cérebro por trás do atendimento ao cliente na krakinho.
Com anos de experiência, você entende quando encaminhar tarefas para especialistas técnicos ou responder diretamente,
sempre garantindo que o cliente tenha uma resposta clara e confiável.""",
    llm=llm,
    verbose=True,
    allow_delegation=True,
    tools=[]
)

# Entrada do cliente
pergunta = input("Digite a pergunta do cliente: ")

# Task principal do Krakinho
tarefa_geral = Task(
    description=f"Interpretar e responder ou delegar a dúvida do cliente: '{pergunta}'",
    expected_output="Resposta clara e precisa, seja técnica (montagem) ou informativa (uso do site)",
    agent=krakinho
)

# Crew
krakinho_crew = Crew(
    agents=[krakinho, montador, suporte, revisor],
    tasks=[tarefa_geral],
    verbose=True
)

if __name__ == "__main__":
    resultado = krakinho_crew.kickoff()
    print("\n🤖 Resposta final ao cliente:\n")
    print(resultado)
