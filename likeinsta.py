import time

import requests
import json

key = 'f3995d08154230d16a450e0e053f13b19bb140dc4ce11d94'

host = "https://api-public.likeinsta.ru/v1"

request_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json;charset=UTF-8",
    "X-Api-Key": key
}

method = '/bots/tasks/?service_type=1&task_type=3'

url = host + method

response = requests.get(url, headers=request_headers)
decoder_json = json.loads(response.text)
values = decoder_json['data']['items']


def hide(value):
    method1 = '/bots/tasks/'
    method2 = '/hide'
    method11 = method1 + value + method2
    url = host + method11
    response = requests.post(url, headers=request_headers)
    decoder_json = json.loads(response.text)
    print(decoder_json)

def do(value):
    method1 = '/bots/tasks/'
    method2 = '/do'
    method11 = method1 + value + method2
    url = host + method11
    response = requests.get(url, headers=request_headers)
    decoder_json = json.loads(response.text)
    print(decoder_json)


def check(value):
    method1 = '/bots/tasks/'
    method2 = '/check'
    method11 = method1 + value + method2
    url = host + method11
    response = requests.get(url, headers=request_headers)
    decoder_json = json.loads(response.text)
    print(decoder_json)

for i in range(10):
    value = values[i]['id']
    print(value)
    do(value)
    check(value)
# do('1023481')
# check('1023481')
