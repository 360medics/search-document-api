from application.main.src.utils.indexation_pdf import index_pdf_to_elasticsearch
from tqdm import tqdm

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
