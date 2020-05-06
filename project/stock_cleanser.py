import requests
import common
from stock_evaluator import get_dicts
from stock_evaluator import get_jsn_as_dict
import json

with open('companies.json') as json_file:
    data = json.load(json_file)

def get_key_metric(label):
    
key_metrics = get_dicts("key_metrics")

for company_dict in data["symbolsList"]:
    company_label = company_dict["symbol"]

#data["symbolsList"][0]["symbol"]
