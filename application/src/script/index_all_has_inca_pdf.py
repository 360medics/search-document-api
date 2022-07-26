import requests
import os
from tqdm import tqdm
import google.auth.transport.requests
import google.oauth2.id_token


URL = (
    "https://europe-west1-data-api-dev-55313450491.cloudfunctions.net/HandleToolsUpsert"
)
key = "settings/key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key


def createTokenForGCP(audience):
    auth_req = google.auth.transport.requests.Request()
    return google.oauth2.id_token.fetch_id_token(auth_req, audience)


TOKEN = createTokenForGCP(URL)
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def index_pdf_to_elasticsearch(tool_name: str, id: int, url: str, title: str):

    d = {
        "name": f"{tool_name}",
        "typeTool": "externe",
        "toolId": id,
        "source": f"{url}",
        "url": f"{url}",
        "title": f"{title}",  # PDF Name
        "crawled": True,
    }

    resp = requests.post(URL, headers=HEADERS, json=d)
    return resp.json()


with open("data/pdf_list.txt", "r") as f:
    fnames = f.readlines()

BASE_URL = "https://d218dw8cc3oete.cloudfront.net/defi-has/"

tool_mapping = {"HAS": {"tool_name": "Défi HAS", "tool_id": 9999999}}


for fname in tqdm(fnames):
    url = BASE_URL + fname.replace("\n", "")
    splitted_url = url.split("/")
    title = splitted_url[-1]
    folder = splitted_url[-2]
    tool_name = tool_mapping.get(folder).get("tool_name")
    tool_id = tool_mapping.get(folder).get("tool_id")
    index_pdf_to_elasticsearch(tool_name=tool_name, id=tool_id, url=url, title=title)
