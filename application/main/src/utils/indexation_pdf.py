import requests
import os
import google.auth.transport.requests
import google.oauth2.id_token


URL = (
    "https://europe-west1-data-api-dev-55313450491.cloudfunctions.net/HandleToolsUpsert"
)
key = "/Users/louisgabilly/Documents/search-document-api/settings/key.json"
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


d = {
    "name": "Défi HAS",
    "typeTool": "externe",
    "toolId": 9999999,
    "source": "https://d218dw8cc3oete.cloudfront.net/defi-has/Publication_HAS/EvaluationDesPratiques/c_2874187/c_2032151/2018-10-09_note_de_cadrage_coordination_mg_psy.pdf",  # noqa: E501
    "url": "https://d218dw8cc3oete.cloudfront.net/defi-has/Publication_HAS/EvaluationDesPratiques/c_2874187/c_2032151/2018-10-09_note_de_cadrage_coordination_mg_psy.pdf",  # noqa: E501
    "title": "COMMISSION DE LA TRANSPARENCE",  # PDF Name
    "crawled": True,
}


if __name__ == "__main__":

    resp = index_pdf_to_elasticsearch(
        tool_name="Défi HAS",
        id="externe",
        url="https://d218dw8cc3oete.cloudfront.net/defi-has/Publication_HAS/EvaluationDesPratiques/c_2874187/c_2032151/2018-10-09_note_de_cadrage_coordination_mg_psy.pdf",  # noqa: E501
        title="COMMISSION DE LA TRANSPARENCE",
    )

    print(resp)
