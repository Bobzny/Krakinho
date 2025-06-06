from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field 
import requests

class EstoqueInput(BaseModel):
    categoria: str = Field(..., description="Categoria do produto, como 'processador','placaMae','memoriaRam','placaDeVideo','ssd','hd','cooler','fonte','gabinete','fans','so','software'")
    filtro_nome: Optional[str] = Field(None, description="Nome do produto ou palavra-chave para filtrar resultados.")

class EstoqueTool(BaseTool):
    name: str = "EstoqueTool"
    description: str = "Consulta o estoque da OctoCore pela API interna"
    args_schema: Type[BaseModel] = EstoqueInput

    def _run(self, categoria: str) -> str:
        try:
            if categoria.strip() == "":
                url = "http://localhost/octocore_api/produtos"
            else:
                url = f"http://localhost/octocore_api/produtos/{categoria}"

            resposta = requests.get(url, timeout=5)
            resposta.raise_for_status()
            dados = resposta.json()

            if not dados:
                return f"Nenhum produto encontrado para a categoria '{categoria}'."

            # Formata os produtos encontrados
            produtos_formatados = []
            for item in dados:
                nome = item.get("nome")
                preco = item.get("preco")
                produtos_formatados.append(f"- {nome} (R$ {preco})")

            return "\n".join(produtos_formatados)

        except requests.exceptions.RequestException as e:
            return f"Erro ao consultar o estoque: {str(e)}"
