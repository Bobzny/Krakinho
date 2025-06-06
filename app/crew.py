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
        description=f"Entenda a dúvida: '{pergunta}' e analise o histórico da sua conversa com o cliente se houver: {historico}. Se for sobre montagem de PC, delegue ao técnico montador. Se for sobre uso do site, chame o suporte. Antes de enviar uma resposta final a mensagem deve ser revisada pelo agente revisor. No final, entregue uma resposta clara e concisa ao cliente, evitando explicar coisas desnecessariamente a menos que solicitado, sempre em português brasileiro e sempre falando diretamente com o cliente na resposta final, caso não esteja deve ser alterada.",
        expected_output="Uma resposta enxuta, precisa e não exageradamente formal para a dúvida do cliente, sempre falando diretamente com ele na resposta final, sob nenhuma hipótese deve ser uma resposta que não diga diretamente ao cliente o que ele perguntou ou algum pensamento do agente, deve ser uma resposta clara e objetiva, sem rodeios, e sempre em português brasileiro.",
        
        agent=krakinho)

    # 🔹 Crew
    crew = Crew(
        agents=[krakinho, montador, suporte, revisor],
        tasks=[tarefa_principal],
        verbose=True
    )
    resultado = crew.kickoff()

    # Checagem automática para evitar pensamentos do agente
    frases_proibidas = [
        "A dúvida do cliente é",
        "Como agente",
        "Devo delegar",
        "Antes de enviar a resposta final",
        "Como Krakinho",
        "Como agente-chefe",
        "Como técnico",
        "Como revisor",
        "Como suporte",
        "Como montador",
        "Uma resposta enxuta, precisa e não exageradamente formal para a dúvida do cliente, sempre falando diretamente com ele na resposta final, sob nenhuma hipótese deve ser uma resposta que não diga diretamente ao cliente o que ele perguntou ou algum pensamento do agente, deve ser uma resposta clara e objetiva, sem rodeios, e sempre em português brasileiro.",
        "Verificar disponibilidade na OctoCore"
    ]

    if any(frase.lower() in str(resultado).lower() for frase in frases_proibidas):

        tarefa_revisao = Task(
        description=(
            "Reescreva a seguinte resposta para que seja clara, objetiva e diretamente para o cliente, "
            "sem pensamentos do agente, sem mencionar agentes, delegações ou processos internos. "
            "A resposta deve ser exatamente o que o cliente deve receber, como se estivesse falando diretamente com ele. "
            "Exemplo ruim: Vou acionar o técnico montador para fornecer as recomendações."
            "Exemplo bom: Para jogar Cyberpunk 2077, recomendamos as seguintes peças: ..."
            f"Resposta original: {resultado}"
        ),
        expected_output=(
            "Uma resposta clara, objetiva e diretamente para o cliente, em português brasileiro, "
            "sem mencionar agentes, delegações ou processos internos."
        ),
        agent=revisor
    )
        crew_revisao = Crew(
            agents=[revisor],
            tasks=[tarefa_revisao],
            verbose=False
        )
        resultado = crew_revisao.kickoff()

    return resultado

        
