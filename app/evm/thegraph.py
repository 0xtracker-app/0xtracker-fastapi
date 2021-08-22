import requests
import json

def call_graph(url, post_json):

    headers = {'Content-type': 'application/json;charset=UTF-8'}
    return json.loads(requests.post(url, json=post_json, headers=headers).text)