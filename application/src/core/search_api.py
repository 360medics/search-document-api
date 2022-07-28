import requests
import json
from config import Config


def get_search_all(text):
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
    resp = requests.post(f"{Config.baseURI}/v3/search/tools", params=params)
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
