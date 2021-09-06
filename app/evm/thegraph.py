import requests
import json
from . import utils

async def call_graph(url, post_json, session):

    headers = {'Content-type': 'application/json;charset=UTF-8'}
    data = await utils.make_post_json(session, url, kwargs={'json': post_json, 'headers' : headers})
    return data