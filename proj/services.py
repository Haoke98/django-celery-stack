# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/6
@Software: PyCharm
@disc:
======================================="""
import os

from elasticsearch import Elasticsearch
from saer import Saer

print("ES_URI", os.getenv("ES_URI"))
saerAPI = Saer(os.getenv("SAER_ID"), os.getenv("SAER_KEY"))
es_client = Elasticsearch(os.getenv("ES_URI"), http_auth=(os.getenv("ES_USERNAME"), os.getenv("ES_PASSWORD")),
                          ca_certs=os.getenv("ES_CA_CERTS"),
                          timeout=3600)