import json
import logging

import requests

from config import Config
from application.services.es_service import es_client

logger = logging.getLogger("uvicorn.error")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 4SJxKlCP9ucc6pzVXVv9zurURQ96Um7d",
    "X-User-Api-Key": "1ade9001222a075902bc1ea12e0dc643",
}

payload = json.dumps(
    {
        "id": 2,
        "specialty_id": 10,
        "profession_id": 2,
        "title": "DOCTOR",
        "roles": ["ROLE_EXPERT"],
    }
)


def get_search(text, env="dev"):
    params = {
        "lang": "fr",
        "q": text,
        "medics_area": "ansm",
        "highlight": True,
        "offset": 0,
        "limit": 10,
        "page": 1,
        "country": "FR",
        "skiprcppart": 0,
    }
    body = {
        "body": {
            "id": 2,
            "specialty_id": 10,
            "profession_id": 2,
            "title": "DOCTOR",
            "roles": ["ROLE_EXPERT"],
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token 4SJxKlCP9ucc6pzVXVv9zurURQ96Um7d",
        "X-User-Api-Key": "1ade9001222a075902bc1ea12e0dc643",
    }
    resp = requests.post(
        f"{Config.baseURI if (env == 'dev') else Config.baseURIPROD}/v3/search/all",
        params=params,
        json=body,
        headers=headers,
    )
    return json.loads(resp.content.decode("utf-8")).get("results")


def get_medics(text):
    params = {"lang": "fr", "q": text, "medics_area": "ansm", "offset": 0, "limit": 1}
    resp = requests.post(
        f"{Config.MEDICS_URL_API}/rcp/v0",
        params=params,
    )
    return json.loads(resp.content.decode("utf-8")).get("results")[0]


def get_tools(text):

    logger.debug(text)

    params = {"lang": "fr", "q": text, "medics_area": "ansm", "offset": 0, "limit": 1}

    resp = requests.post(
        f"{Config.baseURIPROD}/v3/search/tool",
        headers=headers,
        params=params,
        data=payload,
    )

    logger.debug(resp)

    return json.loads(resp.content.decode("utf-8")).get("results")


def get_sve(text):

    logger.debug(text)
    params = {
        "lang": "fr",
        "q": text[:102],
        "medics_area": "ansm",
        "highlight": True,
        "offset": 0,
        "limit": 1,
        "page": 1,
        "courtry": "FR",
        "skiprcppart": 0,
        "min_score": 0,
    }
    resp = requests.post(
        f"{Config.SVE_URL_API}/v1/elastic/vector",
        params=params,
    )

    logger.debug(resp)

    if str(resp.status_code) == "200":
        return json.loads(resp.content.decode("utf-8")).get("results")

    return []


def get_direct_es(text):
    res = es_client.search(
        query={
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"match": {"id": {"query": "1290", "boost": 100}}},
                                {"match": {"id": "56"}},
                                {"match": {"id": "31"}},
                                {"match": {"id": "916"}},
                            ]
                        }
                    },
                    {
                        "bool": {
                            "should": [
                                {"match": {"title": f"{text}"}},
                                {"match": {"title.synonyms": f"{text}"}},
                            ]
                        }
                    },
                ]
            }
        },
        _source_includes=["title", "document.url"],
    )
    return res


def get_result_related(text):
    if "Classification TNM" in text:
        return [
            {
                "category": "tool",
                "data": {
                    "id": 849,
                    "name": "Classification des tumeurs - SFJRO",
                    "source": "https://tools.360medics.com/com.SFJRO.medics/0.0.1",
                },
            }
        ]

    elif "Traitement" in text:
        return get_tools(text=text)
    else:
        return []
