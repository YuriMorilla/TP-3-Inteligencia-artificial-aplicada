"""Templates de prompt para as tarefas de LLM planejadas (TP4).

Nenhum LLM é chamado aqui: o objetivo do TP3 é deixar os dados e os
prompts prontos para a próxima etapa.
"""

from __future__ import annotations

PROMPTS: dict[str, dict] = {
    "resumo": {
        "titulo": "Resumo automático",
        "tipos": ["texto", "noticia"],
        "descricao": "Condensar textos longos (artigos, notícias) em poucas frases.",
        "template": (
            "Você é um analista de políticas educacionais. Resuma em até 3 frases, "
            "em português, o texto abaixo, preservando números e nomes próprios.\n\n"
            "TEXTO:\n{texto}\n\nRESUMO:"
        ),
    },
    "sentimento": {
        "titulo": "Classificação de sentimento",
        "tipos": ["noticia"],
        "descricao": "Classificar manchetes de notícias como positivo, negativo ou neutro.",
        "template": (
            "Classifique o sentimento da manchete abaixo em relação ao cenário "
            "educacional. Responda com UMA palavra: positivo, negativo ou neutro.\n\n"
            "MANCHETE: {texto}\nSENTIMENTO:"
        ),
    },
    "qa": {
        "titulo": "Perguntas e respostas (Q&A)",
        "tipos": ["texto", "indicador", "noticia"],
        "descricao": "Responder perguntas usando apenas os documentos coletados como contexto.",
        "template": (
            "Responda à pergunta usando APENAS o contexto. Se a resposta não estiver "
            "no contexto, responda \"Não sei\".\n\nCONTEXTO:\n{contexto}\n\n"
            "PERGUNTA: {pergunta}\nRESPOSTA:"
        ),
    },
    "geracao": {
        "titulo": "Geração de relatório",
        "tipos": ["indicador"],
        "descricao": "Gerar um parágrafo descritivo/insight a partir dos indicadores municipais.",
        "template": (
            "Escreva um parágrafo curto de relatório para gestores municipais de "
            "educação, em português, com base nos dados abaixo. Destaque desigualdades "
            "e não invente números.\n\nDADOS:\n{texto}\n\nRELATÓRIO:"
        ),
    },
}


def render(task: str, **kwargs: str) -> str:
    """Preenche o template da tarefa com os valores informados."""
    return PROMPTS[task]["template"].format(**kwargs)
