from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from config import Config


es_client = Elasticsearch(
    hosts=f"https://data-elastic-{Config.ENV_STATE}.360medics.com:9200",
    http_auth=("elastic", "david"),
    verify_certs=True,
)
indices_client = IndicesClient(es_client)
