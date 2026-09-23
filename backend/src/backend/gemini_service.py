import json
import os

from google import genai
from google.genai import errors as genai_errors

_MODELO = "gemini-2.5-flash"

_cliente: genai.Client | None = None


class GeminiIndisponivelError(Exception):
    pass


class GeminiRespostaVaziaError(Exception):
    pass


def _obter_cliente() -> genai.Client:
    global _cliente

    if _cliente is None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise GeminiIndisponivelError("GEMINI_API_KEY não configurada")

        _cliente = genai.Client(api_key=api_key)

    return _cliente


def _gerar_lista_json(prompt: str) -> list[str]:
    cliente = _obter_cliente()

    try:
        resposta = cliente.models.generate_content(
            model=_MODELO,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
        )
    except (genai_errors.ServerError, genai_errors.APIError) as erro:
        raise GeminiIndisponivelError(str(erro)) from erro
    except Exception as erro:
        raise GeminiIndisponivelError(str(erro)) from erro

    texto = (resposta.text or "").strip()

    if not texto:
        raise GeminiRespostaVaziaError("Gemini retornou resposta vazia")

    try:
        itens = json.loads(texto)
    except json.JSONDecodeError as erro:
        raise GeminiRespostaVaziaError("Gemini retornou resposta em formato inválido") from erro

    itens = [item.strip() for item in itens if isinstance(item, str) and item.strip()]

    if not itens:
        raise GeminiRespostaVaziaError("Gemini não retornou nenhum item")

    return itens


def identificar_afirmacoes(conteudo: str) -> list[str]:
    prompt = (
        "Você é um assistente de checagem de fatos. Leia o conteúdo abaixo e "
        "identifique as afirmações factuais que podem ser verificadas "
        "(potencialmente verificáveis). Retorne APENAS um array JSON de "
        "strings, uma string por afirmação, sem comentários adicionais.\n\n"
        f"Conteúdo:\n{conteudo}"
    )

    return _gerar_lista_json(prompt)


def gerar_perguntas(texto_afirmacao: str) -> list[str]:
    prompt = (
        "Você é um assistente de checagem de fatos. Para a afirmação abaixo, "
        "gere perguntas orientadoras que ajudem uma pessoa a investigar e "
        "analisar criticamente essa afirmação. Retorne APENAS um array JSON "
        "de strings, uma string por pergunta, sem comentários adicionais.\n\n"
        f"Afirmação:\n{texto_afirmacao}"
    )

    return _gerar_lista_json(prompt)
