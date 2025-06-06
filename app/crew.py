from crewai import Task, Crew
from app.config import OPENAI_API
from app.Agents.krakinho import krakinho
from app.Agents.montador import montador
from app.Agents.suporte import suporte
from app.Agents.revisor import revisor
import os

# Configuração da chave da OpenAI
os.environ["OPENAI_API_KEY"] = OPENAI_API



def responder(pergunta, historico):

    # 🔸 Tarefa principal (Krakinho escolhe)
    tarefa_principal = Task(
        description=f"Entenda a dúvida: '{pergunta}' e analise o histórico da sua conversa com o cliente{historico}. Se for sobre montagem de PC, delegue ao técnico montador. Se for sobre uso do site, chame o suporte. Sempre revise a resposta com o revisor se for necessário. No final, entregue uma resposta clara ao cliente e sempre em português brasileiro.",
        expected_output="Uma resposta completa e precisa para a dúvida do cliente",
        agent=krakinho
    )

    # 🔹 Crew
    crew = Crew(
        agents=[krakinho, montador, suporte, revisor],
        tasks=[tarefa_principal],
        verbose=True
    )
    resultado = crew.kickoff()
    print(resultado)
    return resultado

        
