import json
import logging

import requests

from config import Config

logger = logging.getLogger("uvicorn.error")


def get_search(text):
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
        f"{Config.baseURI}/v3/search/tool", params=params, json=body, headers=headers
    )
    return json.loads(resp.content.decode("utf-8")).get("results")


def get_medics(text):
    params = {"lang": "fr", "q": text, "medics_area": "ansm", "offset": 0, "limit": 1}
    resp = requests.post(
        f"{Config.MEDICS_URL_API}/rcp/v0",
        params=params,
    )
    return json.loads(resp.content.decode("utf-8")).get("results")[0]


def get_sve(text):
    params = {
        "lang": "fr",
        "q": text,
        "medics_area": "ansm",
        "highlight": True,
        "offset": 0,
        "limit": 1,
        "page": 1,
        "courtry": "FR",
        "skiprcppart": 0,
    }
    resp = requests.post(
        f"{Config.SVE_URL_API}/v1",
        params=params,
    )
    return json.loads(resp.content.decode("utf-8")).get("results")
