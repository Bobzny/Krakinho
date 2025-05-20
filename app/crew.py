from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from config import SERPER_API, GEMINI_API
import os 

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]
os.environ["GEMINI_API_KEY"] = GEMINI_API


from google.generativeai import GenerativeModel, configure

class GeminiTool(BaseTool):
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        super().__init__(
            name="GeminiTool",
            description="Usa a API do Gemini para responder perguntas e gerar conteúdo."
        )
        configure(api_key=api_key)
        self._model = GenerativeModel(model_name)

    def _run(self, input: str) -> str:
        response = self._model.generate_content(input)
        return response.text.strip()



pesquisa = SerperDevTool(api_key=SERPER_API)
gemini = GeminiTool(api_key=GEMINI_API)

#Criação dos agentes do sistema
krakinho = Agent(
    role="Coordenador da equipe de montagem de computadores do site octocore",
    goal="Distribuir as tarefas entre os membros da equipe para garantir que o melhor computador possível seja montado pro cliente e fazer toda a interação direta com o cliente",
    backstory="Você trabalha a muitos anos na empresa octocore ajudando os clientes que não tem muito conhecimento a montarem seus computadores de acordo com oque eles pedem, tambem tem um conhecimento suficiente para tirar dúvidas básicas sobre esse processo",
    tools=[gemini],
    verbose= True,
    allow_delegation=True,
    llm=llm
)

montador= Agent(
    role="Especialista em montagem de computadores dos mais variados tipos do site octocore",
    goal="Pesquisa na internet por peças que se adequem aos requisitos passados pelo cliente ao krakinho, verificando compatibilidades e jogos que o cliente especificou que gostaria de conseguir jogar",
    backstory="No passado ja teve computadores ruins e aprendeu a montar pcs por conta própria, sendo especialista em pesquisas detalhadas para saber exatamente oque um computador precisa para atingir uma certa performance ",
    tools=[pesquisa, gemini],
    verbose= True,
    allow_delegation=False,
    llm=llm
)


montarPC = Task(
    description="Encontrar uma configuração ideal de PC para jogos com orçamento de até R$5000",
    expected_output="Lista de componentes com nome, modelo e preço aproximado",
    agent=montador,
)


crew = Crew(
    agents=[krakinho, montador],
    tasks=[montarPC],
    verbose=True
)

result = crew.kickoff()
print(result)