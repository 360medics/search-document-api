from fastapi.routing import APIRouter

from application.src.core.es_search import analyze_es_text, explain_es_match

router = APIRouter(prefix="/utils")


@router.get("/analyze")
async def es_analyze(text: str):
    """This route is for running analyze es command

    Args:
        text (str): text to analyze in es

    Returns:
        dict: analyze text token by token
    """
    return analyze_es_text(text)


@router.get("/explain")
async def es_explain(id: str):
    """This route is for running analyze es command

    Args:
        text (str): text to analyze in es

    Returns:
        dict: analyze text token by token
    """
    return explain_es_match(id)
