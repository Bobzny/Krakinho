from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, PrivateAttr
import json
import difflib

class FAQInput(BaseModel):
    pergunta: str = Field(..., description="A pergunta do usuário")

class FAQTool(BaseTool):
    name: str = "FAQTool"
    description: str = "Fornece respostas com base nas perguntas frequentes da OctoCore"
    args_schema: Type[BaseModel] = FAQInput
    
    # Usar PrivateAttr para dados que não fazem parte do schema
    _faq_data: list = PrivateAttr()

    def __init__(self, json_path: str, **kwargs):
        super().__init__(**kwargs)
        with open(json_path, "r", encoding="utf-8") as f:
            self._faq_data = json.load(f)

    def _run(self, pergunta: str) -> str:
        perguntas = [item["pergunta"] for item in self._faq_data]
        correspondencia = difflib.get_close_matches(pergunta, perguntas, n=1, cutoff=0.4)

        if correspondencia:
            pergunta_encontrada = correspondencia[0]
            for item in self._faq_data:
                if item["pergunta"] == pergunta_encontrada:
                    return item["resposta"]
        return "Desculpe, não encontrei uma resposta para sua pergunta."
