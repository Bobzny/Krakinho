import requests
from crewai_tools import BaseTool

class ConsultaAPIProdutos(BaseTool):
    name = "consulta_api_produtos"
    description = "Consulta uma API de produtos retornando nome, preço e quantidade"

    def _run(self, query: str) -> str:
        url = f"http://localhost/octocore_api/produtos?busca={query}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if not data:
                return "Nenhum produto encontrado."

            return "\n".join([f"{item['nome']} - R${item['preco']} - {item['quantidade']} disponíveis" for item in data])
        except Exception as e:
            return f"Erro na consulta: {str(e)}"
