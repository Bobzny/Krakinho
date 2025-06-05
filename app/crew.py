from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from config import OPENAI_API
from Agents.montador import montador
from Agents.suporte import suporte
from Agents.revisor import revisor
import os

# Configuração da chave da OpenAI
os.environ["OPENAI_API_KEY"] = OPENAI_API

# LLM para o Krakinho
llm_chefe = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Agente-chefe Krakinho
krakinho = Agent(
    role="Agente-chefe de atendimento da OctoCore",
    goal="Entender a pergunta do cliente e acionar o agente mais apropriado ou responder diretamente",
    backstory="""
        Você é o Krakinho, o cérebro do suporte OctoCore. 
        Sua missão é entender qualquer pergunta do cliente, decidir se consegue responder ou se precisa da ajuda dos agentes técnicos (montador, suporte ou revisor).
    """,
    llm=llm_chefe,
    verbose=True,
    allow_delegation=True,
    tools=[]  # Krakinho apenas delega
)

# 🔹 Entrada do cliente
pergunta = input("Digite a pergunta do cliente:\n> ")

# 🔸 Tarefa principal (Krakinho escolhe)
tarefa_principal = Task(
    description=f"Entenda a dúvida: '{pergunta}'. Se for sobre montagem de PC, delegue ao técnico montador. Se for sobre uso do site, chame o suporte. Sempre revise a resposta com o revisor se for necessário. No final, entregue uma resposta clara ao cliente.",
    expected_output="Uma resposta completa e precisa para a dúvida do cliente",
    agent=krakinho
)

# 🔹 Crew
crew = Crew(
    agents=[krakinho, montador, suporte, revisor],
    tasks=[tarefa_principal],
    verbose=True
)

# 🔸 Executa
if __name__ == "__main__":
    resultado = crew.kickoff()
    print("\n🤖 Resposta final para o cliente:\n")
    print(resultado)
