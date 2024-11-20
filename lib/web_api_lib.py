#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def get_api_data(url,headers=None):
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data


def post_api_data(url, payload, headers=None):
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    data = json.loads(response.text)
    return data